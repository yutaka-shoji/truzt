"""Module for defining the ShadingConfigure model."""

from typing import Literal, Optional

from openpyxl import Workbook
from pydantic import Field, RootModel

from .model_config import BaseConfigModel


class ShadingConfigure(BaseConfigModel):
    """shading configure model.

    Attributes:
        shading_effect_c: shading effect coefficient for cooling
        shading_effect_h: shading effect coefficient for heating
        x1: NOT IMPLEMENTED
        x2: NOT IMPLEMENTED
        x3: NOT IMPLEMENTED
        y1: NOT IMPLEMENTED
        y2: NOT IMPLEMENTED
        y3: NOT IMPLEMENTED
        zx_plus: NOT IMPLEMENTED
        zx_minus: NOT IMPLEMENTED
        zy_plus: NOT IMPLEMENTED
        zy_minus: NOT IMPLEMENTED
        info:
    """

    shading_effect_c: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
    )

    shading_effect_h: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
    )

    # not implemented also in builelib
    # builelibでは日除けの形状って書いてあった
    x1: Optional[float] = None
    x2: Optional[float] = None
    x3: Optional[float] = None
    y1: Optional[float] = None
    y2: Optional[float] = None
    y3: Optional[float] = None
    zx_plus: Optional[float] = None
    zx_minus: Optional[float] = None
    zy_plus: Optional[float] = None
    zy_minus: Optional[float] = None
    info: Optional[str] = None


class ShadingConfigures(RootModel):
    """ShadingConfigure dict.

    Attributes:
        root: ShadingConfigure dict.
    """

    root: dict[str, ShadingConfigure]

    @classmethod
    def from_workbook(cls, wb: Workbook, ver: Literal["v2", "v3"] = "v3") -> "ShadingConfigures":
        """WorkbookからShadingConfiguresモデルを生成する.

        Args:
            wb: Workbook
            ver: WEBPRO input workbook version (v2 or v3).

        Returns:
            dict[str, ShadingConfigures]: ShadingConfigure dict
        """
        if ver == "v2":
            return cls._from_workbook_v2(wb)
        else:
            # TODO: v3のセル参照定義
            raise NotImplementedError("v3 is not implemented yet")

    @classmethod
    def _from_workbook_v2(cls, wb: Workbook) -> "ShadingConfigures":
        """WorkbookからShadingConfiguresモデルを生成する (v2).

        Args:
            wb: Workbook

        Returns:
            ShadingConfigures: ShadingConfigure dict
        """
        # シート名と開始行の定義
        sheet_name = "2-4) 外皮 "
        start_row = 11  # DATA_START_ROW + 1 (0-indexedから1-indexedへの変換)

        # シートの取得
        try:
            ws = wb[sheet_name]
        except KeyError:
            # シートが存在しない場合は空のデータを返す
            return cls(root={})

        # データ格納用の辞書
        shading_configures: dict[str, ShadingConfigure] = {}

        # 庇の番号
        eaves_num = 0

        # 行のループ
        empty_count = 0
        for row in range(start_row, ws.max_row + 1):
            # 連続して空欄が続いた場合はループを抜ける
            if empty_count > 20:
                break

            # セルの値を取得
            shade_c_cell = ws.cell(row=row, column=4)  # 日よけ効果係数（冷房）
            shade_h_cell = ws.cell(row=row, column=5)  # 日よけ効果係数（暖房）

            # セルの値を安全に取得
            shade_c = shade_c_cell.value
            shade_h = shade_h_cell.value

            # 日よけ効果係数の処理
            if shade_c and shade_h:
                # 庇IDの生成
                eaves_id = f"庇{eaves_num}"
                eaves_num += 1

                # 型変換を安全に行う
                try:
                    # 文字列に変換してから浮動小数点に変換
                    shade_c_str = str(shade_c) if shade_c is not None else ""
                    shade_h_str = str(shade_h) if shade_h is not None else ""

                    shade_c_float = float(shade_c_str) if shade_c_str else None
                    shade_h_float = float(shade_h_str) if shade_h_str else None
                except (ValueError, TypeError):
                    # 変換できない場合はスキップ
                    empty_count += 1
                    continue

                # 日よけデータの作成
                shading_data = {
                    "shading_effect_c": shade_c_float,
                    "shading_effect_h": shade_h_float,
                    "x1": None,
                    "x2": None,
                    "x3": None,
                    "y1": None,
                    "y2": None,
                    "y3": None,
                    "zx_plus": None,
                    "zx_minus": None,
                    "zy_plus": None,
                    "zy_minus": None,
                    "info": None,
                }

                # ShadingConfigureモデルの作成と追加
                shading_configures[eaves_id] = ShadingConfigure(**shading_data)
            else:
                empty_count += 1
                continue

            # 空行カウンタをリセット
            empty_count = 0

        return cls(root=shading_configures)
