# truzt プロジェクト作業計画書

## プロジェクト概要

truztは、WEBPROシミュレーションツールの入力ファイル（Excelファイル）をPydanticを使用してバリデーションし、JSONに変換するPythonパッケージです。このプロジェクトは、既存のbuilelibパッケージの機能を改良し、より堅牢なデータ検証と変換を実現することを目指しています。

## 作業進捗

### 1. 基盤整備フェーズ
1. Excel読み込み基盤の実装
   - [x] ExcelReaderベースクラスの作成
   - [x] セル座標定義の外部化 (cell_mapping.yaml)
   - [x] ValidationMixinの実装
   - [x] ExcelReadErrorの実装

2. 既存実装の改善
   - [x] BuildingとRoomsのリファクタリング
   - [x] 新しい基盤クラスへの移行
   - [x] テストケースの拡充

### 2. buielibの実装理解フェーズ
builelibのmake_inputdata.pyの処理フローを理解し，コードの可読性とメンテナンス性を向上させるための最小限のリファクタリングを行う．詳細な作業計画は[builelib実装理解フェーズ作業計画書](builelib_understanding.md)を参照．

主な作業内容：
1. コード構造の把握
   - 処理フローの理解
   - シート処理パターンの整理
   - 重複処理の特定

2. リファクタリング実装
   - 共通処理のメソッド化
   - コードの構造化
   - 命名規則の統一

3. テスト整備
   - シート読み込みテスト
   - データ変換テスト
   - エラーケーステスト

主な成果物：
- make_inputdata_refactored.py: リファクタリング実装
- test_make_inputdata.py: テストコード
- 処理パターンと共通処理の説明ドキュメント

### 3. 新規コンポーネント実装フェーズ
- [ ] Air Conditioning Zone
- [ ] Wall Configure
- [ ] Window Configure
- [ ] Envelope Set
- [ ] Shading Configure
- [ ] Heat Source System
- [ ] Secondary Pump System
- [ ] Air Handling System
- [ ] Ventilation Room
- [ ] Ventilation Unit
- [ ] Lighting Systems
- [ ] Hot Water Room
- [ ] Hot Water Supply Systems
- [ ] Elevators
- [ ] Photovoltaic Systems
- [ ] Cogeneration Systems
- [ ] Special Input Data

### 4. バリデーション強化フェーズ 
- [ ] フィールドの制約条件の実装
- [ ] クロスバリデーションルールの実装
- [ ] エラーメッセージの日本語化

### 5. ドキュメント整備フェーズ
- [ ] APIドキュメントの作成
- [ ] 使用方法のガイドの作成
- [ ] サンプルコードの追加

## ディレクトリ構造

```
.
├── LICENSE
├── README.md
├── builelib # 独立パッケージ (参考) 
│   ├── LICENSE
│   ├── MANIFEST.in
│   ├── README.md
│   ├── builelib
│   ├── builelib_cmd.py
│   ├── builelib_run.py
│   ├── builelib_run_AC.py
│   ├── calc_standard_energy_AC.py
│   ├── docs
│   ├── requirements.txt
│   ├── sample
│   ├── setup.py
│   └── tests
├── docs
│   ├── CONTRIBUTING.md
│   ├── implementation_plan.md
│   ├── index.md
│   ├── javascripts
│   └── license.md
├── mkdocs.yml
├── out
├── pyproject.toml
├── sample # WEBPROexcelファイルおよび等価なjson, csvのサンプル
│   ├── sample_input_v2.json
│   ├── sample_input_v2.xlsm
│   ├── sample_input_v2_csv/ # sample_input_v2.xlsxの内容がシートごとにcsv出力されたものが保存されている　
│   ├── sample_input_v3.json
│   ├── sample_input_v3.xlsx
│   └── sample_input_v3_csv/ # sample_input_v3.xlsxの内容がシートごとにcsv出力されたものが保存されている　
├── scripts
│   └── gen_ref_pages.py # mkdocs用
├── src
│   └── truzt/ # truztの本実装
└── tests # testスクリプト
```

## 現状
- データモデルは Pydantic を使用して実装済み
- Excel -> JSON 変換機能は Building と Room のみ実装済み
- JSON -> オブジェクト変換とバリデーションは実装済み

## 目標
sample/sample_input_v3.xlsx から sample/sample_input_v3.json と同等のJSONを生成できるようにする

## 実装すべき機能一覧

以下の各コンポーネントについて、Excelファイルからの読み込み機能を実装する必要があります：

- [x] Building (実装済・要改善)
- [x] Rooms (実装済・要改善)
- [ ] Air Conditioning Zone
- [ ] Wall Configure
- [ ] Window Configure
- [ ] Envelope Set
- [ ] Shading Configure
- [ ] Heat Source System
- [ ] Secondary Pump System
- [ ] Air Handling System
- [ ] Ventilation Room
- [ ] Ventilation Unit
- [ ] Lighting Systems
- [ ] Hot Water Room
- [ ] Hot Water Supply Systems
- [ ] Elevators
- [ ] Photovoltaic Systems
- [ ] Cogeneration Systems
- [ ] Special Input Data

## 既存実装の改善事項

### 1. Excel読み込み基盤の整備
1. ExcelReaderベースクラスの作成
   ```python
   class ExcelReader:
       def __init__(self, workbook: Workbook, version: Literal["v2", "v3"]):
           self.wb = workbook
           self.version = version
           self._load_cell_mapping()
   
       def _load_cell_mapping(self):
           """バージョンに応じたセル座標マッピングを読み込む"""
           pass
   
       def read_cell(self, sheet: str, address: str) -> Any:
           """セルの値を読み込み、適切な型に変換"""
           pass
   
       @abstractmethod
       def read(self) -> BaseConfigModel:
           """モデルの読み込みを実装"""
           pass
   ```
   
2. セル座標定義の外部化
   ```yaml
   # cell_mapping.yaml
   building:
     v2:
       name: C9
       region: C12
       # ...
     v3:
       name: C9
       region: C12
       # ...
   ```
   
3. バリデーション機能の強化
   ```python
   class ValidationMixin:
       def validate_required_cells(self, required_cells: list[str]):
           """必須セルの存在チェック"""
           pass
   
       def validate_cell_format(self, cell: str, format_type: str):
           """セルの形式チェック"""
           pass
   ```
   
4. エラーハンドリングの改善
   ```python
   class ExcelReadError(Exception):
       def __init__(self, sheet: str, cell: str, message: str):
           self.sheet = sheet
           self.cell = cell
           self.message = message
           super().__init__(f"Sheet '{sheet}' Cell '{cell}': {message}")
   ```
   
### 2. 共通ユーティリティの整備
1. 型変換ユーティリティ
   ```python
   def convert_value(value: Any, target_type: type) -> Any:
       """セルの値を指定された型に変換"""
       pass
   ```
   
2. セル操作ユーティリティ
   ```python
   def get_cell_value(ws, address: str) -> Any:
       """セルの値を安全に取得"""
       pass
   ```
   
3. バリデーションユーティリティ
   ```python
   def validate_numeric_range(value: float, min_val: float, max_val: float):
       """数値範囲の検証"""
       pass
   ```

## 実装手順

### 1. 基盤整備フェーズ
1. Excel読み込み基盤の実装
   - ExcelReaderベースクラスの作成
   - セル座標定義の外部化
   - 共通バリデーション機能の実装
   - エラーハンドリング機能の実装
   
2. 既存実装の改善
   - BuildingとRoomsのリファクタリング
   - 新しい基盤クラスへの移行
   - テストケースの拡充
   
### 2. 新規コンポーネント実装フェーズ
1. コンポーネントごとに以下の作業を実施：
   - Excel上のデータ配置の調査
   - データマッピング定義の作成
   - 読み込みクラスの実装
   - 単体テストの作成
   - 結合テストの作成
   
### 3. バリデーション強化フェーズ
1. 各フィールドの制約条件の確認と実装
2. クロスバリデーションルールの実装
3. エラーメッセージの日本語化
   
### 4. ドキュメント整備フェーズ
1. APIドキュメントの作成
2. 使用方法のガイド作成
3. サンプルコードの追加
   
## テスト戦略

### 1. 単体テスト
1. 各コンポーネントの読み込みテスト
   - 正常系テスト
   - 異常系テスト
   - エッジケースのテスト
   
2. バリデーションテスト
   - 型チェック
   - 範囲チェック
   - 必須項目チェック
   - クロスバリデーション
   
3. エラーハンドリングテスト
   - セル不正テスト
   - データ不整合テスト
   - 型変換エラーテスト
   
### 2. 結合テスト
1. sample_input_v3.xlsx を使用した全体テスト
   
## マイルストーン

### 1. フェーズ1: 基盤整備 
- Excel読み込み基盤の実装
- 既存実装の改善
- テスト環境の整備

### 2. フェーズ2: 主要機能実装 
- 高優先度コンポーネントの実装
- 基本的なバリデーション機能の実装
- 初期テストの実施

### 3. フェーズ3: 補完的機能実装 
- 残りのコンポーネントの実装
- 高度なバリデーション機能の追加
- 総合テストの実施

### 4. フェーズ4: 最終調整 
- パフォーマンス最適化
- ドキュメント整備
- リリース準備

## 注意事項

1. 既存のbuilelibとの互換性維持
2. エラーメッセージは日本語で分かりやすく
3. 適切な例外処理の実装

## 定期的なレビュー項目

1. コードの品質
   - 可読性
   - メンテナンス容易性
   - 適切なドキュメンテーション

2. テストカバレッジ
   - 各コンポーネントの機能テスト

## レビュー記録

### 2024-01-28
#### 基盤整備フェーズの完了確認
- BuildingとRoomの基盤クラス移行が完了
- test_webpro_reader.pyの全テストが正常に通過
  - Excel V3ファイルの読み込みテスト
  - BuildingReaderのテスト
  - RoomReaderのテスト
  - エラーハンドリングのテスト
- 基盤整備フェーズの全タスクが完了
- 次のフェーズ（新規コンポーネント実装）への移行準備が整った

### 2024-02-01
#### builelib実装理解フェーズの完了確認
- make_inputdata.pyの処理フロー分析が完了
  - 全体構造の図式化
  - シート別処理パターンの整理
  - データ読み込み・バリデーションパターンの分類
- リファクタリングによる実装理解が深化
  - make_inputdata_refactored.pyの作成
  - test_make_inputdata.pyによるテスト整備
  - 共通パターンの抽出と文書化
- 実装パターンガイドの整備
  - Readerクラス実装パターンの定義
  - テストパターンの体系化
  - ベストプラクティスの文書化
- 次のフェーズ（空調ゾーン実装）への移行準備が完了
