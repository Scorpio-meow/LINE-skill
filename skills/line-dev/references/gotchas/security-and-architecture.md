# Gotchas: tokens and security, architecture patterns, testing

Field-tested patterns from production LINE bots, checked against the official docs. Paths are relative to
`https://developers.line.biz/en/`. Numbers marked "(at the time of writing)" were checked in 2026-10.

## Contents
1. Tokens, channels, providers, security
2. Architecture patterns (incl. LLM bots)
3. Testing toolkit

## 1. Tokens, channels, providers, security

- Three different credentials: Messaging API **channel secret** (webhook signatures), Messaging API **channel
  access token** (API calls), LINE Login **channel ID** (ID-token `aud`). Keep them as separately named
  server-side secrets.
- **Keep tokens off command lines and out of chat.** Don't `source .env` into a shell or paste
  `-H "Authorization: Bearer $TOKEN"`-expanded values into commands that land in shell history, process lists
  or logs; read the token inside a program (`line_api.py --env-file .env`) or from the platform's secret
  store. Never print it, commit it, or echo it back to the user.
- Token types differ in lifetime and count (long-lived: one per channel, **reissuing invalidates the current
  one** - which breaks a live bot still using it - though the console can extend the old one by up to 24 h;
  stateless: short-lived, unlimited, not revocable; v2.1 JWT: chosen expiry).
  Re-check: `docs/basics/channel-access-token/`.
- 401 from the API = invalid/expired/revoked token or another channel's token - don't retry; check which
  channel the token belongs to (`GET /v2/bot/info` shows the bot). If the user's bot is live and working,
  the fix is usually to copy the token it already uses, not to reissue.
- **Never put long-lived secrets in message links** (Flex button URLs are visible to everyone in the chat,
  can be forwarded, and live forever in history). Use short-lived signed URLs for one resource, or route
  through LIFF with an ID token.
- userIds are personal data: don't print them in logs or scripts; keep service-account JSON and `.env`
  files out of git; compare internal shared secrets in constant time; use a CSPRNG for codes/tokens.
- Put the bot, LIFF and Login channels under one provider (`liff-and-login.md`).
- LINE Notify is discontinued; notifications go through a Messaging API bot. Check `news/tags/end-of-life/`
  before recommending any older feature.

## 2. Architecture patterns (incl. LLM bots)

- **Webhook pipeline:** verify -> durable, deduplicated insert -> 200 -> background worker per chat -> one
  outbound function (reply first). Keep a trace per event (event -> decision -> reply/push, with
  `x-line-request-id`) - it's the main debugging tool, and LINE support asks for request IDs.
  Re-check: `docs/messaging-api/development-guidelines/#messaging-api-logs`.
- **LLM in the loop:** the model classifies/extracts into structured output; your code enforces rules,
  permissions and recipients and builds every LINE message. Pre-filter greetings/stickers before the model
  (keep acknowledgements). Give it per-chat context limited in time and size - never other groups' history.
  Message text is untrusted input (prompt injection): it must never choose recipients or call the API. Escape
  model output that goes into textV2.
- **Bursts:** people send several short messages; store them and let a frequent job merge a sender's burst into
  one decision once they go quiet, sized to fit the reply-token window.
- **Missing information** becomes a quiet draft for a human to complete, not an invented item.
- **Alerts into groups** (monitoring -> LINE): authenticate the source with its own HMAC, one card per incident
  (dedupe by incident key, cooldown re-fires only update your timeline), acknowledge via a postback answered by
  reply (free), escalate with a textV2 mention after N minutes, fold downstream symptoms into the upstream card.
- **1:1 LLM bots:** map userId -> conversation session with a reset command, show the loading animation, keep
  each user's messages in order, and keep a push path for results/errors once the reply token is gone.
- **Privacy:** honour unsend, minimise stored profile data, don't infer user attributes (prohibited by the
  development guidelines).

## 3. Testing toolkit

For your own verification (run these yourself and report the results):
- `scripts/webhook_tools.py selftest <url>` - Verify ping, valid event, wrong and missing signature, timing.
- `scripts/webhook_tools.py simulate <url> <type> [--source group]` - one signed event of a common type.
- `scripts/webhook_tools.py sample <type>` - realistic payloads; in unit tests **sign fixtures** with a test
  secret instead of disabling verification. Fixtures worth having: `events: []`, a redelivered duplicate, a body
  with CJK/emoji and escapes, mentions with `isSelf` and `type: "all"`, stickers, unsend,
  memberJoined/memberLeft, join/leave, postback, video (202 then 200), file with `fileSize`.
- `scripts/line_api.py webhook-test` - LINE itself calls the configured URL (60/hour at the time of writing).
- `scripts/line_api.py validate ...` / `richmenu-validate ...` - catch bad JSON without sending (good in CI).

For the user to run on their own machine, give self-contained commands instead of the skill's scripts (they
may not have them):
```bash
BODY='{"destination":"Uxxxxxxxx","events":[]}'
SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$LINE_CHANNEL_SECRET" -binary | openssl base64)
curl -i -X POST "$WEBHOOK_URL" -H 'Content-Type: application/json' -H "x-line-signature: $SIG" --data-raw "$BODY"
```
(`$LINE_CHANNEL_SECRET` read from their environment; tell them to expect 200, and a 401/403 body that tells
which layer refused.)

Also: console > Messaging API tab > webhook error statistics; platform incidents at
`https://api.line-status.info/`.
