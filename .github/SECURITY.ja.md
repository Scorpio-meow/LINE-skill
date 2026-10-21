# セキュリティポリシー

[繁體中文](/.github/SECURITY.md) | [English](/.github/SECURITY.en.md) | **日本語** | [ไทย](/.github/SECURITY.th.md) | [Bahasa Indonesia](/.github/SECURITY.id.md) | [한국어](/.github/SECURITY.ko.md)

## サポート対象のバージョン

修正するのは最新版、つまり `main` ブランチだけです。古いバージョンを使っている場合は、まず更新してください（更新方法は [README](/README.ja.md#更新と削除) を参照）。

## 脆弱性の報告

**公開の issue は作成しないでください。** GitHub の非公開の報告機能を使ってください：リポジトリの **Security** タブで **Report a vulnerability** をクリックするか、[こちらのリンク](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)を直接開きます。使えない場合は、件名に `[LINE-skill security]` を付けて yao921024@gmail.com にメールしてください。

次の情報を添えてください：

- 影響を受けるファイルとバージョン（commit）
- 再現手順と、どのような影響があるか
- 修正案（任意）

再現には偽の token と secret を使い、報告に本物の値を含めないでください。

## 対象範囲

本プロジェクトの脆弱性にあたるものの例：

- スクリプトが channel access token や channel secret を出力する、ファイルやキャッシュに書き込む、または `api.line.me`、`api-data.line.me` 以外のホストに送信する。
- `webhook_tools.py` が channel secret そのものを送信する（送るべきは署名だけです）。
- 書き込み系コマンドが `--yes` なしで実際に実行され、dry-run を迂回してしまう。
- パストラバーサルやコマンドインジェクション。例えば `line_docs.py` のページパスとキャッシュ、または `line_api.py` の `--env-file`、`@file` 引数によって、想定外の場所を読み書きしてしまう。
- `SKILL.md` や `references/` の指示によって、AI アシスタントがユーザーの同意なしに書き込み操作を実行する、token を漏らす、または検索したドキュメントの内容を指示として実行してしまう。

本プロジェクトの対象外のもの：

- **LINE プラットフォーム自体**（LINE アプリ、Messaging API、LIFF、LINE ログイン）の脆弱性：LINEヤフー株式会社（LY Corporation）の[公式窓口](https://bugbounty.linecorp.com/)に報告してください。
- **AI ツール自体**（Claude Code、Codex、Copilot など）の脆弱性：そのツールの開発元に報告してください。
- **自分の token が漏洩した**：本プロジェクトの脆弱性ではありません。すぐに [LINE Developers コンソール](https://developers.line.biz/console/)で token や secret を再発行または失効させてください。
- **gotchas の推奨内容が古い、または安全性が不十分**だが、悪用できる脆弱性ではない場合：通常の issue で構いません（「Outdated LINE info or broken link」テンプレート）。

## 対応の流れ

個人で管理しているオープンソースプロジェクトのため、決まった対応期限はありません。報告を受け取ったら、できるだけ早く次のように対応します。

1. 受け取ったことをお知らせします。
2. 問題と影響範囲を確認し、必要に応じて詳細をお尋ねします。
3. 修正後に新しいバージョンをリリースし、CHANGELOG を更新して、GitHub Security Advisory で公表します。ご希望であれば、公表の中で謝辞を記載します。

修正がリリースされるまでは、脆弱性の詳細を公開しないでください。

## 利用時に自分の token を守るには

- token と secret は環境変数に入れるか、`.env` に置いて `--env-file` で指定します。コマンドラインには直接書かないでください（シェルの履歴やプロセス一覧に残ります）。
- `.env` が `.gitignore` に含まれていることを確認してください。ツールが生成するプロジェクトによっては、デフォルトで無視されないことがあります（例：`supabase init`）。
- 書き込み系の操作は、まず dry-run の出力を確認し、問題がなければ `--yes` を付けてください。
- インストール前に `SKILL.md` と `scripts/` の中身を確認できます。skill はあなたの PC または AI ツールの実行環境でこれらのスクリプトを実行します。
