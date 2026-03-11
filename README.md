# Zeronity課題 SNS製作

* おそらくActivityPub対応
* Instagramをあまり使ったことがない
  * え？　10年前のトイカメラ・セピア調の写真にサーバー側でして公開する "あの" サービスですよね？
* テストファースト
* ドメイン駆動設計

# ディレクトリ構成

* bock :: サーバーサイドプロジェクト(Domain, UseCase層)
* docs :: アプリを構成するにあたっての文書
* front :: Webブラウザ（クライアント）サイドプロジェクト(Presentation層)
* artifacts :: SQLスクリプトなど(Infrastructures層)
* README.md :: 今読んでいる文書
* AGENTS.md :: 生成AI向け文書

# 開発環境

## back(Domain, Usecase)
Python製となります

* パッケージマネージャー :: uv
* フレームワーク :: Flask

### テスト実行方法

``` sh
cd back
uv run tests/ 
```

### サーバー実行方法

``` sh
cd back
uv run python src/main.py
```

## front(Presentation)
JavaScript製となります

* パッケージマネージャー :: pnpm
* フレームワーク :: Svelte

## articafts(Infrastructures)

DBは一旦SQLite。他、環境構築にあたっての構成管理ツール用のソースコードを置く予定

# docsの内容に関して

## Mermaid( `*.mmd` )ファイルについて

図式の編集ファイルとなります。[mermaid-cli](https://github.com/mermaid-js/mermaid-cli) などで画像出力する事。例：

* `npx -p @mermaid-js/mermaid-cli mmdc -i fig_class.mmd -o fig_class.svg`
* `pnpm --package=@mermaid-js/mermaid-cli dlx mmdc -i fig_class.mmd -o fig_class.svg`

なお、生成した図式ファイルはリポジトリでは管理対象外とします。
