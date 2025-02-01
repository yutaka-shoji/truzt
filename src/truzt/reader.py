"""Excelファイルからのデータ読み込みに関する基底実装を提供するモジュール."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar

import yaml
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class ExcelReadError(Exception):
    """Excelファイルの読み込み時に発生するエラー."""

    sheet: str
    cell: str
    message: str

    def __str__(self) -> str:
        """エラーメッセージを文字列形式で返す.

        Returns:
            str: エラーメッセージ.
        """
        return f"Sheet '{self.sheet}' Cell '{self.cell}': {self.message}"


class ValidationMixin:
    """セルの検証機能を提供するMixin."""

    def validate_required_cells(self, sheet: str, required_cells: list[str]) -> None:
        """必須セルの存在チェック.

        Args:
            sheet: シート名.
            required_cells: 必須セルのアドレスリスト.

        Raises:
            ExcelReadError: 必須セルが存在しない場合.
        """
        worksheet = self._get_worksheet(sheet)  # type: ignore
        for cell in required_cells:
            if not worksheet[cell].value:
                raise ExcelReadError(sheet, cell, "必須セルが空です") from None

    def validate_cell_format(self, sheet: str, cell: str, format_type: str) -> None:
        """セルの形式チェック.

        Args:
            sheet: シート名.
            cell: セルのアドレス.
            format_type: 期待される形式 (e.g., "numeric", "text", "date").

        Raises:
            ExcelReadError: セルの形式が不正な場合.
        """
        worksheet = self._get_worksheet(sheet)  # type: ignore
        value = worksheet[cell].value

        if format_type == "numeric":
            try:
                float(value)
            except (ValueError, TypeError) as e:
                raise ExcelReadError(sheet, cell, "数値形式である必要があります") from e
        elif format_type == "text":
            if not isinstance(value, str):
                raise ExcelReadError(sheet, cell, "文字列形式である必要があります") from None


class ExcelReader(ABC, Generic[T], ValidationMixin):
    """ExcelファイルからWEBPROデータを読み込む基底クラス.

    genericなT型をパラメータとして持ち、ValidationMixinを継承しています.
    T型はpydanticのBaseModelを継承している必要があります.
    """

    def __init__(self, workbook: Workbook, version: Literal["v2", "v3"]) -> None:
        """リーダーの初期化.

        Args:
            workbook: openpyxlのWorkbookオブジェクト.
            version: WEBPROのバージョン ("v2" or "v3").
        """
        self.wb = workbook
        self.version = version
        self.cell_mapping = self._load_cell_mapping()

    def _load_cell_mapping(self) -> dict:
        """バージョンに応じたセル座標マッピングを読み込む.

        Returns:
            dict: マッピング定義の辞書.
        """
        config_dir = Path(__file__).parent / "config"
        mapping_file = config_dir / "cell_mapping.yaml"

        with open(mapping_file) as f:
            mappings = yaml.safe_load(f)

        # コンポーネント名をプロパティから取得
        # プロパティが実装されていない場合はクラス名から推測
        try:
            component_name = self._component_name  # type: ignore
        except AttributeError:
            component_name = self.__class__.__name__.lower().replace("reader", "")

        if component_name not in mappings:
            raise ValueError(f"セル座標マッピングが定義されていません: {component_name}")

        version_mapping = mappings[component_name].get(self.version)
        if not version_mapping:
            raise ValueError(f"バージョン {self.version} のマッピングが定義されていません")

        return version_mapping

    def _get_worksheet(self, name: str) -> Worksheet:
        """ワークシートを取得.

        Args:
            name: シート名.

        Returns:
            Worksheet: ワークシートオブジェクト.

        Raises:
            ExcelReadError: シートが存在しない場合.
        """
        try:
            return self.wb[name]
        except KeyError as e:
            raise ExcelReadError("", name, f"シート '{name}' が存在しません") from e

    def read_cell(self, sheet: str, address: str, optional: bool = False) -> Any:
        """セルの値を読み込み、適切な型に変換.

        Args:
            sheet: シート名.
            address: セルのアドレス.
            optional: 必須でない場合True.

        Returns:
            Any: セルの値.

        Raises:
            ExcelReadError: セルが存在しないか値の取得に失敗した場合.
        """
        try:
            worksheet = self._get_worksheet(sheet)
            value = worksheet[address].value

            if value is None and not optional:
                raise ExcelReadError(sheet, address, "セルが空です") from None

            return value

        except Exception as e:
            if not optional:
                raise ExcelReadError(sheet, address, str(e)) from e
            return None

    @abstractmethod
    def read(self) -> T:
        """モデルの読み込みを実装.

        Returns:
            T: 読み込んだモデルオブジェクト.
        """
        pass
