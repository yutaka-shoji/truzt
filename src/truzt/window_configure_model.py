"""This module defines the WindowConfigure class.

Classes:
    WindowConfigure: A class representing the configuration of a window, including attributes such
        as area, dimensions, input method, frame type, glass properties, and additional information.
"""

from typing import Literal, Optional

from openpyxl import Workbook
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

    @staticmethod
    def _convert_frame_type(frame_type: str) -> Optional[str]:
        """建具の種類を変換する.

        Args:
            frame_type: エクセルファイルの建具種類

        Returns:
            変換後の建具種類
        """
        if not frame_type:
            return None

        # 括弧を含む場合は、括弧前の部分を取得
        frame_type = frame_type.split("(")[0]

        # 変換マップ
        conversion = {
            "樹脂アルミ複合": "金属樹脂複合製",
            "アルミ樹脂複合": "金属樹脂複合製",
            "木アルミ複合": "金属木複合製",
            "アルミ木複合": "金属木複合製",
            "金属": "金属製",
        }
        return conversion.get(frame_type, frame_type)

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
            # 開口部名称の取得
            key = ws[f"{ref['name']}{row}"].value

            # 連続して空欄が続いた場合はループを抜ける
            if empty_count > 20:
                break

            # 開口部名称が空欄の場合はスキップ
            if not key:
                empty_count += 1
                continue

            # 既に同じ名称が存在する場合はスキップ
            if key in window_configures:
                continue

            # 基本データの作成
            window_data = {
                "window_area": 1,
                "window_width": None,
                "window_height": None,
            }

            # 入力方法の判定と各種データの取得
            u_value = ws[f"{ref['u_value']}{row}"].value
            i_value = ws[f"{ref['i_value']}{row}"].value
            glass_u = ws[f"{ref['glass_u']}{row}"].value
            glass_i = ws[f"{ref['glass_i']}{row}"].value
            glass_type = ws[f"{ref['glass_type']}{row}"].value

            if u_value and i_value:
                window_data.update(
                    {
                        "input_method": "性能値を入力",
                        "window_uvalue": float(u_value),
                        "window_ivalue": float(i_value),
                        "layer_type": "単層",
                        "glass_uvalue": float(glass_u) if glass_u else None,
                        "glass_ivalue": float(glass_i) if glass_i else None,
                    }
                )
            elif glass_u and glass_i:
                raw_frame_type = ws[f"{ref['frame_type']}{row}"].value
                window_data["input_method"] = "ガラスの性能を入力"
                if raw_frame_type:
                    frame_type = cls._convert_frame_type(raw_frame_type)
                    if frame_type:
                        window_data["frame_type"] = frame_type
                window_data.update(
                    {
                        "glass_uvalue": float(glass_u),
                        "glass_ivalue": float(glass_i),
                    }
                )
            elif glass_type:
                raw_frame_type = ws[f"{ref['frame_type']}{row}"].value
                window_data["input_method"] = "ガラスの種類を入力"
                if raw_frame_type:
                    frame_type = cls._convert_frame_type(raw_frame_type)
                    if frame_type:
                        window_data["frame_type"] = frame_type
                window_data["glass_id"] = glass_type

            # 備考の追加
            info = ws[f"{ref['info']}{row}"].value
            if info:
                window_data["info"] = info

            # WindowConfigureモデルの作成と追加
            window_configures[key] = WindowConfigure(**window_data)

        return cls(root=window_configures)
