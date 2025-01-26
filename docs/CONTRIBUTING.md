# Contribution Guideline

このドキュメントでは, truztプロジェクトへの貢献方法について説明します.

## 開発環境のセットアップ

### 1. uvのインストール

このプロジェクトでは[uv](https://github.com/astral-sh/uv)を使用して, Python環境とパッケージ管理を行います.
uvのインストール手順は手元の環境によって公式ドキュメントを参照してください．

### 2. プロジェクトのセットアップ

```bash
# プロジェクトディレクトリで仮想環境を作成し, 依存関係をインストール
uv sync
```

### 3. pre-commitのセットアップ

このプロジェクトでは, コードの品質を保つためにpre-commitを使用しています.以下のコマンドでセットアップしてください：

```bash
pre-commit install
```

これにより, コミット時に以下のチェックが自動的に実行されます：
- commitizen: コミットメッセージの形式チェック
- ruff: コードの静的解析とフォーマット
- pyright: 型チェック


## 開発プロセス

### 1. 新しい機能の開発やバグ修正

1. プロジェクトをフォークし, ローカルにクローンします
2. 既存のissueを確認し, 同様の内容がないことを確認します
3. 新規のissueを作成し, 実装内容について説明します
4. 新しいブランチを作成
5. 変更を加えます
6. 必要に応じテストを実行
7. プルリクエストを作成

### 2. コードスタイル

このプロジェクトでは, [ruff](https://github.com/astral-sh/ruff)を使用してコードスタイルを管理し, [pyright](https://github.com/microsoft/pyright)を使用して型チェックを行っています.

#### 2.1 Ruff

主なルール:

- 行の最大長: 100文字
- docstringスタイル: Google形式
- インポートの自動整理
- 型アノテーションの必須化（テストファイルを除く）

手動でコードをフォーマットする場合：
```bash
ruff check --fix .  # リンターによる自動修正
ruff format .       # コードフォーマット
```

#### 2.2 Pyright

Pyrightは型チェックを行い, 以下を確認します：

- すべての関数とメソッドの型アノテーション
- 変数の型の整合性
- オプショナルな値の適切な処理
- 未定義の属性へのアクセス

設定は`pyproject.toml`の`[tool.pyright]`セクションで管理されています.

#### 2.3 VSCode Extensions

VSCodeでの開発では以下の拡張を推奨します：

- Linter, Formatter: [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- Python Type Check: [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- Typo Check: [Typos spell checker](https://marketplace.visualstudio.com/items?itemName=tekumara.typos-vscode)

### 3. プルリクエストの作成

1. 変更をコミットし, プッシュします
2. GitHubでプルリクエストを作成します
3. プルリクエストのタイトルと説明には以下を含めてください：
> - 変更の目的
> - 変更の概要
> - 関連するIssue番号

### 4. レビュープロセス

1. CIチェックがすべてパスすることを確認します
2. レビュアーからのフィードバックに基づいて必要な修正を行います
3. 承認を得たら, 変更がマージされます

## ヘルプが必要な場合

- バグを見つけた場合は, GitHubのIssueを作成してください
- 質問がある場合は, GitHubのDiscussionsを使用してください

ご協力ありがとうございます！
