#!/usr/bin/env python3
"""webhook_tools.py - debug a LINE Messaging API webhook endpoint without the LINE app.

Commands
  sign FILE                 print the x-line-signature LINE would send for FILE's exact bytes
  verify FILE SIGNATURE     check a captured body + signature against your channel secret
  sample TYPE               print a realistic webhook payload (fixture for unit tests)
  simulate URL [TYPE]       sign a payload with your channel secret and POST it to URL
  selftest URL              run a battery: console "Verify" ping, valid event, bad/missing signature

The channel secret is read from $LINE_CHANNEL_SECRET (or --secret-env / --env-file) and never printed.
Payloads use fake IDs and reply tokens, so any reply your bot attempts will fail with
"Invalid reply token" - that's expected; this tool tests receiving, not replying.

Python 3.8+, standard library only.
Docs: https://developers.line.biz/en/docs/messaging-api/verify-webhook-signature/
      https://developers.line.biz/en/reference/messaging-api/#webhook-event-objects
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import random
import string
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

LINE_TIMEOUT_MS = 2000  # LINE records request_timeout when your server takes longer than 2 s
SIG_DOC = "https://developers.line.biz/en/docs/messaging-api/verify-webhook-signature/"


def _setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load_env_file(path):
    p = Path(path)
    if not p.is_file():
        sys.exit(f"--env-file not found: {path}")
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:]
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def get_secret(args):
    name = args.secret_env or "LINE_CHANNEL_SECRET"
    s = os.environ.get(name, "").strip()
    if not s:
        sys.exit(f"No channel secret: set {name} (Messaging API channel > Basic settings > Channel secret), "
                 f"or pass --env-file / --secret-env.")
    return s


def signature(secret, body_bytes):
    mac = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).digest()
    return base64.b64encode(mac).decode("ascii")


# --------------------------------------------------------------------------- payloads

def _hex(n):
    return "".join(random.choice("0123456789abcdef") for _ in range(n))


def _ulid():
    return "01" + "".join(random.choice(string.digits + "ABCDEFGHJKMNPQRSTVWXYZ") for _ in range(24))


def _msg_id():
    return str(random.randint(10 ** 17, 10 ** 18 - 1))


def make_event(kind, source, user_id, group_id, text, data):
    src = {"type": source, "userId": user_id}
    if source == "group":
        src = {"type": "group", "groupId": group_id, "userId": user_id}
    elif source == "room":
        src = {"type": "room", "roomId": "R" + _hex(32), "userId": user_id}
    ev = {"type": kind, "timestamp": int(time.time() * 1000), "source": src, "mode": "active",
          "webhookEventId": _ulid(), "deliveryContext": {"isRedelivery": False}}
    reply = {"replyToken": _hex(32)}
    if kind == "text":
        ev["type"] = "message"
        ev["message"] = {"type": "text", "id": _msg_id(), "quoteToken": "q" + _hex(40), "text": text}
        ev.update(reply)
    elif kind == "mention":  # group text that @mentions the bot itself
        ev["type"] = "message"
        label = "@Bot "
        ev["message"] = {"type": "text", "id": _msg_id(), "quoteToken": "q" + _hex(40),
                         "text": label + text,
                         "mention": {"mentionees": [{"index": 0, "length": len(label) - 1,
                                                     "type": "user", "userId": "U" + _hex(32),
                                                     "isSelf": True}]}}
        ev.update(reply)
    elif kind == "image":
        ev["type"] = "message"
        ev["message"] = {"type": "image", "id": _msg_id(), "quoteToken": "q" + _hex(40),
                         "contentProvider": {"type": "line"}}
        ev.update(reply)
    elif kind == "sticker":
        ev["type"] = "message"
        ev["message"] = {"type": "sticker", "id": _msg_id(), "quoteToken": "q" + _hex(40),
                         "packageId": "446", "stickerId": "1988", "stickerResourceType": "STATIC",
                         "keywords": ["OK"]}
        ev.update(reply)
    elif kind == "postback":
        ev["postback"] = {"data": data}
        ev.update(reply)
    elif kind == "follow":
        ev["follow"] = {"isUnblocked": False}
        ev.update(reply)
    elif kind == "unfollow":
        pass
    elif kind == "join":
        ev["source"] = {"type": "group", "groupId": group_id}
        ev.update(reply)
    elif kind == "leave":
        ev["source"] = {"type": "group", "groupId": group_id}
    elif kind == "memberJoined":
        ev["source"] = {"type": "group", "groupId": group_id}
        ev["joined"] = {"members": [{"type": "user", "userId": user_id}]}
        ev.update(reply)
    elif kind == "memberLeft":
        ev["source"] = {"type": "group", "groupId": group_id}
        ev["left"] = {"members": [{"type": "user", "userId": user_id}]}
    elif kind == "unsend":
        ev["unsend"] = {"messageId": _msg_id()}
    else:
        raise SystemExit(f"unknown event type {kind}")
    return ev


EVENT_TYPES = ["text", "mention", "image", "sticker", "postback", "follow", "unfollow", "join",
               "leave", "memberJoined", "memberLeft", "unsend", "verify"]


def make_payload(args, kind=None):
    kind = kind or args.type
    destination = args.destination or ("U" + _hex(32))
    if kind == "verify":  # what the console's Verify button / a connectivity check sends
        return {"destination": destination, "events": []}
    ev = make_event(kind, args.source, args.user_id or "U" + _hex(32),
                    args.group_id or "C" + _hex(32), args.text, args.data)
    return {"destination": destination, "events": [ev]}


def body_bytes(payload):
    # Compact, non-ASCII kept as UTF-8 - like LINE. Your server must hash these exact bytes.
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# --------------------------------------------------------------------------- http

def post(url, body, sig, timeout=10):
    headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "LineBotWebhook/2.0"}
    if sig is not None:
        headers["x-line-signature"] = sig
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, text = r.status, r.read(2000)
    except urllib.error.HTTPError as e:
        status, text = e.code, e.read(2000)
    except urllib.error.URLError as e:
        return None, int((time.monotonic() - t0) * 1000), str(e.reason)
    except (TimeoutError, OSError) as e:  # socket read timeouts aren't wrapped in URLError
        ms = int((time.monotonic() - t0) * 1000)
        reason = f"timed out after {timeout} s" if isinstance(e, TimeoutError) or "timed out" in str(e) else str(e)
        return None, ms, reason
    return status, int((time.monotonic() - t0) * 1000), text.decode("utf-8", errors="replace")


def describe(status, ms, text):
    if status is None:
        if "timed out" in (text or ""):
            return (f"no response ({text}) - LINE gives up after about {LINE_TIMEOUT_MS // 1000} s, "
                    f"so this delivery would count as request_timeout")
        return f"could not connect ({text})"
    flag = "" if ms <= LINE_TIMEOUT_MS else f"  <-- slower than LINE's {LINE_TIMEOUT_MS} ms limit (request_timeout)"
    snippet = (text or "").strip().replace("\n", " ")[:200]
    return f"HTTP {status} in {ms} ms{flag}" + (f"  body: {snippet}" if snippet else "")


# --------------------------------------------------------------------------- commands

MISMATCH_CHECKLIST = f"""Common causes (see {SIG_DOC}):
  - the body was parsed/re-serialized before hashing (use the raw request bytes, e.g. await req.text() / raw body middleware)
  - the secret belongs to another channel (e.g. the LINE Login/LIFF channel instead of the Messaging API channel)
  - the channel secret was reissued and the server still has the old one
  - a proxy / framework / platform rewrote the body (pretty-printing, charset conversion, escaping)
  - hashing with the wrong algorithm/encoding (must be HMAC-SHA256, key = channel secret, base64 digest)"""


def cmd_sign(args):
    secret = get_secret(args)
    print(signature(secret, Path(args.file).read_bytes()))
    return 0


def cmd_verify(args):
    secret = get_secret(args)
    raw = Path(args.file).read_bytes()
    expected = signature(secret, raw)
    if hmac.compare_digest(expected, args.signature.strip()):
        print("OK: signature matches this body and secret.")
        return 0
    print("MISMATCH: the signature does not match this exact body with this secret.")
    try:
        compact = body_bytes(json.loads(raw.decode("utf-8")))
        if compact != raw and hmac.compare_digest(signature(secret, compact), args.signature.strip()):
            print("  -> it DOES match after compact re-serialization: the file you captured was reformatted "
                  "(your server or logger is not hashing the raw bytes).")
    except Exception:
        pass
    print(MISMATCH_CHECKLIST)
    return 1


def cmd_sample(args):
    print(json.dumps(make_payload(args), ensure_ascii=False, indent=2))
    return 0


def cmd_simulate(args):
    if args.body:
        body = Path(args.body).read_bytes()
    else:
        body = body_bytes(make_payload(args))
    if args.no_signature:
        sig = None
    elif args.bad_signature:
        sig = base64.b64encode(os.urandom(32)).decode()
    else:
        sig = signature(get_secret(args), body)
    status, ms, text = post(args.url, body, sig, timeout=args.timeout)
    print(describe(status, ms, text))
    if args.show_body:
        print(body.decode("utf-8"))
    if args.bad_signature or args.no_signature:
        if status is not None and 200 <= status < 300:
            print("WARNING: your server accepted a request with an invalid/missing signature. "
                  "Anyone could forge events. Reject it (e.g. 401/403) before doing any work.")
            return 1
        return 0
    return 0 if status is not None and 200 <= status < 300 and ms <= LINE_TIMEOUT_MS else 1


def cmd_selftest(args):
    secret = get_secret(args)
    results = []

    def run(name, payload, sig_mode, expect_ok):
        body = body_bytes(payload)
        sig = {"good": signature(secret, body), "bad": base64.b64encode(os.urandom(32)).decode(),
               "none": None}[sig_mode]
        status, ms, text = post(args.url, body, sig, timeout=args.timeout)
        ok = status is not None and 200 <= status < 300
        passed = (ok == expect_ok) and (not expect_ok or ms <= LINE_TIMEOUT_MS)
        results.append(passed)
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {describe(status, ms, text)}")
        return status

    print(f"Target: {args.url}")
    run("console Verify ping (empty events) -> expect 2xx", make_payload(args, "verify"), "good", True)
    run(f"{args.type} event, valid signature -> expect 2xx within 2 s", make_payload(args), "good", True)
    run("valid payload, WRONG signature -> expect rejection (4xx)", make_payload(args), "bad", False)
    run("valid payload, NO signature header -> expect rejection (4xx)", make_payload(args), "none", False)
    if not all(results[:2]):
        print("\nIf the first two fail with 401/403 before your code runs, look for an auth layer in front of "
              "the handler (e.g. Supabase Edge Functions verify a JWT by default - deploy the webhook function "
              "with JWT verification disabled and rely on the LINE signature instead).")
        print(MISMATCH_CHECKLIST)
    return 0 if all(results) else 1


def main(argv=None):
    _setup_stdout()
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--secret-env", help="env var with the channel secret (default LINE_CHANNEL_SECRET)")
    common.add_argument("--env-file", help="load KEY=VALUE pairs (e.g. your bot's .env) first")

    ev = argparse.ArgumentParser(add_help=False)
    ev.add_argument("--source", choices=["user", "group", "room"], default="user")
    ev.add_argument("--text", default="hello from webhook_tools")
    ev.add_argument("--data", default="action=test&id=1", help="postback data")
    ev.add_argument("--user-id")
    ev.add_argument("--group-id")
    ev.add_argument("--destination", help="bot user ID to put in 'destination'")

    p = argparse.ArgumentParser(prog="webhook_tools.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND")
    s = sub.add_parser("sign", parents=[common], help="signature for a body file")
    s.add_argument("file")
    s = sub.add_parser("verify", parents=[common], help="check body file + signature")
    s.add_argument("file")
    s.add_argument("signature")
    s = sub.add_parser("sample", parents=[ev], help="print a sample webhook payload")
    s.add_argument("type", choices=EVENT_TYPES)
    for name in ("simulate", "selftest"):
        s = sub.add_parser(name, parents=[common, ev],
                           help="POST a signed event" if name == "simulate" else "run a battery of checks")
        s.add_argument("url")
        s.add_argument("type", nargs="?", default="text", choices=EVENT_TYPES)
        s.add_argument("--timeout", type=int, default=10)
        if name == "simulate":
            s.add_argument("--body", help="send this exact file instead of a generated payload")
            s.add_argument("--bad-signature", action="store_true")
            s.add_argument("--no-signature", action="store_true")
            s.add_argument("--show-body", action="store_true")
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 2
    if getattr(args, "env_file", None):
        load_env_file(args.env_file)
    return {"sign": cmd_sign, "verify": cmd_verify, "sample": cmd_sample,
            "simulate": cmd_simulate, "selftest": cmd_selftest}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # output piped into `head` etc.
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        sys.exit(0)
