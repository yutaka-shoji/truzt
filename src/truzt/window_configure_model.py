"""This module defines the WindowConfigure class.

Classes:
    WindowConfigure: A class representing the configuration of a window, including attributes such
        as area, dimensions, input method, frame type, glass properties, and additional information.
"""

from typing import Literal, Optional

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import ConfigDict, Field, RootModel
from pydantic.alias_generators import to_camel

from .model_config import BaseConfigModel


class WindowConfigure(BaseConfigModel):
    """窓仕様.

    Attributes:
        window_area: 窓面積
        window_width: 窓の幅
        window_height: 窓の高さ
        input_method: 窓性能の入力方法
        frame_type: 建具の種類
        glass_id: ガラス建築確認記号
        layer_type: ガラスの層数
        glass_uvalue: ガラスの熱貫流率
        glass_ivalue: ガラスの日射熱取得率
        window_uvalue: 窓の熱貫流率
        window_ivalue: 窓の日射熱取得率
        info: 備考
    """

    # NOTE: builelibでここだけcamelCaseになっているのでその対応
    model_config = ConfigDict(alias_generator=to_camel)

    window_area: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_width: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_height: Optional[float] = Field(
        None,
        ge=0.0,
    )
    input_method: Optional[
        Literal[
            "性能値を入力",
            "ガラスの性能を入力",
            "ガラスの種類を入力",
        ]
    ] = Field(
        None,
    )
    frame_type: Optional[
        Literal[
            "樹脂製",
            "木製",
            "金属樹脂複合製",
            "金属木複合製",
            "金属製",
        ]
    ] = Field(
        None,
    )
    glass_id: Optional[str] = Field(
        None,
        alias="glassID",  # NOTE: for builelib compatibility
    )
    layer_type: Optional[Literal["複層", "単層"]] = Field(
        None,
        alias="layerType",  # NOTE: for builelib compatibility
    )
    glass_uvalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    glass_ivalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_uvalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_ivalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    info: Optional[str] = Field(
        None,
        alias="Info",  # NOTE: for builelib compatibility
    )


class WindowConfigures(RootModel):
    """WindowConfigure dict.

    Attributes:
        root: WindowConfigure dict.
    """

    root: dict[str, WindowConfigure]

    @classmethod
    def _create_window_data_by_performance(
        cls, ws: Worksheet, row: int, ref: dict, raw_frame_type: Optional[str] = None
    ) -> Optional[dict]:
        """性能値による窓データの生成.

        Args:
            ws: ワークシート
            row: 行番号
            ref: セル参照定義
            raw_frame_type: 建具種類の生の値

        Returns:
            生成した窓データ
        """
        u_value = ws[f"{ref['u_value']}{row}"].value
        i_value = ws[f"{ref['i_value']}{row}"].value
        glass_u = ws[f"{ref['glass_u']}{row}"].value
        glass_i = ws[f"{ref['glass_i']}{row}"].value

        if not (u_value and i_value):
            return None

        return {
            "input_method": "性能値を入力",
            "window_uvalue": float(u_value),
            "window_ivalue": float(i_value),
            "layer_type": "単層",
            "glass_uvalue": float(glass_u) if glass_u else None,
            "glass_ivalue": float(glass_i) if glass_i else None,
        }

    @classmethod
    def _create_window_data_by_glass_performance(
        cls, ws: Worksheet, row: int, ref: dict, raw_frame_type: Optional[str] = None
    ) -> Optional[dict]:
        """ガラス性能による窓データの生成.

        Args:
            ws: ワークシート
            row: 行番号
            ref: セル参照定義
            raw_frame_type: 建具種類の生の値

        Returns:
            生成した窓データ
        """
        glass_u = ws[f"{ref['glass_u']}{row}"].value
        glass_i = ws[f"{ref['glass_i']}{row}"].value

        if not (glass_u and glass_i):
            return None

        window_data = {
            "input_method": "ガラスの性能を入力",
            "glass_uvalue": float(glass_u),
            "glass_ivalue": float(glass_i),
        }

        if raw_frame_type:
            frame_info = cls._convert_frame_type(raw_frame_type)
            if frame_info:
                frame_type, layer_type = frame_info
                window_data["frame_type"] = frame_type
                window_data["layer_type"] = layer_type

        return window_data

    @classmethod
    def _create_window_data_by_glass_type(
        cls, ws: Worksheet, row: int, ref: dict, raw_frame_type: Optional[str] = None
    ) -> Optional[dict]:
        """ガラス種類による窓データの生成.

        Args:
            ws: ワークシート
            row: 行番号
            ref: セル参照定義
            raw_frame_type: 建具種類の生の値

        Returns:
            生成した窓データ
        """
        glass_type = ws[f"{ref['glass_type']}{row}"].value
        if not glass_type:
            return None

        window_data = {
            "input_method": "ガラスの種類を入力",
            "glass_id": glass_type,
        }

        if raw_frame_type:
            frame_info = cls._convert_frame_type(raw_frame_type)
            if frame_info:
                frame_type, _ = frame_info
                window_data["frame_type"] = frame_type

        return window_data

    @staticmethod
    def _convert_frame_type(frame_type: str) -> Optional[tuple[str, str]]:
        """建具の種類を変換する.

        Args:
            frame_type: エクセルファイルの建具種類

        Returns:
            変換後の建具種類とガラス層数のタプル、または None
        """
        if not frame_type:
            return None

        frame_type_mapping = {
            "木製(単板ガラス)": ("木製", "単層"),
            "木製(複層ガラス)": ("木製", "複層"),
            "樹脂製(単板ガラス)": ("樹脂製", "単層"),
            "樹脂製(複層ガラス)": ("樹脂製", "複層"),
            "樹脂": ("樹脂製", "複層"),
            "金属木複合製(単板ガラス)": ("金属木複合製", "単層"),
            "金属木複合製(複層ガラス)": ("金属木複合製", "複層"),
            "金属樹脂複合製(単板ガラス)": ("金属樹脂複合製", "単層"),
            "金属樹脂複合製(複層ガラス)": ("金属樹脂複合製", "複層"),
            "アルミ樹脂複合": ("金属樹脂複合製", "複層"),
            "金属製(単板ガラス)": ("金属製", "単層"),
            "金属製(複層ガラス)": ("金属製", "複層"),
            "アルミ": ("金属製", "複層"),
        }

        return frame_type_mapping.get(frame_type)

    @classmethod
    def _process_row(cls, ws: Worksheet, row: int, ref: dict) -> Optional[tuple[str, dict]]:
        """行データを処理する.

        Args:
            ws: ワークシート
            row: 行番号
            ref: セル参照定義

        Returns:
            キーとWindowConfigureデータのタプル、または None
        """
        # 開口部名称の取得
        key = ws[f"{ref['name']}{row}"].value
        if not key:
            return None

        # 基本データの作成
        window_data = {
            "window_area": 1,
            "window_width": None,
            "window_height": None,
        }

        # 建具種類の取得
        raw_frame_type = ws[f"{ref['frame_type']}{row}"].value

        # データ生成の試行
        additional_data = (
            cls._create_window_data_by_performance(ws, row, ref, raw_frame_type)
            or cls._create_window_data_by_glass_performance(ws, row, ref, raw_frame_type)
            or cls._create_window_data_by_glass_type(ws, row, ref, raw_frame_type)
        )

        if not additional_data:
            return None

        window_data.update(additional_data)

        # 備考の追加
        info = ws[f"{ref['info']}{row}"].value
        if info:
            window_data["info"] = info

        return key, window_data

    @classmethod
    def from_workbook(cls, wb: Workbook, ver: Literal["v2", "v3"] = "v3") -> "WindowConfigures":
        """WorkbookからWindowConfigureモデルを生成する.

        Args:
            wb: Workbook
            ver: WEBPRO input workbook version (v2 or v3).

        Returns:
            dict[str, WindowConfigure]: WindowConfigure dict
        """
        # セル参照の定義
        if ver == "v2":
            ref = {
                "sheet_name": "2-3) 窓仕様",
                "start_row": 11,
                "name": "A",  # 開口部名称
                "u_value": "B",  # 窓の熱貫流率
                "i_value": "C",  # 窓の日射熱取得率
                "frame_type": "D",  # 建具の種類
                "glass_type": "E",  # ガラスの種類
                "glass_u": "F",  # ガラスの熱貫流率
                "glass_i": "G",  # ガラスの日射熱取得率
                "info": "H",  # 備考
            }
        else:
            # TODO: v3のセル参照定義
            raise NotImplementedError

        # シートの取得
        ws = wb[ref["sheet_name"]]

        # データ格納用の辞書
        window_configures: dict[str, WindowConfigure] = {}

        # 行のループ
        empty_count = 0
        for row in range(ref["start_row"], ws.max_row + 1):
            # 連続して空欄が続いた場合はループを抜ける
            if empty_count > 20:
                break

            # 行の処理
            result = cls._process_row(ws, row, ref)
            if not result:
                empty_count += 1
                continue

            key, window_data = result

            # 既に同じ名称が存在する場合はスキップ
            if key in window_configures:
                continue

            # WindowConfigureモデルの作成と追加
            window_configures[key] = WindowConfigure(**window_data)

        return cls(root=window_configures)
