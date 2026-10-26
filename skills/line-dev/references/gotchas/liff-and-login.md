# Gotchas: LIFF and LINE Login

Field-tested failure modes from production LIFF apps, checked against the official docs. Each entry:
**symptom or rule -> cause -> fix**, plus the page to re-check (paths relative to
`https://developers.line.biz/en/`). Numbers marked "(at the time of writing)" were checked in 2026-10.

## Contents
1. SDK version first
2. Identity on the server
3. Token expiry and re-login
4. User IDs and providers
5. init, deep links and the in-app browser
6. LINE Login web flow and sessions

## 1. SDK version first

Check the banner at the top of `docs/liff/release-notes/` and the LIFF-tagged news before touching LIFF code:
LINE deprecates SDK versions, sometimes for security reasons, and later restricts them on the platform side.
Pin the version in `package.json`/the CDN path and tell the user when theirs is affected.

**The v2.20.0-v2.31.0 XSS (at the time of writing).** Deprecated 2026-09-30 (fixed in v2.31.1), disclosed
2026-10-20 as an XSS (CVE-2026-112148): a LIFF app or LINE MINI App opened in an external browser from a
crafted URL can run attacker JavaScript on the app's domain and read access tokens and on-screen data. Opening
the **endpoint URL** (not the `liff.line.me` LIFF URL) in LINE's in-app browser counts as an external browser
too. LINE plans to restrict these versions **around 2026-11-24 (may move earlier without notice)**: after
that, LINE Login and other LIFF features may stop working for them in external browsers. The restriction
doesn't remove the risk - update now. LINE also emails affected channels' admins ("Update LIFF SDK before
external browser restrictions"); treat such an email as "this channel still serves a vulnerable version".
Re-check: `news/2026/10/20/liff-sdk-issue/`, `docs/liff/release-notes/`.

When the user needs to find and fix affected code:
- **Find every copy.** The version that ships is what matters, not the range in `package.json`: read the
  resolved `@line/liff` version in the lockfile (`bun.lock`, `package-lock.json`, `yarn.lock`,
  `pnpm-lock.yaml`), including LIFF plugins/templates that depend on it; grep HTML/templates for
  `static.line-scdn.net/liff/edge/versions/<x.y.z>/sdk.js`; look for vendored or self-hosted `sdk.js` copies.
  At runtime `liff.getVersion()` prints the loaded version. Check every LIFF app / MINI App on the channel.
- **Fix by integration type.** CDN edge path (`/liff/edge/2/sdk.js`) is already updated - nothing to do.
  CDN fixed path: change the version in the URL. npm: bump `@line/liff` (using the project's package manager),
  make sure the lockfile changes, then rebuild and **redeploy** - an updated lockfile in git doesn't help users
  until the new bundle is live (watch for CDN/service-worker caches serving the old bundle).
- **Which version.** v2.31.1 is the minimum fix. Newer releases may change behaviour: v2.31.2 stopped
  replacing `?` with `&` in LIFF URL query values in the LIFF browser, which affects apps that pass URLs
  (e.g. `return_url`) as query params - recommend the current latest but tell the user to test that, or pin
  the minimum fix if they can't test before the deadline.
- **Afterwards.** The news reports no confirmed attacks and doesn't ask for anything beyond the update; say
  that rather than inventing incident steps. Confirm with `liff.getVersion()` on the deployed site.

## 2. Identity on the server

**Never trust identity from the client.** A `userId` in a query string or body, or `getProfile()` /
`getDecodedIDToken()` results forwarded to the server, can be forged. Send `liff.getIDToken()` as
`Authorization: Bearer <idToken>`, verify it on the server, and use the verified `sub` as the user ID:
- `POST https://api.line.me/oauth2/v2.1/verify` (form body: `id_token`, `client_id` = the **LINE Login
  channel ID** that hosts the LIFF app - not the Messaging API channel ID; it's on that channel's Basic
  settings tab), or
- local JWT verification: LIFF/native tokens are ES256, keys at `https://api.line.me/oauth2/v2.1/certs`,
  `iss = https://access.line.me`, `aud` = LINE Login channel ID (web-login tokens are HS256 with the channel
  secret).
```ts
import { createRemoteJWKSet, jwtVerify } from "jose";
const JWKS = createRemoteJWKSet(new URL("https://api.line.me/oauth2/v2.1/certs"));
export async function lineUser(req: Request, loginChannelId: string) {
  const t = req.headers.get("authorization")?.replace(/^Bearer /, "");
  if (!t) return { error: "missing_token" } as const;
  try {
    const { payload } = await jwtVerify(t, JWKS, { issuer: "https://access.line.me", audience: loginChannelId, algorithms: ["ES256"] });
    return { userId: payload.sub! } as const;
  } catch (e: any) {
    return { error: e?.code === "ERR_JWT_EXPIRED" ? "token_expired" : "invalid_token" } as const; // tell them apart
  }
}
```
Decoding the payload with `atob` is not verification (and `atob` chokes on base64url, giving random 500s).
Answer user-specific responses with `Cache-Control: private, no-store`. The LIFF app needs the `openid` scope
to get an ID token (and `email` for email). Re-check: `docs/liff/using-user-profile/`,
`docs/line-login/verify-id-token/`.

## 3. Token expiry and re-login

**401s after about an hour that a reload doesn't fix (often LINE for PC / external browsers).** ID tokens
expire (one hour at the time of writing) and `liff.getIDToken()` returns the cached token without checking
it; the SDK keeps it in browser storage, so F5 resends the same expired token.
- Before API calls, check `liff.getDecodedIDToken().exp` with a small margin.
- **Re-login only for expiry.** Have the server distinguish `token_expired` from other failures. A wrong
  `aud` (misconfigured channel ID), a forged token or a missing `openid` scope will never be fixed by logging
  in again - show an error with what to check instead of redirecting, or users get an endless login loop.
- How to re-acquire: inside the LINE app (`liff.isInClient()`), **`liff.login()` can't be used** - call
  `liff.logout()` then reload so `liff.init()` gets a fresh token; wherever `isInClient()` is false (external
  browsers - check it rather than assuming what LINE for PC does), `liff.logout()` then
  `liff.login({ redirectUri })`.
- Share one in-flight re-login across concurrent calls; allow at most one automatic re-login per couple of
  minutes, then show a manual "sign in again / reopen" button. `liff.logout()` clears the stored tokens, so
  calls that start while the redirect/reload is pending must wait for it instead of reading the token (they
  would otherwise fail with a misleading "no ID token" error, or call `liff.login()` inside the LIFF browser).
- Strip stale OAuth params (`code`, `state`, `error*`, `liffClientId`, `liffRedirectUri`, `liff.referrer`)
  from the redirect URI and merge `liff.state` params back into the query, or the next login breaks and users
  lose their place.
Re-check: `reference/liff/#get-id-token`, `reference/liff/#login`.

## 4. User IDs and providers

**LIFF userId != the bot's userId.** User IDs are issued per provider: the LINE Login channel hosting the
LIFF app is under a different provider than the Messaging API channel. Channels can't be moved between
providers, and there's no documented way to convert IDs. Fix: create a LINE Login channel + LIFF app under
the bot's provider, publish it (new channels start in "Developing", usable only by admins/testers), switch
`VITE_LIFF_ID` / the server's channel ID, replace old LIFF links in cards and rich menus, and plan for data
already stored under the old IDs. Compare against `events[].source.userId`, not the webhook's top-level
`destination` (that's the bot's own ID). Re-check: `docs/messaging-api/getting-user-ids/`,
`docs/line-developers-console/best-practices-for-provider-and-channel-management/`.

## 5. init, deep links and the in-app browser

- Call `liff.init()` once (memoise), at the endpoint URL or a path below it, before other LIFF APIs. In an
  external browser when not logged in, `liff.login({ redirectUri: location.href })` and wait on a promise
  that never resolves so nothing races the redirect.
- Read deep-link params from both the query and `liff.state`.
- In-app browser quirks: avoid native `alert`/`confirm`; wire the Android back button to history (otherwise it
  closes LIFF); inputs >= 16 px to avoid iOS zoom; open third-party sites that need the user's normal browser
  session with `liff.openWindow({ url, external: true })`. LIFF pages don't live-update: re-fetch on
  visibility/focus and lock buttons while a request runs.
- Features differ by environment (`sendMessages`, `shareTargetPicker`, `scanCodeV2`, friendship APIs) - check
  `liff.isApiAvailable()` and `docs/liff/differences-between-liff-browser-and-external-browser/`.
Re-check: `reference/liff/#initialize-liff-app`, `docs/liff/developing-liff-apps/`.

## 6. LINE Login web flow and sessions

- Use `state` (store in an HttpOnly cookie, compare, delete) and `nonce`; prefer PKCE; exchange the code
  server-side (`POST /oauth2/v2.1/token`); the callback URL must exactly match the console setting; email needs
  a separate permission application. Re-check: `docs/line-login/security-checklist/`.
- The flow is the easy part; **the session you create afterwards** is where it goes wrong. A LINE userId is an
  identifier, not a secret: never build session tokens from it (`session_<userId>_<ts>` is forgeable), never
  accept sessions via query string, and fail closed when an admin allow-list is empty. Use a signed or random
  opaque session (HttpOnly, Secure, SameSite=Lax). After verifying an ID token once, issuing your own session
  avoids per-request verification calls.
- "Add friend option" (`bot_prompt`) links the login to your Official Account: `docs/line-login/link-a-bot/`.
