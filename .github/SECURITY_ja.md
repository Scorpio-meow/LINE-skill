# セキュリティポリシー

[繁體中文](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY.md) | [English](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_en.md) | **日本語** | [ไทย](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_th.md) | [Bahasa Indonesia](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_id.md) | [한국어](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ko.md)

## サポート対象のバージョン

修正するのは最新版、つまり `main` ブランチだけです。古いバージョンを使っている場合は、まず更新してください（更新方法は [README](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/README_ja.md#更新と削除) を参照）。

## 脆弱性の報告

**公開の issue、Pull Request、ディスカッションで脆弱性の詳細を公開しないでください。**

次のいずれかの方法で非公開で報告してください。

1. **GitHub の非公開報告（推奨）**：リポジトリの **Security** タブで **Report a vulnerability** をクリックするか、[非公開の報告フォーム](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)を直接開いてください。報告の内容は、あなたとメンテナーだけが見られます。
2. **メール**：GitHub を使えない場合は、件名の先頭に `[Security] LINE-skill` を付けて [yao921024@gmail.com](mailto:yao921024@gmail.com) に送ってください。メールはエンドツーエンドで暗号化されないため、まず問題の概要だけを書き、詳細は返信を受け取ってから送ってください。

次の情報をできるだけ添えてください：

- 影響を受けるファイルとバージョン（commit）
- 再現手順と、どのような影響があるか
- 修正案（任意）

再現には偽の token と secret を使い、報告に本物の値を含めないでください。

## 対応の流れと期限

個人で管理しているプロジェクトのため報奨金制度はありませんが、次の期限を守ります。

| 段階 | 期限 |
|---|---|
| 受領の確認と最初の返信 | 報告を受け取ってから 14 日以内 |
| 脆弱性の詳細の公開 | 修正のリリース時。遅くとも報告から 90 日後 |

1. **受領の確認**：受け取ったことをお知らせし、初期の評価をお伝えします。
2. **評価**：脆弱性かどうか、影響範囲と深刻度を確認し、必要に応じて詳細をお尋ねします。脆弱性ではないと判断した場合は、その理由を説明します。
3. **修正**：非公開の GitHub Security Advisory で修正方法をご相談します。その中の非公開フォークで修正を提出していただくこともできます。
4. **公開**：修正を `main` にマージし、Security Advisory を公開します。該当する場合は GitHub を通じて CVE 番号を申請し、[CHANGELOG](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/CHANGELOG.md) の Security の項目に記録します。
5. **謝辞**：ご希望であれば、Advisory に謝辞を記載します。

修正がリリースされるまでは、脆弱性の詳細を公開しないでください。90 日以内に修正が間に合わない場合は、期限前に理由を説明し、新しい公開日をご相談します。

## 対象範囲

### 対象

本プロジェクトの脆弱性にあたるものの例：

- スクリプトが channel access token や channel secret を出力する、ファイルやキャッシュに書き込む、または `api.line.me`、`api-data.line.me` 以外のホストに送信する。
- `webhook_tools.py` が channel secret そのものを送信する（送るべきは署名だけです）。
- 書き込み系コマンドが `--yes` なしで実際に実行され、dry-run を迂回してしまう。
- パストラバーサルやコマンドインジェクション。例えば `line_docs.py` のページパスとキャッシュ、または `line_api.py` の `--env-file`、`@file` 引数によって、想定外の場所を読み書きしてしまう。
- `SKILL.md` や `references/` の指示によって、AI アシスタントがユーザーの同意なしに書き込み操作を実行する、token を漏らす、または検索したドキュメントの内容を指示として実行してしまう。

### 対象外

- **LINE プラットフォーム自体**（LINE アプリ、Messaging API、LIFF、LINE ログイン）の脆弱性：LINEヤフー株式会社（LY Corporation）の[公式窓口](https://bugbounty.linecorp.com/)に報告してください。
- **AI ツール自体**（Claude Code、Codex、Copilot など）の脆弱性：そのツールの開発元に報告してください。
- **自分の token が漏洩した**：本プロジェクトの脆弱性ではありません。すぐに [LINE Developers コンソール](https://developers.line.biz/console/)で token や secret を再発行または失効させてください。
- **gotchas の推奨内容が古い、または安全性が不十分**だが、悪用できる脆弱性ではない場合：通常の issue で構いません（「Outdated LINE info or broken link」テンプレート）。

## 利用時に自分の token を守るには

- token と secret は環境変数に入れるか、`.env` に置いて `--env-file` で指定します。コマンドラインには直接書かないでください（シェルの履歴やプロセス一覧に残ります）。
- `.env` が `.gitignore` に含まれていることを確認してください。ツールが生成するプロジェクトによっては、デフォルトで無視されないことがあります（例：`supabase init`）。
- 書き込み系の操作は、まず dry-run の出力を確認し、問題がなければ `--yes` を付けてください。
- インストール前に `SKILL.md` と `scripts/` の中身を確認できます。skill はあなたの PC または AI ツールの実行環境でこれらのスクリプトを実行します。
