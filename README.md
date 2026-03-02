# Zeronity課題 SNS製作

# ディレクトリ構成

* bock :: サーバーサイドプロジェクト
* docs :: アプリを構成するにあたっての文書
* front :: Webブラウザ（クライアント）サイドプロジェクト
* artifacts :: SQLスクリプトなど
* README.md :: 今読んでいる文書
* AGENTS.md :: 生成AI向け文書

# 開発環境

## back
Python製となります

* パッケージマネージャー :: uv
* フレームワーク :: Flask

## front
JavaScript製となります

* パッケージマネージャー :: pnpm
* フレームワーク :: Svelte

## articafts

DBは一旦SQLite。他、環境構築にあたっての構成管理ツール用のソースコードを置く予定

# docsの内容に関して

## Mermaid( `*.mmd` )ファイルについて

図式の編集ファイルとなります。[mermaid-cli](https://github.com/mermaid-js/mermaid-cli) などで画像出力する事。例：

* `npx -p @mermaid-js/mermaid-cli mmdc -i fig_class.mmd -o fig_class.svg`
* `pnpm --package=@mermaid-js/mermaid-cli dlx mmdc -i fig_class.mmd -o fig_class.svg`

なお、生成した図式ファイルはリポジトリでは管理対象外とします。
