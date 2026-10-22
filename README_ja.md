# LINE-skill

[繁體中文](README.md) | [English](README_en.md) | **日本語** | [ไทย](README_th.md) | [Bahasa Indonesia](README_id.md) | [한국어](README_ko.md)

AI コーディングアシスタント向けの Agent Skill **`line-dev`** です。Claude、Codex、GitHub Copilot、Cursor、Gemini CLI などのツールが、LINE プラットフォームの開発・デバッグ・運用をより確実に行えるようにします。対象は Messaging API の Webhook、応答／プッシュメッセージとメッセージ通数、Flex Message、リッチメニュー、グループ向けボット、LIFF、LINE ログインです。

オープンな [Agent Skills](https://agentskills.io) 形式（フォルダー＋`SKILL.md`）を採用しているので、この形式に対応したツールならどれでも使えます。インストール方法は[クイックスタート](#クイックスタート)を参照してください。

- **仕様は必ずその場で公式ドキュメントを確認**：skill にはドキュメントの写しを含めず、「トピック → 公式 URL」の索引と検索スクリプトだけを同梱しています。数値・制限・料金が関わるときは、AI がその場で GitHub 上の公式 Markdown 原稿（developers.line.biz の同期元）を確認し、developers.line.biz の出典を添えます。
- **実戦で見つけた落とし穴リスト**：署名検証には raw body を使う、Webhook には約 2 秒以内に応答する、応答トークンは一度きりですぐに失効する、グループへのプッシュは人数分カウントされる、未認証アカウントではグループメンバーを一覧取得できない、textV2 のメンションの書き方とエスケープ、Flex のサイズと URI の制限、リッチメニュー画像の制限と優先順位、LIFF の ID トークンの有効期限とバックエンドでの検証、プロバイダーが違うと userId が一致しない……。どれも「症状 → 原因 → 対処 → 公式ページ」の形でまとめています。
- **LINE API を直接操作**：Python 標準ライブラリだけで動くスクリプトを同梱しています。書き込み系の操作はデフォルトで dry-run のみで、確認後に `--yes` を付けたときだけ実際に実行します。token／secret は環境変数か `.env` からのみ読み込み、出力には表示しません。

> 本プロジェクトは LINEヤフー株式会社（LY Corporation）の公式プロジェクトではありません。LINE は LINEヤフー株式会社の商標です。

## クイックスタート

[`skills`](https://github.com/vercel-labs/skills) コマンド 1 行でインストールできます。PC 上の AI ツールを検出して、それぞれのフォルダーに配置します。

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g` はユーザーディレクトリにインストールします（すべてのプロジェクトで使用可能）。`-g` を外すと現在のプロジェクトにだけインストールします。
- 特定のツールにだけ入れる場合は `-a` を付けます（例：`-a claude-code -a codex`）。各ツールの値は[次の節の表](#ツール別の-skill-フォルダー)を参照してください。
- [Bun](https://bun.sh) がない場合は、`bunx` を `npx` に置き換えても使えます。

インストール後、LINE 開発に関する質問をすると自動的に有効になります。例：

> LINE ボットの応答トークンはどれくらいで失効しますか？

skill が読み込まれていれば、回答はまず公式ドキュメントを確認し、developers.line.biz へのリンクを添えます。初めてスクリプトを実行するとき、多くのツールはコマンドの実行やネットワーク接続の許可を求めます。

各ツールへの手動インストールやその他の方法は次の節を参照してください。

## インストール

**Python 3.8 以上**が必要です（スクリプトは標準ライブラリのみを使うので、パッケージのインストールは不要です）。公式ドキュメントの検索には `raw.githubusercontent.com` または `github.com` への接続が、LINE API の直接操作には `api.line.me` への接続が必要です。

### ツール別の skill フォルダー

手動インストールでは、`line-dev` フォルダーをツールが読み込む skill フォルダーにコピーし、`SKILL.md` が `<skill フォルダー>/line-dev/SKILL.md` に来るようにします。個人用フォルダーはこの PC 上のすべてのプロジェクトで使えます。プロジェクト用フォルダーはプロジェクトのルート直下に置くもので、commit すればチームで共有できます。

| ツール | `-a` の値 | 個人用フォルダー | プロジェクト用フォルダー | 手動で呼び出す |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex（CLI、IDE 拡張機能、ChatGPT デスクトップアプリ） | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` または `$line-dev` |
| GitHub Copilot（VS Code、Copilot CLI、JetBrains） | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | Agent のチャットで `/` を入力して選択 |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | `/skills list` で読み込まれたか確認できる |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop（旧 Windsurf） | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | `/` を入力して選択 |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` または `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

Windows では `~` はユーザーフォルダー（`%USERPROFILE%`）を指します。どのツールも会話に関係があれば自動で skill を使います。「手動で呼び出す」列は、明示的に指定したいときの方法です。

- Codex、Copilot、Cursor、Gemini CLI、OpenCode、Devin Desktop、Junie、Roo Code は `~/.agents/skills/` も読み込むので、複数のツールを使う場合はここに 1 つ置けば共有できます。Claude Code が読み込むのは `~/.claude/skills/` だけです。
- `bunx skills` は skill を共有の `.agents/skills/`（`-g` 指定時は `~/.agents/skills/`）に置き、ほかのツール用にリンクを作成します。インストール後にツールが読み込まない場合は、下の手動インストールで表のフォルダーに配置してください。
- 表にないツール（Amp、Goose、Kilo Code、Trae、Qwen Code など）も `bunx skills` でインストールできます。`-a` の値は [skills の README](https://github.com/vercel-labs/skills) を参照してください。
- Devin Desktop は Windsurf 時代の `~/.codeium/windsurf/skills/` と `.windsurf/skills/` も引き続き読み込みます。

以下は `~/.agents/skills/` にコピーする例です。ほかのツールの場合は `TARGET` を表のパスに置き換えてください。

macOS／Linux：

```bash
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
TARGET=~/.agents/skills
mkdir -p "$TARGET"
cp -r LINE-skill/skills/line-dev "$TARGET/"
```

Windows PowerShell：

```powershell
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
$TARGET = "$HOME\.agents\skills"
New-Item -ItemType Directory -Force $TARGET | Out-Null
Copy-Item -Recurse -Force LINE-skill\skills\line-dev "$TARGET\"
```

ツールが新しい skill を検出しない場合は、一度再起動してください。

### その他のインストール方法

独自のインストールコマンドを持つツールもあります。

- **GitHub CLI**（2.90 以上。`gh skill` は現在 public preview）：`--agent` の値は表の `-a` と同じです。

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**：Codex で次のように入力します。

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  Codex はデフォルトでサンドボックス内でネットワークなしでコマンドを実行するため、スクリプトがドキュメントを検索したり LINE API を呼び出したりするときに承認を求めます。常に許可する場合は、`~/.codex/config.toml` に次を追加します。

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**：clone したあと `copilot skill add LINE-skill/skills/line-dev` を実行します。セッションの途中で追加した場合は `/skills reload` で読み込みます。リポジトリの `.github/skills/` に置いて commit すれば、クラウドで動く Copilot cloud agent も使います。
- **Gemini CLI**：デフォルトではユーザースコープにインストールされます。`--scope workspace` を付けると現在のプロジェクトにだけインストールします。

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**：Kiro パネルの **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub** を選びます。URL は skill があるサブフォルダーを指定してください：`https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`。
- **Devin Desktop**：Cascade パネル右上の **⋯** → **Skills** で skill を管理できます。
- **Cline**：新しい skill はデフォルトで有効です。Cline パネル下部の **Skills** タブで切り替えられます。

### Claude アプリ（Web 版／デスクトップ版）

1. コード実行を有効にします。Pro・Max プランは **Settings > Capabilities** で「Code execution and file creation」をオンにします。Team・Enterprise プランは、組織のオーナーが組織設定で「Code execution and file creation」と「Skills」をオンにします。
2. `line-dev.zip` を自分で作成します。ZIP の最上位は `line-dev/` フォルダーである必要があります。GitHub の「Download ZIP」はリポジトリ全体（最上位が `LINE-skill-main/`）なので、そのままではアップロードできません。展開するかリポジトリを clone してから、`line-dev` フォルダーだけを圧縮してください。
   - macOS／Linux：`LINE-skill/skills` フォルダーで `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'` を実行します。
   - Windows：エクスプローラーで `skills\line-dev` フォルダーを右クリック →「ZIP ファイルに圧縮する」（Windows 10 では「送る → 圧縮 (zip 形式) フォルダー」）。
3. **Customize > Skills** で **+** → **Create skill** → **Upload a skill** を選び、ZIP をアップロードします。画面が **Settings > Capabilities** の場合は、Skills セクションの **Upload skill** をクリックします。

アップロードした skill は自分のアカウントでしか使えません。組織全体で使うには、組織のオーナーによるプロビジョニングが必要です。アプリのコード実行環境は通常、パッケージマネージャーや `github.com` など一部のドメインにしか接続できません。`line_docs.py` は `raw.githubusercontent.com` に接続できないと自動的に `github.com` から同じドキュメントを取得しますが、`line_api.py` が必要とする `api.line.me` にはデフォルトで接続できません。Team・Enterprise プランでは、組織のオーナーが組織設定の Capabilities で許可するドメインを追加できます。LINE API を直接操作するなら、自分の PC で Claude Code などのツールを使うことをおすすめします。画面が変わった場合は[公式ヘルプ](https://support.claude.com/en/articles/12512180-using-skills-in-claude)に従ってください。

### ChatGPT

[公式ヘルプ](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)によると、ChatGPT の skill は現在 Business、Enterprise、Healthcare、Edu プランの対象ユーザーに提供されており、アップロードできるかどうかはワークスペースの設定で決まります。

1. 前の節の方法で `line-dev.zip` を用意します。
2. サイドバーの **Plugins** → **Skills** タブで **Create** → **Upload from your computer** を選び、ZIP をアップロードします。
3. 会話で `@` を入力して `line-dev` を選ぶか、ChatGPT に自動で判断させます。

ChatGPT と Codex の skill は現在同期されないため、Codex を使う場合は別途インストールしてください。LINE API を直接操作するなら、自分の PC で Codex などのツールを使うことをおすすめします。

### 更新と削除

| インストール方法 | 更新 | 削除 |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | `line-dev` フォルダーを削除 |
| Gemini CLI | 削除して再インストール | `gemini skills uninstall line-dev` |
| 手動コピー | `LINE-skill` フォルダーで `git pull` を実行し、もう一度コピー | `line-dev` フォルダーを削除 |
| Claude アプリ、ChatGPT | 古いものを削除して新しい ZIP をアップロード | Skills ページで削除 |

### 各ツールの公式ドキュメント

パスや画面が変わった場合は公式ドキュメントに従ってください：[Claude Code](https://code.claude.com/docs/en/skills)・[Claude アプリ](https://support.claude.com/en/articles/12512180-using-skills-in-claude)・[ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)・[OpenAI Codex](https://learn.chatgpt.com/docs/build-skills)・[GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)・[VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)・[Cursor](https://cursor.com/docs/skills)・[Gemini CLI](https://geminicli.com/docs/cli/skills/)・[Google Antigravity](https://antigravity.google/docs/skills)・[Devin Desktop](https://docs.devin.ai/desktop/cascade/skills)・[OpenCode](https://opencode.ai/docs/skills)・[Cline](https://docs.cline.bot/customization/skills)・[Kiro](https://kiro.dev/docs/skills/)・[JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html)・[Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/)・[skills](https://github.com/vercel-labs/skills)・[gh skill](https://cli.github.com/manual/gh_skill_install)

## スクリプトの使い方

skill はこれらのスクリプトを自動で呼び出しますが、直接使うこともできます。Python 3.8 以上が必要で、パッケージのインストールは不要です（Windows では `python` または `py -3`）。

```bash
# 公式ドキュメントを検索（その場で取得し 1 日キャッシュ。git があれば全文検索に対応）
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API：token は環境変数に入れるか、--env-file でプロジェクトの .env を指定
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # ボット情報
python3 skills/line-dev/scripts/line_api.py quota                    # 今月の上限と使用量
python3 skills/line-dev/scripts/line_api.py validate push card.json  # メッセージ形式を検証（送信はしない）
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "テスト"        # dry-run：送信内容を表示するだけ
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "テスト" --yes  # 実際に送信
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# Webhook のデバッグ：secret は環境変数に入れる
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest` は 4 つのリクエストを順に送ります：LINE Developers コンソールの「検証」（空の `events`）、正しい署名のイベント、誤った署名、署名なし。あわせて、応答が LINE の 2 秒のタイムアウトを超えていないかも確認します。

## 内容

```
skills/line-dev/
├── SKILL.md                      # メインの説明（AI 向け、英語）
├── references/
│   ├── doc-map.md                # 公式ドキュメントの索引：URL の規則、ページ一覧、API リファレンスのアンカー、OpenAPI、ステータスページ、提供終了のお知らせ
│   └── gotchas/                  # 実戦の落とし穴と設計パターン。トピック別のファイルで、AI は必要なものだけ読む
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # 公式ドキュメントをその場で検索：全文検索、API リファレンスの節、ガイドページを取得（引用できる URL 付き）
    ├── line_api.py               # Messaging API 操作 CLI（dry-run 優先）
    └── webhook_tools.py          # 署名の計算・検証、LINE からの Webhook 送信を模擬、ワンコマンドの selftest
evals/                            # この skill の開発に使ったテストシナリオ
.github/                          # コミュニティ文書（コントリビューションガイド、行動規範、セキュリティポリシー、アクセシビリティ方針）と issue／PR テンプレート
```

## 安全設計

- push／multicast／broadcast、Webhook の設定、リッチメニューの公開・デフォルト設定・削除、ボットのグループ退出などの書き込み操作は、`--yes` がなければ dry-run だけを行います。まず検証し、完全なリクエストに加えて、送信先の種類、グループの人数（グループへのプッシュは人数分カウントされる）、今月の残り通数を表示します。
- メッセージ送信時には自動で `X-Line-Retry-Key` を付けるので、タイムアウト後に再試行しても重複して送信されません。
- `line_api.py` は `api.line.me` と `api-data.line.me` にのみ、`line_docs.py` はドキュメント取得のため GitHub にのみ接続し、`webhook_tools.py` は指定した URL にのみリクエストを送ります（送るのは署名で、secret は送りません）。token／secret が出力に表示されることはありません。
- skill はあなたの PC（または AI ツールの実行環境）でスクリプトを実行します。インストール前に `SKILL.md` と `scripts/` の中身を確認できます。

## 公式ドキュメント

この skill が参照する公式ドキュメントは、[LINE Developers](https://developers.line.biz/) と、その Markdown 原稿 [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source)（README で AI ツールでの利用が明示的に許可されています）です。公式ドキュメントは継続的に更新されるため、skill には索引だけを置き、写しは含めていません。

## テスト

`evals/evals.json` は、この skill の開発に使った 5 つのテストシナリオです：Webhook の 401 のデバッグ、グループボットの仕様確認、リッチメニューの公開、LIFF でのユーザー認証、グループボットのコードレビュー。採点基準は合計 49 項目です。`evals/files/richmenu/` はわざとエラーを仕込んだリッチメニューの素材です。`fake-env.txt` はランダムに生成した偽の token で、シナリオ 3 を実行するときは作業フォルダーにコピーして `.env` に名前を変えてください（問題文で token が `.env` にあるとしているため）。

直近の比較（Claude Opus 5.5、各シナリオを skill あり／なしで 1 回ずつ実行、ブラインド採点）：skill ありは 47/49、skill なしは 44/49 で、skill ありのほうが平均 16% 速く完了しました。差が最も大きかったのは LIFF（非推奨バージョンの LIFF SDK に関するセキュリティ上の注意、token が失効したときだけ再ログインする）と、リッチメニューの公開（token をコマンドラインに載せない、公開前に確認する）です。その後、通らなかった 2 項目に合わせて skill を修正し、シナリオ 1 と 5 を再実行したところすべて合格し、5 シナリオ合計で skill ありは 49/49 になりました。トリガーテスト（使うべき 10 文と、似ているが使うべきでない 10 文を各 3 回）はすべて正しく判定されました。

## コントリビューション

古くなった LINE の仕様の報告、落とし穴の追加、スクリプトやドキュメントの改善を歓迎します。

- 流れ、skill の方針、変更の確認方法：[コントリビューションガイド](.github/CONTRIBUTING_ja.md)
- [行動規範](.github/i18n/CODE_OF_CONDUCT_ja.md)
- セキュリティの脆弱性は公開の issue にせず、[セキュリティポリシー](.github/SECURITY_ja.md)に従って非公開で報告してください。
- アクセシビリティの状況と既知の制限：[アクセシビリティ方針](.github/ACCESSIBILITY_ja.md)

## ライセンス

[MIT](LICENSE)
