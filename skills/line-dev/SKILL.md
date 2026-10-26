---
name: line-dev
description: Build, review, debug and operate LINE (LY Corporation) bots and apps - Messaging API webhooks, reply/push messages, Flex Messages, rich menus (圖文選單), group-chat bots, LIFF apps and LINE Login - and call the LINE API directly (send a test message, deploy a rich menu, check the monthly quota, set or test the webhook URL). Use this skill whenever the user mentions a LINE Bot, LINE 官方帳號 / LINE Official Account / LINE公式アカウント, channel access token or channel secret, x-line-signature, reply token, push quota, Flex Message, rich menu, LIFF, LINE Login, the LINE Developers Console, a LINE Developers notice email (e.g. "update the LIFF SDK"), migrating off LINE Notify, or a bot in LINE groups (LINE 群組機器人) - even when it looks like a generic webhook, Node, Python or serverless question. Also use it for any question about LINE API limits, pricing or message counting, error codes or event behaviour, because those change often and must be checked against the live official docs.
license: MIT
compatibility: Scripts need Python 3.8+ (standard library only; git optional for full-text doc search). Doc lookups need web access to raw.githubusercontent.com, github.com (git) or developers.line.biz; API operations need access to api.line.me and a channel access token.
---

# LINE platform development

| Request | What to do | Read |
|---|---|---|
| Build, review or debug LINE code | Fix what was asked with the smallest change; use the field-tested failure modes; test without the LINE app | the matching file in `references/gotchas/` |
| Spec questions (limits, quotas, pricing, fields, event behaviour) | Look it up in the live official docs, answer with links | `scripts/line_docs.py`, `references/doc-map.md` |
| Operate the API for the user | `scripts/line_api.py`: dry run, confirm, then `--yes` | "Operating the API" below |

Gotcha files (read only the ones that match the task):
`webhooks-and-hosting.md` (signatures, timeouts, dedupe, Supabase/Vercel/Workers traps) ·
`messaging.md` (reply vs push, quota, Flex, postbacks, media, long text, quotes/unsend) ·
`groups-and-mentions.md` (joining, members/profiles, scoping, mentions/textV2) · `rich-menus.md` ·
`liff-and-login.md` (SDK versions and security updates, ID-token verification, expiry/re-login, provider/userId) ·
`security-and-architecture.md` (tokens, LLM-bot patterns, testing).

## The one rule: verify LINE facts against the live docs

LINE changes limits and behaviour regularly (reply-token windows, push eligibility, message counting, new
event types such as `messageEdited`, deprecated SDK versions, end-of-life features like LINE Notify).
Remembered numbers are often stale, and a wrong limit becomes a production bug or a wrong cost estimate.
Before you state or code a number, limit, quota, field name, or "can the bot do X" fact, look it up:

```bash
python3 scripts/line_docs.py search "loading animation"        # which pages cover it
python3 scripts/line_docs.py section "Send reply message"      # one API-reference section (+ citable URL)
python3 scripts/line_docs.py page messaging-api/pricing --grep "count"
```
(`--product liff|line-login|...` for other references; `references/doc-map.md` has the page list, anchors,
and manual fallbacks.) Cite the `developers.line.biz` URL next to each claim. If you couldn't fetch it, say the
statement is unverified; if the docs don't cover it, say so instead of guessing.

Keep lookups proportional: the reference plus the few guide pages that matter is usually enough. Go to news,
regional pricing pages or release notes only for volatile topics - pricing and quotas (send the user to the
regional page; the docs' example table is Japan's), deprecations, recently added features, SDK versions.

## Mental model (details and current numbers: the gotcha files and the docs)

- **Provider > channels.** A Messaging API channel is the bot / Official Account; LIFF apps live on a LINE
  Login channel. User IDs are issued **per provider**, and channels can't be moved between providers.
- **Webhook.** Verify `x-line-signature` (HMAC-SHA256 over the *raw* body bytes, key = the Messaging API
  channel secret, base64) before parsing, return 2xx within LINE's short timeout, do slow work in the
  background. Events can repeat or arrive out of order (`webhookEventId`). Verify sends `"events": []`.
- **Reply vs push.** Reply is free but needs the event's single-use, short-lived reply token. Push and
  friends count against the monthly quota **per recipient** - a push to a group counts once per member.
- **1:1 vs group.** Groups need "Allow bot to join group chats". The loading animation and rich menus are
  1:1-only (rich menus also don't show on LINE for PC); listing group members needs a verified/premium
  account; the event set differs (see the table in `receiving-messages`).
- **Messages.** A handful of objects per request (5 at the time of writing); Flex/template/imagemap need
  `altText`; validate endpoints check a message without sending it.
- **LIFF / LINE Login.** Verify the ID token server-side with the **LINE Login channel ID**; tokens expire
  and the SDK keeps returning the cached one.
- **Account settings fight your bot.** Auto-reply and greeting messages are on by default; "Use webhook"
  must be on (console / LINE Official Account Manager).

## Building, reviewing and debugging

1. **Scope.** Fix the reported problem with the smallest change that works, and explain the cause. Put
   production hardening (dedupe tables, queues, retries, chunking, monitoring) in a short "worth doing
   next" list instead of adding it - no new tables, migrations, dependencies or deploy steps unless the user
   asked for production-ready code or the fix needs them. "Smallest" never means "partly right": when the
   broken thing *is* such a mechanism (a dedupe that doesn't dedupe, a retry that duplicates), fix it the
   documented way (e.g. dedupe keyed on `webhookEventId`, covering every event type). When reviewing code,
   rank findings by severity and give each a concrete fix.
2. **Read the matching gotcha file(s)** - each entry is *symptom -> cause -> fix -> doc page*, collected from
   production bots. When code pins SDK versions (`@line/liff`, `@line/bot-sdk`, ...), check the release notes
   for deprecations and say so if the user's version is affected.
3. **Webhook non-negotiables** when you write or fix a handler: signature on raw bytes with a constant-time
   compare, reject bad signatures (4xx) before any work, 200 for an empty `events` array, fast acknowledgement
   with background processing, tolerate unknown event types/fields, check LINE API responses and log
   `x-line-request-id`. If background work answers with the reply token, bound it - a timeout on the slow
   call plus a fallback reply - so something still goes out while the single-use token is valid, and tell
   the user what happens past that window (push costs quota).
4. **Verify your fix yourself** without a phone: `scripts/webhook_tools.py selftest <url>` (Verify ping, signed
   event, bad/missing signature, timing) and `simulate <url> <type>` (text, mention, image, sticker, postback,
   follow, unfollow, join, leave, memberJoined, memberLeft, unsend, verify); `sign`/`verify` for captured
   bodies; `sample <type>` for fixtures. Report what you ran and what you couldn't (e.g. the real platform).
5. **Tests the user should run** must be self-contained - curl + openssl, or a small script you include -
   because the skill's scripts live where you (the agent) run, not necessarily on the user's machine
   (template in `security-and-architecture.md`).
6. **Check the account side** when behaviour is odd: `line_api.py info` (chatMode), `webhook-info`,
   auto-reply/greeting settings in LINE Official Account Manager.

Scripts need only Python 3.8+; run them with `python3` (Windows: `python` / `py -3`). Paths are relative to
this skill's folder - in Claude Code `${CLAUDE_SKILL_DIR}`, e.g.
`python3 "${CLAUDE_SKILL_DIR}/scripts/line_docs.py" search "reply token"`.

## Answering spec questions

Lead with the direct answer, give the condition or number with its source link, and flag anything
region-specific (pricing), plan-specific (verified/premium-only endpoints) or version-specific (minimum app
versions, SDK deprecations). Label what is documented vs. your inference, and name what the docs don't say.
When the user's premise is outdated (LINE Notify, "reply tokens last 30 s", "one push to a group = one
message"), correct it with the link.

## Operating the API

Use `scripts/line_api.py` (`-h` lists commands). It talks only to `api.line.me` / `api-data.line.me`, reads
the token from `LINE_CHANNEL_ACCESS_TOKEN` or `--env-file path/to/.env`, and never prints it. Keep tokens off
command lines yourself too: don't `source .env` or expand the token into curl arguments (shell history,
process lists, logs) - use the script's `--env-file`.

**Safety tiers** - messages reach real people and cost quota, and some changes (default rich menu, webhook
URL) instantly affect every user; none of it can be unsent quietly.
1. *Read-only* - run freely: `info`, `quota`, `webhook-info`, `profile`, `group-summary`, `group-count`,
   `group-member`, `richmenu-list`, `richmenu-get`, `richmenu-default`, `content`.
2. *Validation* - run freely, nothing is delivered: `validate <reply|push|...> file.json`,
   `richmenu-validate menu.json --image menu.png` (local pre-flight checks plus the API's validator).
3. *Writes* - `push`, `multicast`, `broadcast`, `webhook-set`, `richmenu-deploy`, `richmenu-set-default`,
   `richmenu-link`, `richmenu-delete`, `group-leave`, `call` with POST/PUT/DELETE. Without `--yes` they only
   validate and print the exact request plus notes (recipient type, group size, quota left). Re-run with
   `--yes` when the user explicitly asked for this exact action, target and content and the dry run showed
   nothing surprising, or after they confirmed the dry run. Always confirm first when you wrote the content,
   when it goes to many people, when it replaces something that exists (default rich menu, webhook URL), or
   when you had to change the inputs to pass validation.

Workflow details:
- Fix validation errors before creating anything; nothing about a rich menu can be edited after creation, so
  also confirm placeholder URLs/labels. `richmenu-deploy menu.json image.png --default` runs validate ->
  create -> upload (api-data) -> set default and says how to clean up if a step fails; check with
  `richmenu-default` afterwards.
- When you fix inputs (shorter text, compressed image), write new files next to the originals and say what
  you changed; let the user approve wording changes.
- Sends carry an `X-Line-Retry-Key`, reused on retries, so a timeout never duplicates a message.
- On errors the script prints status, a hint, LINE's error body and `x-line-request-id`. 401 = invalid,
  expired, revoked or wrong-channel token: stop and ask for the right token; if their bot is live, warn that
  reissuing the long-lived token breaks it. A 429 can be the monthly quota, not a rate limit.
- Anything without a subcommand: `line_api.py call METHOD /v2/bot/... --data body.json` (writes still need
  `--yes`).

Never paste a token or secret into chat or commit it. If one has leaked, tell the user to reissue or revoke it.

## Files

- `scripts/line_docs.py` - live doc search / section / page lookup with citable URLs.
- `scripts/line_api.py` - Messaging API operations with dry-run safety.
- `scripts/webhook_tools.py` - signature tools, webhook simulator, self-test.
- `references/doc-map.md` - where everything is in the official docs (URL patterns, page list, anchors,
  OpenAPI specs, status page, deprecations, site-only pages).
- `references/gotchas/*.md` - field-tested failure modes and patterns, one file per area (list above).
