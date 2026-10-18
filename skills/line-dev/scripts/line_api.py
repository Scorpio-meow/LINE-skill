#!/usr/bin/env python3
"""line_api.py - a small, dependency-free CLI for the LINE Messaging API.

Built for an AI agent operating the API on a developer's behalf:

* Read-only commands (info, quota, profile, richmenu-list, validate, ...) run immediately.
* Commands that send messages or change what users see (push, multicast, broadcast,
  webhook-set, richmenu-deploy, richmenu-set-default, ...) are DRY RUNS by default:
  they validate, print exactly what would be sent plus cost/quota notes, and exit
  without changing anything. Re-run with --yes only after the human confirmed.
* The channel access token comes from an environment variable (default
  LINE_CHANNEL_ACCESS_TOKEN) or --env-file, and is never printed.

Python 3.8+, standard library only. Run `python line_api.py -h` for the command list.
Official reference: https://developers.line.biz/en/reference/messaging-api/
"""

import argparse
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API = "https://api.line.me"
API_DATA = "https://api-data.line.me"  # content download + rich menu image upload/download
REF = "https://developers.line.biz/en/reference/messaging-api/"

# Pre-flight limits checked locally before calling the API. They mirror the official
# reference as of 2026-10; the API's own validate endpoints are authoritative.
MAX_MESSAGES_PER_REQUEST = 5          # REF#send-push-message ("Max: 5")
MAX_MULTICAST_RECIPIENTS = 500        # REF#send-multicast-message
RICHMENU_MAX_IMAGE_BYTES = 1024 * 1024  # REF#upload-rich-menu-image-requirements

EXIT_OK, EXIT_API_ERROR, EXIT_USAGE, EXIT_NO_TOKEN = 0, 1, 2, 3


# --------------------------------------------------------------------------- output

def _setup_stdout():
    # Windows consoles (e.g. cp950/cp932) choke on emoji/CJK; force UTF-8 with replacement.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def out(obj):
    if isinstance(obj, (dict, list)):
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(obj)


def err(msg):
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------- config

def load_env_file(path):
    """Load KEY=VALUE lines into os.environ without overriding existing values."""
    p = Path(path)
    if not p.is_file():
        err(f"--env-file not found: {path}")
        sys.exit(EXIT_USAGE)
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, val = line.partition("=")
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), val)


def get_token(args, required=True):
    name = getattr(args, "token_env", None) or "LINE_CHANNEL_ACCESS_TOKEN"
    tok = os.environ.get(name, "").strip()
    if not tok and required:
        err(f"No channel access token: set the {name} environment variable "
            f"(or pass --env-file path/to/.env, or --token-env OTHER_NAME).\n"
            f"Issue one in LINE Developers Console > your Messaging API channel > Messaging API tab.")
        sys.exit(EXIT_NO_TOKEN)
    return tok or None


# --------------------------------------------------------------------------- http

class ApiResult:
    def __init__(self, status, headers, body, elapsed_ms):
        self.status = status
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}
        self.body = body or b""
        self.elapsed_ms = elapsed_ms

    @property
    def ok(self):
        return 200 <= self.status < 300

    def json(self):
        if not self.body:
            return {}
        try:
            return json.loads(self.body.decode("utf-8"))
        except Exception:
            return {"_raw": self.body.decode("utf-8", errors="replace")[:2000]}

    @property
    def request_id(self):
        return self.headers.get("x-line-request-id")


def request(method, url, token, body=None, content_type="application/json",
            extra_headers=None, timeout=30):
    headers = {"User-Agent": "line-dev-skill/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        if isinstance(body, (bytes, bytearray)):
            data = bytes(body)
        else:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = content_type
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return ApiResult(resp.status, dict(resp.headers), resp.read(),
                             int((time.monotonic() - t0) * 1000))
    except urllib.error.HTTPError as e:
        return ApiResult(e.code, dict(e.headers or {}), e.read(),
                         int((time.monotonic() - t0) * 1000))
    except urllib.error.URLError as e:
        err(f"Network error calling {method} {url}: {e.reason}\n"
            f"(Behind a proxy? urllib honours HTTPS_PROXY. SSL errors on macOS python.org builds: "
            f"run 'Install Certificates.command', or use the curl equivalent from the reference.)")
        sys.exit(EXIT_API_ERROR)
    except (TimeoutError, OSError) as e:  # read timeouts aren't wrapped in URLError
        err(f"{method} {url} failed after {int((time.monotonic() - t0) * 1000)} ms: {e or 'timed out'} "
            f"(timeout {timeout} s). For sends, retry with the same --retry-key so nothing is duplicated.")
        sys.exit(EXIT_API_ERROR)


HINTS = {
    400: "Bad request - read 'message'/'details' below; for message bodies run the validate command.",
    401: "Unauthorized - token missing/invalid/expired/revoked, or it belongs to a different channel.",
    403: "Forbidden - this account/plan can't use this endpoint (some need a verified/premium account or a special agreement).",
    404: "Not found - wrong ID, or the user/group isn't reachable by this bot (blocked, left, different provider).",
    409: "Conflict - a request with this X-Line-Retry-Key was already accepted (not sent twice).",
    410: "Gone - the content has expired on the LINE Platform.",
    413: "Payload too large.",
    415: "Unsupported media type - rich menu images must be image/png or image/jpeg.",
    429: "Too many requests - rate limit or the monthly message quota is exhausted ('You have reached your monthly limit.').",
}


def report(res, label=None, print_body=True):
    """Print a result. Returns exit code."""
    if res.ok:
        if print_body:
            data = res.json()
            out(data if data else {"status": res.status, "result": "ok (empty body)"})
        return EXIT_OK
    err(f"HTTP {res.status}{' on ' + label if label else ''}"
        f"  x-line-request-id={res.request_id or '-'}")
    hint = HINTS.get(res.status) or ("LINE Platform error - retry later; check https://api.line-status.info/"
                                     if res.status >= 500 else None)
    if hint:
        err("hint: " + hint)
    err(json.dumps(res.json(), ensure_ascii=False, indent=2))
    err(f"reference: {REF}#status-codes")
    return EXIT_API_ERROR


def path_seg(value):
    return urllib.parse.quote(str(value), safe="")


# --------------------------------------------------------------------------- inputs

def read_json_arg(value):
    """value is a path, '-' for stdin, or an inline JSON string."""
    if value == "-":
        text = sys.stdin.read()
    elif value.lstrip().startswith(("{", "[")):
        text = value
    else:
        p = Path(value)
        if not p.is_file():
            err(f"File not found: {value}")
            sys.exit(EXIT_USAGE)
        text = p.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON in {value if value != '-' else 'stdin'}: {e}")
        sys.exit(EXIT_USAGE)


def load_messages(args):
    """Accepts --text, or a file with a message object, a list of them, or {"messages": [...]}"""
    if getattr(args, "text", None):
        msgs = [{"type": "text", "text": args.text}]
    elif getattr(args, "file", None):
        data = read_json_arg(args.file)
        if isinstance(data, dict) and "messages" in data:
            msgs = data["messages"]
        elif isinstance(data, dict):
            msgs = [data]
        elif isinstance(data, list):
            msgs = data
        else:
            err("Message file must contain a message object, a list, or {\"messages\": [...]}")
            sys.exit(EXIT_USAGE)
    else:
        err("Give a message file (or '-' for stdin) or --text.")
        sys.exit(EXIT_USAGE)
    if not msgs:
        err("No messages to send.")
        sys.exit(EXIT_USAGE)
    if len(msgs) > MAX_MESSAGES_PER_REQUEST:
        err(f"{len(msgs)} message objects given; one request takes at most {MAX_MESSAGES_PER_REQUEST} "
            f"({REF}#send-push-message). Split them into several requests.")
        sys.exit(EXIT_USAGE)
    for i, m in enumerate(msgs):
        if not isinstance(m, dict) or "type" not in m:
            err(f"messages[{i}] is not a message object (missing 'type').")
            sys.exit(EXIT_USAGE)
        if m.get("type") in ("flex", "template", "imagemap") and not m.get("altText"):
            err(f"messages[{i}] ({m['type']}) has no altText - it is required and is what shows in "
                f"notifications and the chat list.")
            sys.exit(EXIT_USAGE)
    return msgs


def recipient_kind(to):
    return {"U": "user", "C": "group", "R": "room"}.get(str(to)[:1], "unknown")


# --------------------------------------------------------------------------- dry run

def print_plan(method, url, body=None, headers=None, notes=None, binary_desc=None):
    print("DRY RUN - nothing was sent or changed. Show this to the user; after they confirm, "
          "re-run the same command with --yes.")
    print(f"{method} {url}")
    for k, v in (headers or {}).items():
        print(f"{k}: {v}")
    if binary_desc:
        print(f"Body: {binary_desc}")
    elif body is not None:
        text = json.dumps(body, ensure_ascii=False, indent=2)
        if len(text) > 6000:
            text = text[:6000] + f"\n... ({len(text)} chars total, truncated)"
        print("Body:")
        print(text)
    for n in notes or []:
        print(f"note: {n}")


def quota_note(token, timeout):
    q = request("GET", f"{API}/v2/bot/message/quota", token, timeout=timeout)
    c = request("GET", f"{API}/v2/bot/message/quota/consumption", token, timeout=timeout)
    if not (q.ok and c.ok):
        return "could not read quota (see `quota` command)."
    qd, cd = q.json(), c.json()
    used = cd.get("totalUsage")
    if qd.get("type") == "limited":
        limit = qd.get("value")
        left = (limit - used) if isinstance(limit, int) and isinstance(used, int) else "?"
        return f"monthly message quota: {used}/{limit} used, {left} left."
    return f"monthly message quota: type={qd.get('type')} (no fixed cap), {used} used this month."


def validate_messages(kind, msgs, token, timeout):
    res = request("POST", f"{API}/v2/bot/message/validate/{kind}", token,
                  body={"messages": msgs}, timeout=timeout)
    if res.ok:
        print(f"validate/{kind}: OK (the API accepted the message objects)")
        return True
    report(res, label=f"validate/{kind}")
    return False


# --------------------------------------------------------------------------- send commands

def send_with_retry(url, token, body, retry_key, retries, timeout):
    attempt = 0
    while True:
        res = request("POST", url, token, body=body,
                      extra_headers={"X-Line-Retry-Key": retry_key}, timeout=timeout)
        if res.status == 409:
            accepted = res.headers.get("x-line-accepted-request-id")
            print(f"Already accepted earlier with this retry key (accepted request id: {accepted}). "
                  f"Not sent again.")
            return EXIT_OK
        if res.ok or attempt >= retries or not (res.status >= 500 or res.status == 429):
            break
        attempt += 1
        wait = 2 ** attempt
        err(f"HTTP {res.status}; retrying in {wait}s with the same X-Line-Retry-Key ({attempt}/{retries})")
        time.sleep(wait)
    code = report(res, label=url)
    if res.ok:
        print(f"x-line-request-id: {res.request_id}  retry-key: {retry_key}")
    return code


def cmd_send(args, kind):
    token = get_token(args, required=bool(args.yes))
    msgs = load_messages(args)
    url = f"{API}/v2/bot/message/{kind}"
    if kind == "push":
        body = {"to": args.to, "messages": msgs}
    elif kind == "multicast":
        ids = parse_ids(args.to)
        if len(ids) > MAX_MULTICAST_RECIPIENTS:
            err(f"{len(ids)} recipients; multicast takes at most {MAX_MULTICAST_RECIPIENTS} per request.")
            return EXIT_USAGE
        bad = [i for i in ids if recipient_kind(i) != "user"]
        if bad:
            err(f"multicast only accepts user IDs (U...), not groups/rooms: {bad[:5]}")
            return EXIT_USAGE
        body = {"to": ids, "messages": msgs}
    else:  # broadcast
        body = {"messages": msgs}
    if getattr(args, "notification_disabled", False):
        body["notificationDisabled"] = True

    notes = []
    if kind == "push":
        rk = recipient_kind(args.to)
        notes.append(f"recipient type: {rk}")
        if rk in ("group", "room") and token:
            cnt = request("GET", f"{API}/v2/bot/{rk}/{path_seg(args.to)}/members/count", token,
                          timeout=args.timeout)
            if cnt.ok:
                notes.append(f"a push to this {rk} counts once per member against the monthly quota; "
                             f"it currently has {cnt.json().get('count')} members.")
        if rk == "unknown":
            notes.append("'to' doesn't look like a LINE ID (U... user, C... group, R... room). "
                         "Display names and LINE IDs (@xxx) don't work here.")
    elif kind == "multicast":
        notes.append(f"{len(body['to'])} recipients; counts once per recipient who receives it.")
    else:
        notes.append("broadcast goes to EVERY friend of this account and counts once per recipient.")
    if token:
        notes.append(quota_note(token, args.timeout))
    else:
        notes.append("no token in this environment: skipped validation and quota check.")

    if not args.yes:
        if token and not args.no_validate and not validate_messages(kind, msgs, token, args.timeout):
            return EXIT_API_ERROR
        print_plan("POST", url, body,
                   headers={"Authorization": "Bearer <redacted>",
                            "X-Line-Retry-Key": "<new UUID per logical send; reuse it on retries>"},
                   notes=notes)
        return EXIT_OK

    if not args.no_validate and not validate_messages(kind, msgs, token, args.timeout):
        return EXIT_API_ERROR
    retry_key = args.retry_key or str(uuid.uuid4())
    return send_with_retry(url, token, body, retry_key, args.retries, args.timeout)


def parse_ids(value):
    if value.startswith("@"):
        text = Path(value[1:]).read_text(encoding="utf-8")
        ids = [ln.strip() for ln in text.splitlines() if ln.strip()]
    else:
        ids = [v.strip() for v in value.split(",") if v.strip()]
    return ids


def cmd_validate(args):
    token = get_token(args)
    msgs = load_messages(args)
    return EXIT_OK if validate_messages(args.kind, msgs, token, args.timeout) else EXIT_API_ERROR


# --------------------------------------------------------------------------- simple GETs

def simple_get(args, url, label=None):
    token = get_token(args)
    return report(request("GET", url, token, timeout=args.timeout), label=label)


def cmd_quota(args):
    token = get_token(args)
    q = request("GET", f"{API}/v2/bot/message/quota", token, timeout=args.timeout)
    if not q.ok:
        return report(q, "quota")
    c = request("GET", f"{API}/v2/bot/message/quota/consumption", token, timeout=args.timeout)
    if not c.ok:
        return report(c, "quota/consumption")
    result = {"quota": q.json(), "consumption": c.json(),
              "note": "Only push/multicast/broadcast/narrowcast count; reply messages are free. "
                      "Counted per recipient (a push to a group of N members counts N)."}
    out(result)
    return EXIT_OK


def cmd_content(args):
    token = get_token(args)
    res = request("GET", f"{API_DATA}/v2/bot/message/{path_seg(args.message_id)}/content", token,
                  timeout=max(args.timeout, 60))
    if res.status == 202:
        print("202 Accepted: the video/audio is still being prepared. Retry later or poll "
              f"`call GET {API_DATA}/v2/bot/message/{args.message_id}/content/transcoding`.")
        return EXIT_OK
    if not res.ok:
        return report(res, "content")
    ctype = res.headers.get("content-type", "application/octet-stream").split(";")[0]
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif", "video/mp4": ".mp4",
           "audio/x-m4a": ".m4a", "audio/mp4": ".m4a", "application/pdf": ".pdf"}.get(ctype, ".bin")
    target = Path(args.output) if args.output else Path(f"{args.message_id}{ext}")
    target.write_bytes(res.body)
    out({"saved": str(target), "bytes": len(res.body), "content_type": ctype})
    return EXIT_OK


# --------------------------------------------------------------------------- webhook

def cmd_webhook_test(args):
    token = get_token(args)
    body = {"endpoint": args.url} if args.url else {}
    res = request("POST", f"{API}/v2/bot/channel/webhook/test", token, body=body, timeout=args.timeout)
    code = report(res, "webhook/test")
    if res.ok:
        d = res.json()
        if not d.get("success"):
            err("The LINE Platform could not get a 2xx from your endpoint. Check: HTTPS with a valid "
                "certificate chain, the server responds within 2 seconds, signature verification uses "
                "the raw body and THIS channel's secret, and no auth layer (e.g. a platform JWT check) "
                "rejects LINE's request before your code runs.")
    print("note: this endpoint is rate limited to 60 requests/hour.")
    return code


def cmd_webhook_set(args):
    url = f"{API}/v2/bot/channel/webhook/endpoint"
    body = {"endpoint": args.url}
    if not args.url.startswith("https://"):
        err("The webhook URL must be HTTPS (max 500 characters).")
        return EXIT_USAGE
    if not args.yes:
        token = get_token(args, required=False)
        notes = ["changes where LINE delivers ALL events for this channel; may take up to 1 minute to apply."]
        if token:
            cur = request("GET", url, token, timeout=args.timeout)
            if cur.ok:
                notes.insert(0, f"current endpoint: {cur.json().get('endpoint')} "
                                f"(active={cur.json().get('active')})")
        print_plan("PUT", url, body, headers={"Authorization": "Bearer <redacted>"}, notes=notes)
        return EXIT_OK
    token = get_token(args)
    code = report(request("PUT", url, token, body=body, timeout=args.timeout), "webhook/endpoint")
    if code == EXIT_OK:
        print("Set. Also make sure 'Use webhook' is enabled in the console's Messaging API tab, then run "
              "`webhook-test`.")
    return code


# --------------------------------------------------------------------------- rich menu

def image_info(path):
    """Return (format, width, height) for PNG/JPEG using only the stdlib."""
    data = Path(path).read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return "png", w, h
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7 or marker == 0x01:
                i += 2
                continue
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return "jpeg", w, h
            i += 2 + seg_len
        return "jpeg", None, None
    return "unknown", None, None


def check_richmenu_local(menu, image_path=None):
    """Pre-flight checks mirroring REF#rich-menu-object and #upload-rich-menu-image-requirements.
    Returns (errors, warnings)."""
    errors, warnings = [], []
    size = menu.get("size") or {}
    w, h = size.get("width"), size.get("height")
    if not isinstance(w, int) or not isinstance(h, int):
        errors.append("size.width and size.height are required integers.")
    else:
        if not 800 <= w <= 2500:
            errors.append(f"size.width {w} must be 800-2500.")
        if h < 250:
            errors.append(f"size.height {h} must be >= 250.")
        if h and w / h < 1.45:
            errors.append(f"aspect ratio width/height = {w / h:.3f} must be >= 1.45.")
    for key in ("selected", "name", "chatBarText", "areas"):
        if key not in menu:
            errors.append(f"'{key}' is required.")
    cbt = menu.get("chatBarText", "")
    if isinstance(cbt, str) and len(cbt) > 14:
        errors.append(f"chatBarText is {len(cbt)} characters; max 14.")
    name = menu.get("name", "")
    if isinstance(name, str) and len(name) > 300:
        errors.append(f"name is {len(name)} characters; max 300.")
    areas = menu.get("areas") or []
    if len(areas) > 20:
        errors.append(f"{len(areas)} areas; max 20.")
    rects = []
    for i, a in enumerate(areas):
        b = a.get("bounds") or {}
        x, y, bw, bh = b.get("x", 0), b.get("y", 0), b.get("width", 0), b.get("height", 0)
        if x < 0 or y < 0:
            errors.append(f"areas[{i}] bounds x/y must be >= 0 (got {x},{y}).")
        elif isinstance(w, int) and isinstance(h, int) and (x + bw > w or y + bh > h):
            # The reference only requires x, y >= 0, so LINE may accept this - but the part outside the menu
            # can't be tapped and it's almost always a typo in the layout.
            warnings.append(f"areas[{i}] bounds ({x},{y},{bw}x{bh}) extend past the {w}x{h} menu "
                            f"(x+width={x + bw}, y+height={y + bh}); that part can't be tapped - probably a typo.")
        for j, (rx, ry, rw, rh) in enumerate(rects):
            if x < rx + rw and rx < x + bw and y < ry + rh and ry < y + bh:
                warnings.append(f"areas[{i}] overlaps areas[{j}] - a tap there is ambiguous.")
        rects.append((x, y, bw, bh))
        if "action" not in a:
            errors.append(f"areas[{i}] has no action.")
    if image_path:
        p = Path(image_path)
        if not p.is_file():
            errors.append(f"image not found: {image_path}")
        else:
            fmt, iw, ih = image_info(p)
            nbytes = p.stat().st_size
            if fmt not in ("png", "jpeg"):
                errors.append("image must be PNG or JPEG.")
            if nbytes > RICHMENU_MAX_IMAGE_BYTES:
                errors.append(f"image is {nbytes / 1024:.0f} KB; max 1 MB. Compress it "
                              f"(e.g. pngquant, or export as JPEG).")
            if iw and ih:
                if not 800 <= iw <= 2500 or ih < 250 or iw / ih < 1.45:
                    errors.append(f"image {iw}x{ih} breaks the image requirements "
                                  f"(width 800-2500, height >= 250, width/height >= 1.45).")
                if isinstance(w, int) and isinstance(h, int) and (iw, ih) != (w, h):
                    warnings.append(f"image is {iw}x{ih} but size is {w}x{h}; tap areas are defined "
                                    f"in size coordinates, so make them match.")
    return errors, warnings


def cmd_richmenu_validate(args):
    menu = read_json_arg(args.file)
    errors, warnings = check_richmenu_local(menu, args.image)
    for wmsg in warnings:
        print(f"warning: {wmsg}")
    for e in errors:
        print(f"error: {e}")
    token = get_token(args, required=False)
    if token:
        res = request("POST", f"{API}/v2/bot/richmenu/validate", token, body=menu, timeout=args.timeout)
        if res.ok:
            print("richmenu/validate: OK (the API accepted the rich menu object)")
        else:
            report(res, "richmenu/validate")
            return EXIT_API_ERROR
    else:
        print("no token: ran local checks only (set LINE_CHANNEL_ACCESS_TOKEN for the API validation).")
    return EXIT_USAGE if errors else EXIT_OK


def upload_image(token, rich_menu_id, image_path, timeout):
    fmt, _, _ = image_info(image_path)
    ctype = "image/png" if fmt == "png" else "image/jpeg"
    return request("POST", f"{API_DATA}/v2/bot/richmenu/{path_seg(rich_menu_id)}/content", token,
                   body=Path(image_path).read_bytes(), content_type=ctype, timeout=max(timeout, 60))


def cmd_richmenu_deploy(args):
    """validate -> create -> upload image -> (optional) set as default / create alias."""
    menu = read_json_arg(args.file)
    errors, warnings = check_richmenu_local(menu, args.image)
    for wmsg in warnings:
        print(f"warning: {wmsg}")
    if errors:
        for e in errors:
            print(f"error: {e}")
        return EXIT_USAGE
    token = get_token(args, required=bool(args.yes))
    if token:
        res = request("POST", f"{API}/v2/bot/richmenu/validate", token, body=menu, timeout=args.timeout)
        if not res.ok:
            return report(res, "richmenu/validate")
        print("richmenu/validate: OK")
    steps = [f"POST {API}/v2/bot/richmenu  (create; returns richMenuId)",
             f"POST {API_DATA}/v2/bot/richmenu/{{richMenuId}}/content  (upload {args.image})"]
    if args.alias:
        steps.append(f"POST {API}/v2/bot/richmenu/alias  (aliasId={args.alias})")
    if args.default:
        steps.append(f"POST {API}/v2/bot/user/all/richmenu/{{richMenuId}}  (default for ALL users)")
    if not args.yes:
        print("DRY RUN - nothing was created. Show this to the user; after they confirm, "
              "re-run with --yes.")
        for s in steps:
            print("  " + s)
        if args.default and token:
            cur = request("GET", f"{API}/v2/bot/user/all/richmenu", token, timeout=args.timeout)
            if cur.ok:
                print(f"note: current default rich menu: {cur.json().get('richMenuId')} "
                      f"(it stays on the account; delete it later if unused)")
            elif cur.status == 404:
                print("note: no default rich menu is set right now.")
        print("note: per-user linked menus override the default; a rich menu image can't be replaced "
              "later - to change the picture, deploy a new menu.")
        return EXIT_OK
    res = request("POST", f"{API}/v2/bot/richmenu", token, body=menu, timeout=args.timeout)
    if not res.ok:
        return report(res, "richmenu create")
    rid = res.json().get("richMenuId")
    print(f"created richMenuId={rid}")
    up = upload_image(token, rid, args.image, args.timeout)
    if not up.ok:
        report(up, "richmenu image upload")
        err(f"The menu {rid} exists without an image (unusable). Delete it with: "
            f"richmenu-delete {rid} --yes")
        return EXIT_API_ERROR
    print("image uploaded")
    if args.alias:
        al = request("POST", f"{API}/v2/bot/richmenu/alias", token,
                     body={"richMenuAliasId": args.alias, "richMenuId": rid}, timeout=args.timeout)
        if not al.ok:
            report(al, "richmenu alias")
            err("If the alias already exists, update it instead: "
                f"call POST /v2/bot/richmenu/alias/{args.alias} --data '{{\"richMenuId\":\"{rid}\"}}' --yes")
            return EXIT_API_ERROR
        print(f"alias {args.alias} -> {rid}")
    if args.default:
        d = request("POST", f"{API}/v2/bot/user/all/richmenu/{path_seg(rid)}", token,
                    timeout=args.timeout)
        if not d.ok:
            return report(d, "set default rich menu")
        print("set as default rich menu for all users (clients may take a moment to refresh; "
              "users with a per-user menu keep theirs)")
    out({"richMenuId": rid})
    return EXIT_OK


def guarded(args, method, url, body=None, label=None, notes=None, binary=None):
    """Run a state-changing request only with --yes; otherwise print the plan."""
    if not args.yes:
        print_plan(method, url, body, headers={"Authorization": "Bearer <redacted>"},
                   notes=notes, binary_desc=binary)
        return EXIT_OK
    token = get_token(args)
    return report(request(method, url, token, body=body, timeout=args.timeout), label)


def cmd_richmenu_upload(args):
    fmt, iw, ih = image_info(args.image)
    desc = f"{args.image} ({fmt}, {iw}x{ih}, {Path(args.image).stat().st_size} bytes)"
    if not args.yes:
        print_plan("POST", f"{API_DATA}/v2/bot/richmenu/{args.rich_menu_id}/content",
                   headers={"Authorization": "Bearer <redacted>"}, binary_desc=desc,
                   notes=["an image can be set only once per rich menu."])
        return EXIT_OK
    token = get_token(args)
    return report(upload_image(token, args.rich_menu_id, args.image, args.timeout), "richmenu upload")


# --------------------------------------------------------------------------- generic call

WRITE_METHODS = {"POST", "PUT", "DELETE", "PATCH"}
# POSTs that change nothing: validation endpoints, and the webhook test (sends a test event to your server).
READONLY_POSTS = ("/v2/bot/message/validate/", "/v2/bot/richmenu/validate", "/v2/bot/channel/webhook/test")


def cmd_call(args):
    method = args.method.upper()
    target = args.path
    if not target.startswith("http"):
        host = API_DATA if args.data_host else API
        target = host + (target if target.startswith("/") else "/" + target)
    host = urllib.parse.urlparse(target).hostname or ""
    if host not in ("api.line.me", "api-data.line.me"):
        err("call only talks to api.line.me / api-data.line.me (the token must not go anywhere else).")
        return EXIT_USAGE
    body = read_json_arg(args.data) if args.data else None
    path = urllib.parse.urlparse(target).path
    is_write = method in WRITE_METHODS and not path.startswith(READONLY_POSTS)
    if is_write and not args.yes:
        print_plan(method, target, body, headers={"Authorization": "Bearer <redacted>"},
                   notes=["state-changing call; confirm with the user first."])
        return EXIT_OK
    token = get_token(args)
    extra = {"X-Line-Retry-Key": args.retry_key} if args.retry_key else None
    res = request(method, target, token, body=body, extra_headers=extra, timeout=args.timeout)
    code = report(res, f"{method} {path}")
    if args.verbose:
        err(f"x-line-request-id={res.request_id} elapsed={res.elapsed_ms}ms")
    return code


# --------------------------------------------------------------------------- argparse

def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--env-file", default=argparse.SUPPRESS,
                        help="load KEY=VALUE pairs (e.g. your bot's .env) before reading the token")
    common.add_argument("--token-env", default=argparse.SUPPRESS,
                        help="env var holding the channel access token (default LINE_CHANNEL_ACCESS_TOKEN)")
    common.add_argument("--timeout", type=int, default=argparse.SUPPRESS, help="HTTP timeout seconds (30)")
    common.add_argument("--verbose", action="store_true", default=argparse.SUPPRESS)

    write = argparse.ArgumentParser(add_help=False)
    write.add_argument("--yes", action="store_true", default=argparse.SUPPRESS,
                       help="actually perform the change (otherwise: dry run)")

    msg = argparse.ArgumentParser(add_help=False)
    msg.add_argument("file", nargs="?", help="JSON file with message object(s), or '-' for stdin")
    msg.add_argument("--text", help="send a plain text message instead of a file")

    p = argparse.ArgumentParser(
        prog="line_api.py", parents=[common],
        description="LINE Messaging API helper. Write commands are dry runs unless --yes is given.")
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND")

    def add(name, help_, parents=(), **kw):
        return sub.add_parser(name, help=help_, parents=[common, *parents], **kw)

    add("info", "bot info: userId, basicId, displayName, chatMode (GET /v2/bot/info)")
    add("quota", "monthly message quota and usage")
    add("webhook-info", "current webhook URL and whether it is active")
    s = add("webhook-test", "ask LINE to send a test webhook to the configured (or given) URL")
    s.add_argument("--url")
    s = add("webhook-set", "set the webhook URL [write]", parents=[write])
    s.add_argument("url")

    s = add("validate", "validate message objects without sending (free, nothing is delivered)")
    s.add_argument("kind", choices=["reply", "push", "multicast", "narrowcast", "broadcast"])
    s.add_argument("file", nargs="?", help="JSON file with message object(s), or '-' for stdin")
    s.add_argument("--text", help="validate a plain text message instead of a file")

    for name, help_ in (("push", "send a push message to a user/group/room ID [write, counts quota]"),
                        ("multicast", "send to up to 500 user IDs [write, counts quota]"),
                        ("broadcast", "send to ALL friends [write, counts quota]")):
        s = add(name, help_, parents=[write, msg])
        if name != "broadcast":
            s.add_argument("--to", required=True,
                           help="recipient ID (push) or comma-separated IDs / @file (multicast)")
        s.add_argument("--no-validate", action="store_true", help="skip the validate call")
        s.add_argument("--notification-disabled", action="store_true", help="deliver silently")
        s.add_argument("--retry-key", help="reuse a specific X-Line-Retry-Key (UUID)")
        s.add_argument("--retries", type=int, default=2, help="retries on 5xx/429 with the same key")

    s = add("profile", "profile of a user who is a friend / messaged the bot")
    s.add_argument("user_id")
    for name, help_ in (("group-summary", "group name and icon"),
                        ("group-count", "number of members in a group")):
        s = add(name, help_)
        s.add_argument("group_id")
    s = add("group-member", "profile of a member of a group the bot is in")
    s.add_argument("group_id")
    s.add_argument("user_id")
    s = add("group-leave", "make the bot leave a group [write]", parents=[write])
    s.add_argument("group_id")
    s = add("content", "download an image/video/audio/file a user sent")
    s.add_argument("message_id")
    s.add_argument("-o", "--output")

    add("richmenu-list", "list rich menus on this channel")
    add("richmenu-default", "show the default rich menu ID")
    s = add("richmenu-get", "get one rich menu")
    s.add_argument("rich_menu_id")
    s = add("richmenu-validate", "local pre-flight checks + API validation of a rich menu JSON")
    s.add_argument("file")
    s.add_argument("--image", help="also check the image file against the requirements")
    s = add("richmenu-deploy", "validate, create, upload image, optionally alias/default [write]",
            parents=[write])
    s.add_argument("file")
    s.add_argument("image")
    s.add_argument("--default", action="store_true", help="set as default menu for all users")
    s.add_argument("--alias", help="create a rich menu alias (for tab switching)")
    s = add("richmenu-upload", "upload an image to an existing rich menu [write]", parents=[write])
    s.add_argument("rich_menu_id")
    s.add_argument("image")
    s = add("richmenu-set-default", "set default rich menu for all users [write]", parents=[write])
    s.add_argument("rich_menu_id")
    s = add("richmenu-link", "link a rich menu to one user [write]", parents=[write])
    s.add_argument("user_id")
    s.add_argument("rich_menu_id")
    s = add("richmenu-unlink", "unlink the per-user rich menu [write]", parents=[write])
    s.add_argument("user_id")
    s = add("richmenu-delete", "delete a rich menu [write]", parents=[write])
    s.add_argument("rich_menu_id")

    s = add("call", "any endpoint: call METHOD PATH [--data JSON|file] (writes need --yes)",
            parents=[write])
    s.add_argument("method")
    s.add_argument("path", help="/v2/bot/... or a full https://api(-data).line.me URL")
    s.add_argument("--data", help="JSON body: inline JSON, a file path, or '-' for stdin")
    s.add_argument("--data-host", action="store_true", help="use api-data.line.me for a bare path")
    s.add_argument("--retry-key")
    return p


def main(argv=None):
    _setup_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return EXIT_USAGE
    # defaults for SUPPRESS'ed common options
    for k, v in (("env_file", None), ("token_env", None), ("timeout", 30), ("verbose", False),
                 ("yes", False)):
        if not hasattr(args, k):
            setattr(args, k, v)
    if args.env_file:
        load_env_file(args.env_file)

    c = args.cmd
    if c == "info":
        return simple_get(args, f"{API}/v2/bot/info", "info")
    if c == "quota":
        return cmd_quota(args)
    if c == "webhook-info":
        return simple_get(args, f"{API}/v2/bot/channel/webhook/endpoint", "webhook/endpoint")
    if c == "webhook-test":
        return cmd_webhook_test(args)
    if c == "webhook-set":
        return cmd_webhook_set(args)
    if c == "validate":
        return cmd_validate(args)
    if c in ("push", "multicast", "broadcast"):
        return cmd_send(args, c)
    if c == "profile":
        return simple_get(args, f"{API}/v2/bot/profile/{path_seg(args.user_id)}", "profile")
    if c == "group-summary":
        return simple_get(args, f"{API}/v2/bot/group/{path_seg(args.group_id)}/summary", "group summary")
    if c == "group-count":
        return simple_get(args, f"{API}/v2/bot/group/{path_seg(args.group_id)}/members/count",
                          "group members count")
    if c == "group-member":
        return simple_get(args, f"{API}/v2/bot/group/{path_seg(args.group_id)}/member/"
                                f"{path_seg(args.user_id)}", "group member profile")
    if c == "group-leave":
        return guarded(args, "POST", f"{API}/v2/bot/group/{path_seg(args.group_id)}/leave",
                       label="leave group", notes=["the bot leaves the group; re-adding needs a member to invite it."])
    if c == "content":
        return cmd_content(args)
    if c == "richmenu-list":
        return simple_get(args, f"{API}/v2/bot/richmenu/list", "richmenu list")
    if c == "richmenu-default":
        return simple_get(args, f"{API}/v2/bot/user/all/richmenu", "default richmenu")
    if c == "richmenu-get":
        return simple_get(args, f"{API}/v2/bot/richmenu/{path_seg(args.rich_menu_id)}", "richmenu get")
    if c == "richmenu-validate":
        return cmd_richmenu_validate(args)
    if c == "richmenu-deploy":
        return cmd_richmenu_deploy(args)
    if c == "richmenu-upload":
        return cmd_richmenu_upload(args)
    if c == "richmenu-set-default":
        return guarded(args, "POST", f"{API}/v2/bot/user/all/richmenu/{path_seg(args.rich_menu_id)}",
                       label="set default richmenu",
                       notes=["applies to every user without a per-user menu."])
    if c == "richmenu-link":
        return guarded(args, "POST", f"{API}/v2/bot/user/{path_seg(args.user_id)}/richmenu/"
                                     f"{path_seg(args.rich_menu_id)}", label="link richmenu")
    if c == "richmenu-unlink":
        return guarded(args, "DELETE", f"{API}/v2/bot/user/{path_seg(args.user_id)}/richmenu",
                       label="unlink richmenu")
    if c == "richmenu-delete":
        return guarded(args, "DELETE", f"{API}/v2/bot/richmenu/{path_seg(args.rich_menu_id)}",
                       label="delete richmenu",
                       notes=["users linked to this menu (or using it as default) lose it."])
    if c == "call":
        return cmd_call(args)
    parser.print_help()
    return EXIT_USAGE


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # output piped into `head` etc.
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        sys.exit(0)
