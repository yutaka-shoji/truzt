"""This module defines the WallConfigure class and the Layer class.

Classes:
    Layer: A class representing a building material layer.
    WallConfigure: A class representing the configuration of a wall.
"""

from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class Layer(BaseConfigModel):
    """建材レイヤー.

    Attributes:
        material_id: 断熱材の種類
        conductivity: 熱伝導率
        thickness: 厚み
        info: 備考
    """

    material_id: Optional[str] = Field(
        None,
        alias="materialID",  # NOTE: for builelib compatibility
    )
    conductivity: Optional[float] = Field(
        None,
        gt=0.0,
        alias="conductivity",  # NOTE: for builelib compatibility
    )
    thickness: Optional[float] = Field(
        None,
        ge=0,
        alias="thickness",  # NOTE: for builelib compatibility
    )
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

    wall_type_webpro: Literal["外壁", "接地壁"] = Field(
        None,
        alias="wall_type_webpro",  # NOTE: for builelib compatibility
    )

    structure_type: Literal[
        "木造",
        "鉄筋コンクリート造等",
        "鉄骨造",
        "その他",
    ] = Field(
        None,
        alias="structureType",  # NOTE: for builelib compatibility
    )

    solar_absorption_ratio: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        alias="solarAbsorptionRatio",  # NOTE: for builelib compatibility
    )

    input_method: Optional[Literal["熱貫流率を入力", "建材構成を入力", "断熱材種類を入力"]] = Field(
        None,
        alias="inputMethod",  # NOTE: for builelib compatibility
    )

    material_id: Optional[str] = Field(
        None,
        alias="materialID",  # NOTE: for builelib compatibility
    )

    conductivity: Optional[float] = Field(
        None,
        ge=0.0,
        alias="conductivity",  # NOTE: for builelib compatibility
    )

    layers: Optional[list[Layer]] = Field(
        None,
        alias="layers",  # NOTE: for builelib compatibility
    )

    thickness: Optional[float] = Field(
        None,
        gt=0,
        alias="thickness",  # NOTE: for builelib compatibility
    )

    uvalue: Optional[float] = Field(
        None,
        gt=0.0,
    )

    info: Optional[str] = None
