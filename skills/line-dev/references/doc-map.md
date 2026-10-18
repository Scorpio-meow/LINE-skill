# LINE official documentation map

Links only - this skill deliberately ships no copies of the docs, because LINE updates them
continuously. Fetch the live page every time a number, limit, field name or behaviour matters.

## Contents
1. How to look things up (URL patterns, raw markdown, big reference pages)
2. Messaging API - guides
3. Messaging API - reference anchors (endpoints, events, message objects)
4. LIFF
5. LINE Login
6. Accounts, channels, tokens, console
7. Tools, SDKs, machine-readable specs
8. Status, news, deprecations

---

## 1. How to look things up

**Two mirrors of the same content:**

| What | Pattern |
|---|---|
| Site page (cite this to the user) | `https://developers.line.biz/{en,ja}/docs/<product>/<page>/` |
| Same page as raw Markdown (best for fetching) | `https://raw.githubusercontent.com/line/line-developers-docs-source/main/docs/{en,ja}/docs/<product>/<page>/index.html.md` |
| API reference on the site | `https://developers.line.biz/en/reference/<product>/#<anchor>` |
| API reference as raw Markdown (one big file per product) | `https://raw.githubusercontent.com/line/line-developers-docs-source/main/docs/en/reference/<product>/index.html.md` |

`<product>` is one of `messaging-api`, `liff`, `liff-server`, `line-login`, `line-login-v2`,
`line-mini-app`, `line-notification-messages`, `partner-docs` (reference) or additionally
`basics`, `line-developers-console`, `line-login-sdks`, `line-ads-api`, `line-conversion-api` (docs).

The source repo (https://github.com/line/line-developers-docs-source) is synced automatically from the
site; its README says some site content is missing and formatting may differ slightly. It explicitly
allows using the Markdown with AI tools.

**Fastest: `scripts/line_docs.py`** (fetches the live Markdown, caches it for a day, prints the site URL to
cite):
```bash
python3 scripts/line_docs.py search "loading animation"            # where is it documented? (all pages)
python3 scripts/line_docs.py section "Send push message"           # one API-reference section
python3 scripts/line_docs.py ref --grep "Max character limit" -C 0  # grep the reference with section names
python3 scripts/line_docs.py page messaging-api/pricing --grep count
python3 scripts/line_docs.py section "liff.getIDToken()" --product liff
```

**Manual recipes** (when the script can't run):
- *A guide page*: fetch the raw Markdown URL (your web-fetch tool, or `curl -sL <url>`), then cite the site URL.
- *One endpoint / object in the Messaging API reference*: the raw file is ~700 KB - download once and grep
  for the `### Heading` (titles match section 3 below), then read ~150 lines from there. Without a shell,
  fetch the site URL with the anchor using your web-fetch tool and a pointed prompt.
- *Full-text search*: `git clone --depth 1 --filter=blob:none --sparse https://github.com/line/line-developers-docs-source`
  then `git sparse-checkout set docs/en` and grep.
- *Exact schemas / enums*: LINE's OpenAPI specs (section 7) are authoritative for field names and types.

**Not in the Markdown mirror (site only):** the glossary (`/en/glossary/`), FAQ (`/en/faq/`) and news
(`/en/news/`). The yearly listing `https://developers.line.biz/en/news/<year>/` is plain HTML with every
item's title; individual news pages are client-rendered, so open them with a web-fetch tool. Only go to news when
the topic is volatile (pricing, quotas, deprecations, new event types) or the docs look inconsistent.

**Pricing / free message quota** depends on the account's country and plan and changes over time - follow
the regional links on the pricing page; never quote a number from memory. Japanese (`/ja/`) pages exist for
every English page; useful when an English page is ambiguous.

## 2. Messaging API - guides (`https://developers.line.biz/en/docs/messaging-api/<page>/`)

| Topic | `<page>` |
|---|---|
| Overview / getting started / building a bot | `overview`, `getting-started`, `building-bot`, `nodejs-sample` |
| Receiving webhooks (events, redelivery, which events arrive in 1:1 vs groups) | `receiving-messages` |
| Verify webhook signature (and why verification fails) | `verify-webhook-signature` |
| Verify webhook URL / console "Verify" button | `verify-webhook-url` |
| Webhook error causes & statistics (could_not_connect, request_timeout...) | `check-webhook-error-statistics` |
| TLS requirements of the webhook source | `ssl-tls-spec-of-the-webhook-source` |
| Sending messages (reply vs push vs multicast/narrowcast/broadcast) | `sending-messages` |
| Retrying API requests safely (retry key) | `retrying-api-request` |
| Pricing and how messages are counted | `pricing` |
| Message types overview | `message-types` |
| Character counting (UTF-16, emoji) | `text-character-count` |
| Flex Message: sending / elements / layout / video | `using-flex-messages`, `flex-message-elements`, `flex-message-layout`, `create-flex-message-including-video` |
| Flex Message Simulator tutorial | `using-flex-message-simulator` |
| Actions (postback, message, uri, datetime picker, camera, clipboard, rich menu switch) | `actions` |
| Quick replies | `using-quick-reply` |
| Rich menus: overview / using / per-user / tab switching / playground | `rich-menus-overview`, `using-rich-menus`, `use-per-user-rich-menus`, `switch-rich-menus`, `try-rich-menu` |
| Group chats and multi-person chats | `group-chats` |
| Getting user IDs (per-provider IDs!) | `getting-user-ids` |
| User consent for profile info | `user-consent` |
| Quote tokens (quote a message in a reply/push) | `get-quote-tokens` |
| Loading animation | `use-loading-indicator` |
| Mark as read | `mark-as-read` |
| Account linking (link token) | `linking-accounts` |
| Customize icon and display name per message | `icon-nickname-switch` |
| Audiences / narrowcast | `using-audience` |
| Statistics: impressions, per-unit aggregation | `measure-impressions`, `unit-based-statistics-aggregation` |
| LINE URL scheme (deep links into LINE) | `using-line-url-scheme` |
| Development guidelines (prohibited: load tests, IP allowlists, ...) | `development-guidelines` |
| Channel access token v2.1 (JWT) | `generate-json-web-token` |
| SDK list | `line-bot-sdk` |
| Coupons, membership, beacons | `send-coupons-to-users`, `use-membership-features`, `using-beacons`, `beacon-device-spec` |
| Gaining friends / stopping the API | `sharing-bot`, `stop-using-messaging-api`, `stop-using-line-official-account` |

## 3. Messaging API - reference anchors (`https://developers.line.biz/en/reference/messaging-api/#<anchor>`)

Common specs: `common-specifications`, `domain-name` (api.line.me vs api-data.line.me), `rate-limits`,
`rate-limits-scope`, `status-codes`, `response-headers`, `error-responses`, `retry-api-request`,
`retry-api-request-response`, `signature-validation`.

| Area | Anchors (heading in the raw Markdown in parentheses when it differs) |
|---|---|
| Webhook settings | `set-webhook-endpoint-url`, `get-webhook-endpoint-information`, `test-webhook-endpoint` |
| Webhook payload | `webhooks`, `webhook-event-objects`, `common-properties` |
| Events | `message-event`, `edit-event` (messageEdited), `unsend-event`, `follow-event`, `unfollow-event`, `join-event`, `leave-event`, `member-joined-event`, `member-left-event`, `postback-event`, `postback-params-object`, `membership-event` |
| Incoming message types | `wh-text`, `wh-image`, `wh-video`, `wh-audio`, `wh-file`, `wh-location`, `wh-sticker` |
| Send | `send-reply-message` (Send reply message), `send-reply-message-reply-token`, `send-push-message`, `send-multicast-message`, `send-narrowcast-message`, `send-broadcast-message` |
| Validate before sending (no delivery) | `validate-message-objects-of-reply-message`, `...-of-push-message`, `...-of-multicast-message`, `...-of-narrowcast-message`, `...-of-broadcast-message` |
| Quota & counts | `get-quota`, `get-consumption`, `get-number-of-reply-messages`, `get-number-of-push-messages`, `get-number-of-multicast-messages`, `get-number-of-broadcast-messages`, `get-number-of-delivery-messages` |
| Message objects | `message-objects`, `text-message`, `text-message-v2`, `text-message-v2-mention-object`, `text-message-v2-emoji-object`, `sticker-message`, `image-message`, `video-message`, `audio-message`, `location-message`, `imagemap-message`, `template-messages`, `flex-message`, `quick-reply`, `icon-nickname-switch` |
| Flex containers & components | `bubble`, `bubble-style`, `f-carousel`, `flex-component`, `box`, `button`, `f-text`, `f-image`, `f-video`, `icon`, `span`, `separator`, `filler` |
| Actions | `action-objects`, `postback-action`, `message-action`, `uri-action`, `datetime-picker-action`, `richmenu-switch-action` |
| Users & groups | `get-profile`, `get-follower-ids`, `get-group-summary`, `get-members-group-count`, `get-group-member-user-ids`, `get-group-member-profile`, `leave-group`, `get-room-member-profile`, `get-members-room-count`, `leave-room` |
| Content | `get-content`, `verify-video-or-audio-preparation-status` |
| Chat UI | `display-a-loading-indicator`, `mark-as-read` |
| Rich menu | `rich-menu`, `rich-menu-object`, `validate-rich-menu-object`, `create-rich-menu`, `upload-rich-menu-image`, `upload-rich-menu-image-requirements`, `set-default-rich-menu`, `link-rich-menu-to-user`, `link-rich-menu-to-user-conditions`, `unlink-rich-menu-from-user`, `get-rich-menu-list`, `get-rich-menu`, `delete-rich-menu`, `rich-menu-alias`, `create-rich-menu-alias` |
| Tokens | `issue-stateless-channel-access-token`, `issue-shortlived-channel-access-token`, `issue-channel-access-token-v2-1`, `revoke-channel-access-token-v2-1`, `revoke-longlived-or-shortlived-channel-access-token`, `issue-link-token` |
| Bot | `get-bot-info` |

## 4. LIFF

Check `release-notes` first when touching LIFF code: its top banner lists deprecated SDK versions (at the
time of writing v2.20.0-v2.31.0, deprecated for a security issue - update to v2.31.1+).

Guides (`https://developers.line.biz/en/docs/liff/<page>/`): `overview`, `getting-started`,
`registering-liff-apps`, `developing-liff-apps` (init, behaviour, closing), `opening-liff-app`
(LIFF URLs, permanent links), `using-user-profile` (**send the ID token to your server, never the
decoded profile**), `differences-between-liff-browser-and-external-browser`,
`differences-between-liff-browser-and-line-in-app-browser`, `minimizing-liff-browser`,
`development-guidelines`, `liff-cli`, `cli-tool-create-liff-app`, `liff-plugin`, `pluggable-sdk`,
`versioning-policy`, `release-notes`, `trying-liff-app`.

Reference (`https://developers.line.biz/en/reference/liff/#<anchor>`): `initialize-liff-app`
(liff.init), `initializing-liff-app-notes-1`, `initializing-liff-app-notes-3`, `ready`, `is-in-client`,
`is-logged-in`, `login`, `logout`, `get-context`, `get-os`, `get-language`, `get-app-language`,
`get-version`, `get-line-version`, `get-id-token`, `get-decoded-id-token`, `get-access-token`,
`get-profile`, `get-friendship`, `request-friendship`, `send-messages`, `share-target-picker`,
`open-window`, `close-window`, `scan-code-v2`, `permanent-link-create-url-by`, `permission-query`,
`is-api-available`, `liff-errors`, `use`.
LIFF server API (manage LIFF apps): `https://developers.line.biz/en/reference/liff-server/`.

## 5. LINE Login

Guides (`https://developers.line.biz/en/docs/line-login/<page>/`): `overview`, `getting-started`,
`integrate-line-login` (web flow), `integrate-pkce`, `verify-id-token`, `secure-login-process`,
`security-checklist`, `managing-access-tokens`, `managing-users`, `link-a-bot` (add-friend option),
`how-to-handle-auto-login-failure`, `login-button`, `development-guidelines`, `using-line-url-scheme`.
Native SDKs: `https://developers.line.biz/en/docs/line-login-sdks/`.

Reference (`https://developers.line.biz/en/reference/line-login/#<anchor>`): `issue-access-token`,
`verify-access-token` (GET /oauth2/v2.1/verify), `refresh-access-token`, `revoke-access-token`,
`verify-id-token` (POST /oauth2/v2.1/verify), `userinfo`, `get-user-profile`,
`get-friendship-status`, `deauthorize`, `status-codes`.

## 6. Accounts, channels, tokens, console

- Channel access token types (validity, how many per channel): `https://developers.line.biz/en/docs/basics/channel-access-token/`
- User profile basics: `https://developers.line.biz/en/docs/basics/user-profile/`
- Console overview / roles / notifications: `https://developers.line.biz/en/docs/line-developers-console/{overview,managing-roles,notification,login-account}/`
- Provider & channel best practices (**channels can't move between providers; user IDs are per provider**): `https://developers.line.biz/en/docs/line-developers-console/best-practices-for-provider-and-channel-management/`
- Glossary: `https://developers.line.biz/en/glossary/` · FAQ: `https://developers.line.biz/en/faq/`
- LINE Developers Console: `https://developers.line.biz/console/` · LINE Official Account Manager (auto-reply, greeting, response mode, plan): `https://manager.line.biz/`
- LINE MINI App docs/reference: `https://developers.line.biz/en/docs/line-mini-app/`, `https://developers.line.biz/en/reference/line-mini-app/`

## 7. Tools, SDKs, machine-readable specs

- Flex Message Simulator: `https://developers.line.biz/flex-simulator/`
- Official SDKs: `https://github.com/line/line-bot-sdk-{nodejs,python,go,java,php,ruby,perl}`
- LINE OpenAPI specs (authoritative schemas; generate clients): `https://github.com/line/line-openapi` -
  raw files at `https://raw.githubusercontent.com/line/line-openapi/main/<file>` with `<file>` =
  `messaging-api.yml`, `webhook.yml`, `channel-access-token.yml`, `insight.yml`,
  `manage-audience.yml`, `liff.yml`, `shop.yml`, `module.yml`, `module-attach.yml`
- LIFF tooling: `https://github.com/line/liff-cli`, `https://github.com/line/create-liff-app`,
  `https://github.com/line/liff-inspector`, `https://github.com/line/liff-mock`,
  `https://github.com/line/liff-playground`, npm `@line/liff`

## 8. Status, news, deprecations

- LINE API Status (outages): `https://api.line-status.info/` · outage reports: `https://developers.line.biz/en/news/tags/outage-report/`
- News (new features, spec changes): `https://developers.line.biz/en/news/`
- End-of-life announcements: `https://developers.line.biz/en/news/tags/end-of-life/` - check here before
  recommending any older feature. Example: LINE Notify was discontinued in 2025; notifications now go
  through a Messaging API bot (push to a user or group).
