# Gotchas: webhooks, signatures, slow work, hosting

Field-tested failure modes from production LINE bots, checked against the official docs. Each entry:
**symptom or rule -> cause -> fix**, plus the page to re-check (paths relative to
`https://developers.line.biz/en/`). Numbers marked "(at the time of writing)" were checked in 2026-10.

## Contents
1. Receiving and signatures
2. Idempotency, ordering and slow work
3. Hosting and deployment traps

## 1. Receiving and signatures

**Signature never matches.** The body was parsed and re-serialized before hashing (`req.json()` then
`JSON.stringify`, `express.json()` before the check, framework body parsers). Any change - key order,
spacing, `\u` escapes for CJK/emoji, `\/` - breaks the HMAC. Simple bodies like the Verify ping may happen
to match, so it "works" until a real message with Chinese text or emoji arrives. Hash the exact raw bytes,
then parse:
```ts
// Web-standard runtimes: Deno, Bun, Cloudflare Workers, Hono, Next.js route handlers, Node >= 20
export async function verifyLineSignature(raw: string, sig: string | null, secret?: string) {
  if (!sig || !secret) return false;                                    // fail closed
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
  let mac: Uint8Array;
  try { mac = Uint8Array.from(atob(sig), (c) => c.charCodeAt(0)); } catch { return false; }
  return crypto.subtle.verify("HMAC", key, mac, enc.encode(raw));      // constant-time
}
// handler: const raw = await req.text();
//          if (!(await verifyLineSignature(raw, req.headers.get("x-line-signature"), SECRET)))
//            return new Response("invalid signature", { status: 403 });
//          const body = JSON.parse(raw);
```
Node/Express: `express.raw({ type: "*/*" })` on the webhook route and `crypto.timingSafeEqual` on
equal-length buffers, or the official SDK's middleware. Python: `await request.body()` (FastAPI/Starlette),
`request.get_data()` (Flask), then `hmac.compare_digest`. Re-check: `docs/messaging-api/verify-webhook-signature/`.

**Signature mismatches although the code is right.** Wrong channel's secret - a project with a Messaging
API channel *and* a LINE Login/LIFF channel has two different secrets; the webhook uses the Messaging API
one. Also: the secret was reissued, the env var has a trailing newline/space (`.trim()` it), or a proxy
rewrote the body.

**Fail closed.** If the secret is missing, refuse (500) - don't log a warning and accept. Don't ship "test
mode" bypasses keyed on env vars; sign test fixtures instead. Reject a missing or wrong signature *before*
any work, or anyone can forge postbacks and make you spend quota. Compare in constant time, never `===`.
Answering your own signature failures with a distinct status/body (e.g. 403 "invalid signature") makes it
obvious later whether a 401 came from your code or from a gateway in front of it.

**Console "Verify" fails but real messages work (or the reverse).** Verify (and connectivity checks) send
`{"destination": "...", "events": []}`. Code like `body.events[0].replyToken` crashes -> 500. Loop over
`events ?? []` and return 200. Re-check: `docs/messaging-api/verify-webhook-url/`.

**Route by `event.type`, then `source.type` (user/group/room).** Events with a reply token: message,
`messageEdited`, postback, follow, join, memberJoined. Without: unsend, unfollow, leave, memberLeft -
anything you send for those is a billed push. Which events arrive in 1:1 vs group vs multi-person chats is
tabled in `docs/messaging-api/receiving-messages/` (e.g. follow/unfollow are 1:1 only - unfollow means the
user blocked you; join/leave/memberJoined/memberLeft are group/room only; edit events are group-only at the
time of writing).

**New event types and fields appear without notice** (`messageEdited` is newer than most tutorials).
Ignore unknown `type`s and extra fields; don't use strict schemas that reject them.

**`source.userId` is missing.** Only present on some events, and absent for users who never consented to
profile access (e.g. accounts only ever used on LINE for PC). Handle `undefined`.
Re-check: `docs/messaging-api/user-consent/`.

**`mode: "standby"` events** have no reply token: another module is handling the chat - don't send.

**Don't IP-allowlist or IP-rate-limit the webhook.** LINE doesn't publish its source IPs and they change; a
429 from you is a failed delivery. `X-Forwarded-For` is client-controlled anyway. The signature is the gate.
Re-check: `docs/messaging-api/development-guidelines/#prohibiting-ip-address-restrictions`.

**Flex/template messages a user sends via `liff.sendMessages()`** produce no webhook; other types do.

## 2. Idempotency, ordering and slow work

**`request_timeout` in the webhook error statistics, duplicates, or replies minutes late.** The handler
awaits slow work (LLM, DB, downloads, chains of LINE API calls - even per-message profile lookups) before
responding. LINE counts a response slower than about 2 s (at the time of writing) as a failure and, if
redelivery is enabled, sends the events again. Verify -> persist/enqueue -> return 200 -> process in the
background. Re-check: `docs/messaging-api/check-webhook-error-statistics/`.

**Fire-and-forget isn't durable.** `handle(events).catch(...)` without storage responds fast but loses
events on crash/redeploy and nothing retries. For production, store first (DB row/queue), then process.

**Dedupe with a unique INSERT, never an upsert.** Key on `webhookEventId` (every event type has it; it's
unchanged on redelivery, `deliveryContext.isRedelivery` is true) - `message.id` only covers message events.
An upsert "succeeds" on the redelivered copy, so the pipeline runs twice (duplicate cards). An in-memory Set
is lost on restart and not shared across instances.
```sql
create table line_events (webhook_event_id text primary key, payload jsonb not null, received_at timestamptz default now());
insert into line_events (webhook_event_id, payload) values ($1, $2) on conflict do nothing returning webhook_event_id; -- no row = duplicate
```
When the dedupe itself is what's broken or under review, fix it properly - keyed on `webhookEventId`, for
every event type (a `message.id`-only fix leaves postbacks, joins and unsends unprotected). When you're
fixing an unrelated bug, suggest dedupe rather than bolting new tables onto that fix.

**Claim before slow work** when more than one path can process a stored message (realtime path + periodic
flush, retries, several instances): `update ... set claimed_at = now() where id = $1 and claimed_at is null
returning id`; release with an attempts counter and give up after N. Without it, a 13-second LLM call was
enough for a cron flush to build a second identical card.

**Order matters per chat.** Redeliveries can arrive out of order (use `timestamp`), and with slow LLM calls a
follow-up message ("add this too") can be processed before its parent exists. Serialize processing per chat
(lock table + owner token; session advisory locks don't work through PostgREST/HTTP poolers).

**An image and the text explaining it are separate events,** sometimes seconds apart or from different
people. Bind them by sender + short time window, or (authoritatively) by the user quoting the image.

## 3. Hosting and deployment traps

**401/403 before your code runs** (Verify fails, function logs empty). A platform auth layer rejects LINE,
which sends no `Authorization` header:
- **Supabase Edge Functions** verify a JWT by default -> set `[functions.<name>] verify_jwt = false` in
  `supabase/config.toml` (persists across deploys) or deploy with `--no-verify-jwt`. Do the same for LIFF
  API functions that verify the LINE ID token themselves; every route must then authenticate itself.
- Vercel Deployment Protection on preview URLs, Cloudflare Access, API-gateway authorizers, basic auth on
  staging: exempt the webhook path.
- Tell them apart: the gateway's 401 has the gateway's error body and leaves no log line from your function;
  your own failures carry your body/status. A one-line curl with a correctly signed body shows which layer
  answered.

**Background work dies after the response.** Use `EdgeRuntime.waitUntil(p)` (Supabase), `ctx.waitUntil(p)`
(Cloudflare Workers), `waitUntil` from `@vercel/functions` - or a queue/job table for anything longer than
the platform allows.

**Cold starts eat the timeout.** Keep the webhook entry small; acknowledge before loading heavy modules.

**Secrets.** Set them from a file or the dashboard (`supabase secrets set --env-file supabase/.env`,
`wrangler secret put`), not as values typed on a command line (shell history). A local `.env` is not
deployed. `KEY=` sets an empty string (so `?? default` doesn't apply, `Number("")` is 0) - comment unused keys
out. A secret stored in two places (function env + DB vault used by cron) silently 403s when they drift - set
both from one generated value and compare digests. A missing LIFF URL silently produces cards without
buttons - fail loudly at startup when required settings are missing.

**Local development** needs a public HTTPS URL with a valid certificate: tunnel (ngrok, cloudflared) +
`line_api.py webhook-set` / `webhook-test`, and switch back afterwards (URL changes can take up to a minute
to apply, at the time of writing). Re-check: `docs/messaging-api/ssl-tls-spec-of-the-webhook-source/`.

**Supabase Edge Functions specifics** (observed in production; verify for your setup): HTML responses are
rewritten to `text/plain` with a sandbox CSP, so redirect (302) to your LIFF app instead of serving pages;
an uncaught async error kills the isolate and the browser shows a **CORS error** (a 503 without CORS
headers) - check function logs before touching CORS; outbound SMTP on ports 25/587 is blocked.

**LIFF hosting.** Point the LIFF endpoint URL at the stable production address, never a per-deploy preview
URL (it freezes on that build); on Cloudflare Pages deploy with `--branch=<production branch>`. Disable HTML
caching. `VITE_*`/`NEXT_PUBLIC_*` variables are public and baked in at build time - LIFF ID and API base URL
only, never secrets; rebuild after changing them.

**Windows PowerShell scripting.** `curl` is an alias of `Invoke-WebRequest`; send bodies as UTF-8 bytes and
strip CRLF, or Chinese/Japanese text in rich menu/Flex JSON gets mangled (use `curl.exe` or the bundled
Python scripts).
