# Gotchas: sending messages, quota, Flex, media, quotes

Field-tested failure modes from production LINE bots, checked against the official docs. Each entry:
**symptom or rule -> cause -> fix**, plus the page to re-check (paths relative to
`https://developers.line.biz/en/`). Numbers marked "(at the time of writing)" were checked in 2026-10.

## Contents
1. Reply, push and the message quota
2. Flex Messages, actions, postbacks, quick replies
3. Media, files, stickers and long text
4. Quotes, edits and unsend

## 1. Reply, push and the message quota

**"Invalid reply token".** Single use, valid only briefly (about one minute at the time of writing; LINE
says not to rely on the exact limit; a redelivered event's token works only if unused and the event is
recent). Causes: two code paths both reply; replying after slow work; retrying a reply that succeeded;
replying to a redelivery whose token was used. Decide the one reply per event in one place. Judge staleness
by delivery (`isRedelivery` + your own "already replied" record), not by `now - event.timestamp`.
Re-check: `reference/messaging-api/#send-reply-message-reply-token`.

**Long jobs vs the reply window.** If the answer may take longer than the window: reply now ("working on
it" - free, but it *uses up* the event's only reply token), then push the result later (billed); or keep the
token and reply once with the result if it reliably arrives in time; or reply with a postback button
("show answer") whose tap brings a fresh reply token. Choose per message class: results the user asked for
deserve a push; chatter doesn't. Either way, put a timeout on the slow call (well inside the window, e.g.
~45 s) with a fallback reply ("that took too long, please try again"), so an error or a hang never leaves
the user with silence. In 1:1 chats show the loading animation meanwhile.

**Quota disappears fast in groups.** Push/multicast/broadcast/narrowcast count per *recipient*: one push to a
group of N members counts N, regardless of how many message objects it carries. Replies don't count.
Reply-first design; put several objects in one message instead of several pushes; estimate volume for any
scheduled/alerting feature (reminders x recipients x repeats) before building it; compare with
`line_api.py quota` after a pilot. Whether the bot itself or members who blocked the account are counted
isn't spelled out in the docs - measure with the delivery statistics endpoints instead of assuming.
Re-check: `docs/messaging-api/pricing/` + the regional pricing page.

**One outbound function.** Route all sends through one function that applies mute/audit, replies with the
first <= 5 objects, pushes overflow or falls back to push deliberately, and returns `sentMessages[].id` (same
order as sent; store them - section 4). Make `reply()` report failure only on HTTP failure - if it returns
null because the 200 body wasn't JSON, the caller pushes a duplicate.

**429 that never clears.** `You have reached your monthly limit.` is the quota, not a rate limit: stop
sending (don't retry), alert someone, fall back to reply/other channels.

**200 is not delivery.** Push to someone who blocked the account, deleted their account, or isn't eligible
returns 200 and isn't delivered (and isn't counted). Eligibility has changed over time (at the time of
writing: friends, groups the bot is in, and users who messaged the account 1:1 within 7 days). Keep a
durable in-app inbox (e.g. shown in LIFF) as the guaranteed channel; push is best effort.
Re-check: `reference/messaging-api/#send-push-message`.

**Duplicate pushes after timeouts.** Send push/multicast/narrowcast/broadcast with `X-Line-Retry-Key: <uuid>`
(one key per logical send, reused on every retry, valid 24 h at the time of writing); 409 = an earlier attempt
was accepted (success). Other endpoints - including reply - reject the header with 400. Retry only network
errors, 5xx and non-quota 429s, with backoff. Never blind-retry a reply.
Re-check: `docs/messaging-api/retrying-api-request/`.

**Recurring notifications.** Digests and reminders are the fastest way to burn quota - consider email or an
in-app inbox. LINE Notify is discontinued; LIFF pages can't receive web push (they run in LINE's in-app
browser).

**Users stare at silence while an LLM thinks (1:1).** `POST /v2/bot/chat/loading/start` with `chatId=userId`
shows a typing indicator (5-60 s in steps of 5 at the time of writing), only while the user is viewing the
chat, on recent app versions, until your next message. Groups/rooms: not supported (400) - reply with a
short acknowledgement or nothing. Re-check: `docs/messaging-api/use-loading-indicator/`.

**Bots that talk too much get kicked.** Provide a global and per-group mute (processing continues, output
stops; onboarding/consent messages bypass it) and throttle your own error notices.

## 2. Flex Messages, actions, postbacks, quick replies

**400 on send.** Validate first (`line_api.py validate push card.json`) - it names the failing property.
Usual causes: missing `altText`; undocumented property names (use `paddingAll`/`paddingTop`/...); empty
`text` in a component (skip empty fields instead); a label over its limit (limits depend on where the action
is used - `reference/messaging-api/#action-object-label-spec`); one bad `uri`. Design in the Flex Message
Simulator.

**One bad URI rejects the whole message.** URI actions accept only `http`, `https`, `line`, `tel` (no
`mailto:`), up to 1000 characters, percent-encoded UTF-8 (at the time of writing). Validate URIs built from
data (scanned phone numbers, websites) and drop the button when invalid; `altUri.desktop` for PC.
Re-check: `reference/messaging-api/#uri-action`.

**Size is bytes, not component counts.** Bubble JSON <= 30 KB, carousel <= 50 KB and <= 12 bubbles, whole
request <= 2 MB (413) (at the time of writing). Measure the serialized size before sending and degrade
gracefully ("...and 8 more", link to LIFF). Re-check: `reference/messaging-api/#flex-message`.

**altText is the notification, the chat-list preview and the quote preview.** Write it as a sentence
("Alice assigned you: Q4 report, due Fri"), never "Flex message".

**Sent cards can't be edited.** Avoid relative times ("tomorrow") in cards; show live state in LIFF.

**Postback data is small** (300 characters at the time of writing): put an action and an ID in it
(`action=claim&id=123`), keep state server-side. Handlers must allow-list actions, check the source chat
(cards can be forwarded into other chats), check current state (closed items), and treat repeats (double
taps, redeliveries) as silent no-ops. Anyone in a group can tap any card, forever.

**`displayText` posts a visible message as the user.** In groups, prefer postbacks without it and confirm via
the event's reply token (free). Message actions likewise post visible text - fine for a "/command" interface,
noisy in groups.

**Compact group cards:** `size: "micro"`/`"kilo"` bubbles, `box`-level actions for small "pill" buttons (the
`button` component is large), deep links into LIFF (`https://liff.line.me/{liffId}?item=123`; the params
arrive directly or inside `liff.state`).

**No state-changing GET links** (in chat or email): link scanners and previews open them before the user
does. Link into LIFF and act there with a verified identity, or use postbacks.

**Quick reply buttons** disappear when one is tapped (camera/location/datetime ones stay until used) or when
anyone sends a new message; max 13 per message (at the time of writing). Not persistent navigation - that's
the rich menu. Re-check: `docs/messaging-api/using-quick-reply/`.

**Actions with app-version or chat-type constraints** (postback `inputOption`, datetime picker, camera,
clipboard): check `docs/messaging-api/actions/` first.

## 3. Media, files, stickers and long text

**Downloading content.** `GET https://api-data.line.me/v2/bot/message/{id}/content`, only when
`contentProvider.type === "line"` (`external` = a URL you fetch yourself). Video/audio: poll
`.../content/transcoding` until `succeeded` (images/files don't need it). Treat anything but 200 as "not
available" - **202 passes `res.ok`** and you'd store an empty file. Content is deleted after an undisclosed
period: download promptly (in the background). Re-check: `reference/messaging-api/#get-content`.

**Check `message.fileSize` before downloading** and reject oversized files without buffering them; on failure
tell the user in plain language (not the storage error); don't post "received" for every file in a group.

**Never use the LINE-provided `fileName` as a path or storage key** (path traversal - on Windows `\` too -,
overwrites, non-ASCII keys rejected by object storage, header injection). Store as `<chatId>/<messageId>.<ext>`
with a sanitized extension, keep the original name as metadata, use RFC 5987 `filename*=` in downloads.

**Idempotent by message ID.** Check whether this `message.id` is already stored before downloading/binding.

**Don't send the channel token to redirect targets** when fetching media or URLs; guard user-supplied URLs
against SSRF (scheme/host allow-list, block private ranges).

**Stickers.** Events carry `packageId`, `stickerId`, `stickerResourceType`, optional `text` (message stickers)
and `keywords` (experimental, a random subset of up to 15, may be absent - at the time of writing). To read
reactions, map an allow-list of sticker IDs first, then exact keyword matches; on conflict do nothing; never
let a sticker trigger a destructive action.

**Long text.** Text/textV2 messages hold up to 5000 characters counted as UTF-16 code units (JS `.length`) at
the time of writing (`docs/messaging-api/text-character-count/`), and a request carries <= 5 objects. Split at
newlines, never inside a surrogate pair or a textV2 placeholder, and decide explicitly what happens beyond 5
chunks (push the rest, or a preview + link/file). Don't silently `slice(0, 5)` or truncate.

## 4. Quotes, edits and unsend

**Store `sentMessages[].id` of every bot message users might reply to** (reply/push responses return
`sentMessages` with `id` and `quoteToken`, in send order). An incoming quote gives only `quotedMessageId`, and
there is no API to fetch past message text - resolve quotes through your own `lineMessageId -> item` table,
scoped to the chat.

**Require quoting for destructive or ambiguous actions** ("cancel that"): guessing deletes the wrong item.
"Quote + fixed command word" can take a deterministic fast path that skips the LLM.

**Quoting in your reply:** pass the incoming message's `quoteToken` in a text/textV2/sticker message. Quote
tokens only work in the chat where the message was sent and don't expire (at the time of writing); a quoted
Flex/template shows only its altText. Re-check: `docs/messaging-api/get-quote-tokens/`.

**Edits (`messageEdited`, groups only at the time of writing):** the event carries the edited message and a new
reply token. Decide whether edits update what you derived from the original.

**Unsend:** LINE recommends making the content unusable everywhere (logs, LLM context, derived records). You
only get the message ID, so every derived record must store its source message IDs; also mark any
still-buffered copy as processed. No reply token. Re-check: `docs/messaging-api/receiving-messages/`.
