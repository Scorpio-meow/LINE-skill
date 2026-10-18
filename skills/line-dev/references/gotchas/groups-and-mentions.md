# Gotchas: group chats, members, lifecycle, mentions

Field-tested failure modes from production LINE group bots, checked against the official docs. Each entry:
**symptom or rule -> cause -> fix**, plus the page to re-check (paths relative to
`https://developers.line.biz/en/`). Numbers marked "(at the time of writing)" were checked in 2026-10.

## Contents
1. Joining, consent and lifecycle
2. Members and profiles
3. Scoping everything to the chat
4. Mentions (incoming and outgoing)

## 1. Joining, consent and lifecycle

**Bot can't be invited.** "Allow bot to join group chats" is off by default (console > Messaging API tab /
Official Account Manager - the toggle moves between UI versions). Only one Official Account per group.

**Anyone can add your bot to any group.** On `join`, mark the group pending, reply with an onboarding card
(plain-language steps + one button, not a bare link) and store/analyse nothing until an authorised person
activates it (e.g. a LIFF page with a verified ID token shows a short-lived code that the *same* LINE user
posts in the group - LIFF alone can't prove group membership). Leave unactivated groups after a timeout
(`POST /v2/bot/group/{id}/leave`). Don't re-send onboarding on re-joins/redeliveries.

**The bot receives every member's messages** once it's in a group. A per-member opt-out can only mean "we
don't store/process yours". Say so in privacy notices; honour unsend.

**`leave`** fires when the bot is removed *or* leaves via the API; afterwards you can neither receive from nor
push to that group, and there's no reply token. Soft-delete with a grace period (users remove bots by
accident); a `join` with the same groupId restores. Make the handler a no-op for groups you already purged.

**`memberLeft`:** revoke that user's per-group roles/permissions and flag their open work.

**Multi-person chats (`roomId`)** were merged into groups in newer LINE versions, but old rooms exist: handle
`source.type === "room"` (endpoints under `/v2/bot/room/...`) or ignore rooms deliberately.

**Multicast can't target groups;** push to each group ID. There's no API to create a group invite link.

## 2. Members and profiles

**Can't list the members.** "Get group chat member user IDs" needs a verified or premium account. Build the
roster from `memberJoined.joined.members`, message senders and mentionees; an @All mention carries no IDs;
silent members stay unknown - tell users. Re-check: `docs/messaging-api/group-chats/`.

**Profile lookups.** Choose the endpoint by `source.type`, not ID prefix:
- group -> `GET /v2/bot/group/{groupId}/member/{userId}` - works for members who never added the bot and even
  for users who blocked it;
- room -> `GET /v2/bot/room/{roomId}/member/{userId}`;
- 1:1 -> `GET /v2/bot/profile/{userId}` - friends and recent 1:1 senders only, so it returns 404 for most
  group members. Calling it for group senders is a classic "names missing for half the group" bug.
On failure keep the cached name and show a placeholder; never store the userId as the display name; never
overwrite a known name with null. Cache names - a profile call per message also slows the webhook. Key
everything by userId; names aren't unique or stable. Re-check: `reference/messaging-api/#get-group-member-profile`.

**Group name/icon:** `GET /v2/bot/group/{groupId}/summary`.

## 3. Scoping everything to the chat

Every identifier that reaches you through a user action - `quotedMessageId`, postback data, LIFF item IDs,
mentions - must be resolved within the event's chat (and, for LIFF, the caller's verified membership). Flex
cards can be forwarded into other chats, so a postback for item 123 can arrive from a group that doesn't own
item 123. Cross-group leaks found this way in production included cancelling another group's item by quoting
its card and pulling another group's text into LLM context. Filter every query by the source chat ID and keep
regression tests for tenant isolation.

## 4. Mentions (incoming and outgoing)

**Reading mentions.** The field is `message.mention.mentionees[]` (not `mentions` - reading the wrong field
silently finds nothing). Each has `index`, `length`, `type` (`user` | `all`), `userId` (absent without
profile consent) and `isSelf: true` when the mention is your bot (your bot's userId is also the webhook
`destination`, or `GET /v2/bot/info`). "The bot was mentioned" = some mentionee has `isSelf`; don't detect it
by matching display-name text like `text.includes("@MyBot")` (renames, nicknames, other bots). Exclude the bot
when collecting mentioned members, or it ends up as a phantom member.
```ts
export function readMentions(m: { text?: string; mention?: { mentionees?: any[] } }) {
  const r = { botMentioned: false, all: false, users: [] as { userId: string; label: string }[] };
  for (const x of m.mention?.mentionees ?? []) {
    if (x.type === "all") { r.all = true; continue; }           // carries no user IDs
    if (x.isSelf) { r.botMentioned = true; continue; }
    if (!x.userId) continue;                                     // no profile consent
    r.users.push({ userId: x.userId, label: (m.text ?? "").slice(x.index, x.index + x.length) });
  }
  return r;
}
```

**Sending a real @mention** needs a `textV2` message with `{key}` placeholders and a `substitution` map;
sending the incoming `mention.mentionees` shape is ignored (degrades to plain text). Only in reply/push to a
group/room the bot is in; every mentionee must be a member (the validate endpoint does *not* check this - one
bad mentionee makes the whole request fail); max 20 mentions (at the time of writing); keys `[0-9A-Za-z_]`,
<= 20 chars; you can't mention a bot. In 1:1 chats send plain text. Re-check: `reference/messaging-api/#text-message-v2`.

**Build textV2 from typed segments, never by pasting user/LLM text into a template string.** In textV2,
`{...}` is substitution syntax: literal braces in user or model text either break the message (unpaired
brace, undefined key -> 400) or get interpreted as placeholders. Escape `{`/`}` as `{{`/`}}` in every text
segment:
```ts
type Seg = { text: string } | { userId: string } | { all: true };
export function buildMention(segs: Seg[]) {
  let text = "", plain = "", n = 0; const substitution: Record<string, unknown> = {};
  for (const s of segs) {
    if ("text" in s) { text += s.text.replace(/[{}]/g, (c) => c + c); plain += s.text; continue; }
    const key = `m${n++}`; text += `{${key}}`;
    substitution[key] = { type: "mention", mentionee: "all" in s ? { type: "all" } : { type: "user", userId: s.userId } };
  }
  return n ? { type: "textV2", text, substitution } : { type: "text", text: plain };
}
```
Chunking long textV2 must not split a `{key}` or an escape.
