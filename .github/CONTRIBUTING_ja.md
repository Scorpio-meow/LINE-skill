# コントリビューションガイド

[繁體中文](/.github/CONTRIBUTING.md) | [English](/.github/CONTRIBUTING_en.md) | **日本語** | [ไทย](/.github/CONTRIBUTING_th.md) | [Bahasa Indonesia](/.github/CONTRIBUTING_id.md) | [한국어](/.github/CONTRIBUTING_ko.md)

協力していただきありがとうございます！本プロジェクトに参加する際は[行動規範](/.github/i18n/CODE_OF_CONDUCT_ja.md)を守ってください。

issue や PR は、README にあるどの言語（繁體中文、English、日本語、ไทย、Bahasa Indonesia、한국어）で書いても構いません。返信は繁体字中国語か英語になることがあります。

> 本プロジェクトは LINEヤフー株式会社（LY Corporation）の公式プロジェクトではありません。LINE プラットフォーム自体（LINE アプリ、Messaging API、LIFF、LINE ログイン）の問題は LINE の公式窓口に報告してください。

## 協力できること

| やりたいこと | 方法 |
|---|---|
| インストールや使い方の質問、話し合いたいアイデア | [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions) で質問する |
| LINE の仕様が変わった、ドキュメントのリンクが切れている、skill の数値が古い | 「Outdated LINE info or broken link」（LINE の情報が古い・リンク切れ）の issue を作成し、公式の出典を添える |
| skill に書かれていない落とし穴にはまった | 「Feature request or new gotcha」（新機能・新しい落とし穴）の issue を作成するか、`references/gotchas/` に追加する PR を直接送る |
| スクリプトがエラーになる、skill どおりに動いた AI が間違える | 「Bug report」（バグ報告）の issue を作成する |
| ドキュメントが分かりにくい、翻訳の誤り、アクセシビリティの問題 | 該当する issue を作成するか、PR を直接送る |
| セキュリティの脆弱性 | **issue は作成せず**、[SECURITY.md](/.github/SECURITY_ja.md) に従って非公開で報告する |

大きめの変更（スクリプトの新しいコマンド、`SKILL.md` の手順の変更、gotcha ファイルの追加）は、作業が無駄にならないよう、先に issue で相談してください。

## この skill の原則

変更する前に [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md) を読んでください。PR は次の点に沿ってレビューします。

1. **公式ドキュメントの写しを含めない。** skill に置くのは「トピック → 公式 URL」の索引と検索スクリプトだけで、仕様は必ずその場で [LINE Developers](https://developers.line.biz/) を確認します。公式ドキュメントをまとめてリポジトリに貼り付けないでください。引用するときは URL か、`line_docs.py` で検索できる節の名前を書きます。
2. **落とし穴の項目は形式が決まっています**：**症状またはルール → 原因 → 対処**の順に書き、`Re-check:` で再確認すべき公式ページを添えます（パスは `https://developers.line.biz/en/` からの相対パス）。変わりうる数値には「(at the time of writing)」と付け、ファイル冒頭の確認年月も更新してください。
3. **`SKILL.md` は AI が読むためのもの**：英語で、短く正確に書きます。詳細は `references/` に置き、1 トピック 1 ファイルにして、AI が必要なものだけ読めるようにします。
4. **スクリプトは Python 3.8 以上の標準ライブラリだけを使う**：サードパーティのパッケージは追加しません。
5. **token と secret の扱いを緩めない**：環境変数か `--env-file` からのみ読み込み、出力にも表示せず、ファイルにも書き込みません。`line_api.py` が接続するのは `api.line.me` と `api-data.line.me` だけ、`line_docs.py` は GitHub だけです。`webhook_tools.py` はユーザーが指定した URL にだけリクエストを送り、送るのは署名だけです。
6. **書き込み系の操作はデフォルトで dry-run**：`--yes` がなければ、実際に送信したり設定を変更したりできないようにします。新しく追加する書き込み系コマンドもこれに従い、`SKILL.md` の Safety tiers に載せてください。

## 開発環境

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

編集中のバージョンを AI ツールに直接読み込ませるには、skill フォルダーをツールの skill フォルダーにリンクします（インストール済みの `line-dev` は先に削除してください）。以下は Claude Code の例です。ほかのツールのフォルダーは [README](/README_ja.md#ツール別の-skill-フォルダー) を参照してください。

macOS／Linux：

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell（junction の作成に管理者権限は不要です）：

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## 変更の確認

現時点では自動テストはありません。少なくとも次のコマンドは実行してください（Windows では `python` または `py -3`）。

```bash
# 3 つのスクリプトがすべて起動すること（構文エラーはここで分かる）
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# token 不要の実際の操作
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **Python 3.8 との互換性**：3.9 以降で追加された構文や関数（`list[str]` の型ヒント、`str.removeprefix`、`match` など）は使わないでください。[uv](https://docs.astral.sh/uv/) があれば、次のように 3.8 で実行できます：`uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`。
- **Webhook 関連の機能を変更した場合**：ローカルの Webhook に対して `webhook_tools.py selftest <url>` を実行してください。
- **`line_api.py` の書き込み系コマンドを変更した場合**：`--yes` を付けないときはリクエストを表示するだけで、実際には送信しないことを確認してください。本物のチャネルでテストするときは、自分のテスト用アカウントを使ってください。
- **`SKILL.md` や gotchas を変更し、AI の動作に影響しうる場合**：[`evals/evals.json`](/evals/evals.json) の関連するテストシナリオを変更前と変更後に 1 回ずつ実行し、各シナリオの `expectations` と照らし合わせて採点して、合格数を PR に書いてください。方法は問いません。AI ツールに問題文を貼り付けて、人の目で照らし合わせて採点しても構いません。大きなトピックを新しく追加するときは、テストシナリオも一緒に追加してもらえると助かります。

## ドキュメント

- [`README.md`](/README.md)（繁体字中国語）がメインのバージョンです。その内容を変更したら、ほかの言語版も一緒に更新してください。書けない言語は PR にその旨を書いておけば、メンテナーが補います。
- 注目すべき変更は [`CHANGELOG.md`](/CHANGELOG.md) の `[Unreleased]` に記録してください。形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に従います。

## Pull Request を送る

- 1 つの PR で行うことは 1 つだけにしてください。変更が小さいほどレビューしやすくなります。
- commit メッセージは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) 形式で書き、skill 自体を変更するときは `line-dev` スコープを付けます。例：`fix(line-dev): 擋下 line_docs.py 的路徑穿越`、`docs: 更新評測結果`。説明はどの言語で書いても構いません。
- **本物の token、secret、userId、groupId は絶対に commit しないでください。** サンプルやテスト素材には必ず偽の値を使ってください（`evals/files/richmenu/fake-env.txt` のようにランダムに生成したもの）。
- PR テンプレートに沿って、何をしたか、どうテストしたかを記入してください。

## ライセンス

あなたの貢献は本プロジェクトの [MIT ライセンス](/LICENSE)のもとで公開されます。
