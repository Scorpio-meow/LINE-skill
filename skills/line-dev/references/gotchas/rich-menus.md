# Gotchas: rich menus

Field-tested failure modes, checked against the official docs. Each entry: **symptom or rule -> cause ->
fix**, plus the page to re-check (paths relative to `https://developers.line.biz/en/`). Numbers marked
"(at the time of writing)" were checked in 2026-10.

**Upload fails with 400 ("The image size is not allowed for richmenu").** Image requirements at the time of
writing: JPEG/PNG, width 800-2500 px, height >= 250 px, width/height >= 1.45, <= 1 MB. Exported design PNGs
are often over 1 MB - export JPEG or quantize the palette (keep the pixel size). `line_api.py
richmenu-validate menu.json --image menu.png` checks locally, plus the API validator when a token is set.
Re-check: `reference/messaging-api/#upload-rich-menu-image-requirements`.

**Taps hit the wrong button.** `areas[].bounds` are in `size` coordinates: make the image exactly `size`
pixels and keep every area inside it. (The reference only requires x, y >= 0, so an area that runs past the
edge may not be rejected - but that part can't be tapped and it's almost always a typo.) `chatBarText` has a
short limit (14 characters at the time of writing).

**You can't replace a menu's image.** Create a new menu, upload, switch the default/links, *then* delete the
old one (deleting first leaves users without a menu). Find previous menus by `name` so scripts are
re-runnable; support a dry run. Creation/deletion is rate-limited (100/hour at the time of writing) and a
channel holds a limited number of menus (1000), so clean up. Because nothing can be edited after creation,
confirm placeholder URLs/labels before going live.

**Menu doesn't change for some users.** Priority: per-user (API) > default (API) > default set in LINE
Official Account Manager. Default changes apply when the user re-opens the chat (up to about a minute);
per-user links work only for friends. Re-check: `docs/messaging-api/rich-menus-overview/#rich-menu-display`.

**Where rich menus don't show:** group chats, and LINE for PC (macOS/Windows). If desktop users or groups
need an entry point, reply to any 1:1 message with a card that opens your LIFF app (free reply), and turn off
the account's auto-reply so users don't get two answers.

**Tabs:** rich menu aliases + `richmenuswitch` actions (`docs/messaging-api/switch-rich-menus/`).

**Deploying for someone:** validate locally and with the API, show the plan (create -> upload to
api-data.line.me -> set default), note the current default (for rollback), get a go-ahead if it replaces
the menu every user sees, then run it and confirm with `richmenu-default`. `line_api.py richmenu-deploy` does
this sequence with a dry run first.
