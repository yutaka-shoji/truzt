"""This module defines the WallConfigure class and the Layer class.

Classes:
    Layer: A class representing a building material layer.
    WallConfigure: A class representing the configuration of a wall.
"""

from typing import Annotated, Literal, Optional

from openpyxl import Workbook
from pydantic import Field, RootModel

from .model_config import BaseConfigModel


class Layer(BaseConfigModel):
    """建材レイヤー.

    Attributes:
        material_id: 断熱材の種類
        conductivity: 熱伝導率
        thickness: 厚み
        info: 備考
    """

    material_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="materialID",  # NOTE: for builelib compatibility
        ),
    ]
    conductivity: Annotated[
        Optional[float],
        Field(None, gt=0.0, alias="conductivity"),  # NOTE: for builelib compatibility
    ]
    thickness: Annotated[
        Optional[float],
        Field(
            None,
            ge=0,
            alias="thickness",  # NOTE: for builelib compatibility
        ),
    ]
    info: Optional[str] = None


class WallConfigure(BaseConfigModel):
    """外壁構成.

    Attributes:
        wall_type_webpro: 外壁の種類(WEBPRO)
        structure_type: 構造種別
        solar_absorption_ratio: 日射吸収率
        input_method: 断熱性能の入力方法
        material_id: 断熱材の種類
        conductivity: 熱伝導率
        layers: list of Layer instance
        thickness: 厚み
        uvalue: 熱貫流率
        info: 備考
    """

    wall_type_webpro: Annotated[
        Optional[Literal["外壁", "接地壁"]],
        Field(
            None,
            alias="wall_type_webpro",  # NOTE: for builelib compatibility
        ),
    ]

    structure_type: Annotated[
        Optional[
            Literal[
                "木造",
                "鉄筋コンクリート造等",
                "鉄骨造",
                "その他",
            ]
        ],
        Field(
            None,
            alias="structureType",  # NOTE: for builelib compatibility
        ),
    ]

    solar_absorption_ratio: Annotated[
        Optional[float],
        Field(
            None,
            ge=0.0,
            le=1.0,
            alias="solarAbsorptionRatio",  # NOTE: for builelib compatibility
        ),
    ]

    input_method: Annotated[
        Optional[Literal["熱貫流率を入力", "建材構成を入力", "断熱材種類を入力"]],
        Field(
            None,
            alias="inputMethod",  # NOTE: for builelib compatibility
        ),
    ]

    material_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="materialID",  # NOTE: for builelib compatibility
        ),
    ]

    conductivity: Annotated[
        Optional[float],
        Field(
            None,
            ge=0.0,
            alias="conductivity",  # NOTE: for builelib compatibility
        ),
    ]

    layers: Annotated[
        Optional[list[Layer]],
        Field(
            None,
            alias="layers",  # NOTE: for builelib compatibility
        ),
    ]

    thickness: Annotated[
        Optional[float],
        Field(
            None,
            gt=0,
            alias="thickness",  # NOTE: for builelib compatibility
        ),
    ]

    uvalue: Annotated[
        Optional[float],
        Field(
            None,
            gt=0.0,
        ),
    ]

    info: Optional[str] = None


class WallConfigures(RootModel):
    """WallConfigure dict.

    Attributes:
        root: WallConfigure dict.
    """

    root: dict[str, WallConfigure]

    @classmethod
    def from_workbook(cls, wb: Workbook, ver: Literal["v2", "v3"] = "v3") -> "WallConfigures":
        """WorkbookからWallConfigureモデルを生成する.

        Args:
            wb: Workbook
            ver: WEBPRO input workbook version (v2 or v3).

        Returns:
            dict[str, WallConfigure]: 外壁構成
        """
        # セル参照の定義
        if ver == "v2":
            ref = {
                "sheet_name": "2-2) 外壁構成 ",
                "start_row": 11,
                "name": "A",  # 外壁名称
                "wall_type": "B",  # 壁の種類
                "u_value": "C",  # 熱貫流率
                "material_id": "E",  # 建材名称
                "conductivity": "F",  # 熱伝導率（Rev.2のみ）
                "thickness": {"rev2": "G", "default": "F"},  # 厚み
                "solar_absorption_ratio": "H",  # 日射吸収率（Rev.2のみ）
                "info": {"rev2": "I", "default": "G"},  # 備考
            }
        else:
            # TODO: v3のセル参照定義
            raise NotImplementedError

        # シートの取得
        ws = wb[ref["sheet_name"]]

        # バージョン判定
        is_rev2 = ws["A1"].value.endswith("Rev.2")

        # データ格納用の辞書
        wall_configures: dict[str, WallConfigure] = {}

        # 行のループ
        empty_count = 0
        for row in range(ref["start_row"], ws.max_row + 1):
            # 外壁名称の取得
            key = ws[f"{ref['name']}{row}"].value

            # 連続して空欄が続いた場合はループを抜ける
            if empty_count > 20:
                break

            # 外壁名称が空欄の場合はスキップ
            if not key:
                empty_count += 1
                continue

            # 既に同じ名称が存在する場合はスキップ
            if key in wall_configures:
                continue

            # 外壁の基本情報を作成
            wall_data = {
                "wall_type_webpro": ws[f"{ref['wall_type']}{row}"].value,
                "structure_type": "その他",
                "solar_absorption_ratio": (
                    ws[f"{ref['solar_absorption_ratio']}{row}"].value if is_rev2 else None
                ),
            }

            # 熱貫流率の入力があるかチェック
            u_value = ws[f"{ref['u_value']}{row}"].value
            if u_value:
                wall_data["input_method"] = "熱貫流率を入力"
                wall_data["uvalue"] = float(u_value)
                info_col = ref["info"]["rev2" if is_rev2 else "default"]
                wall_data["info"] = ws[f"{info_col}{row}"].value
            else:
                wall_data["input_method"] = "建材構成を入力"
                layers = []

                # 建材構成の読み取り（最大9層）
                for layer_row in range(1, 10):
                    current_row = row + layer_row
                    material_id = ws[f"{ref['material_id']}{current_row}"].value

                    # 建材名称が空欄の場合はスキップ
                    if not material_id:
                        continue

                    thickness_col = ref["thickness"]["rev2" if is_rev2 else "default"]
                    info_col = ref["info"]["rev2" if is_rev2 else "default"]

                    # レイヤー情報の作成
                    layers.append(
                        Layer(
                            material_id=material_id,
                            conductivity=float(ws[f"{ref['conductivity']}{current_row}"].value)
                            if is_rev2 and ws[f"{ref['conductivity']}{current_row}"].value
                            else None,
                            thickness=float(ws[f"{thickness_col}{current_row}"].value)
                            if ws[f"{thickness_col}{current_row}"].value
                            else None,
                            info=ws[f"{info_col}{current_row}"].value,
                        )
                    )

                wall_data["layers"] = layers

            # WallConfigureモデルの作成と追加
            wall_configures[key] = WallConfigure(**wall_data)

        return cls(root=wall_configures)
