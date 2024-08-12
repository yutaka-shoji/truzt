"""Module for defining the HotWaterSupplySystem model."""

from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class HeatSourceUnitItem(BaseConfigModel):
    """Heat source unit item.

    Attributes:
        usage_type: 給湯用途
        heat_source_type: 熱源機種
        number: 台数
        rated_capacity: 定格加熱能力
        rated_power_consumption: 定格消費電力
        rated_fuel_consumption: 定格燃料消費量(高位)
        info: 備考
    """

    usage_type: Optional[
        Literal[
            "給湯負荷用",
            "配管保温用",
            "貯湯槽保温用",
            "その他",
        ]
    ]

    heat_source_type: Optional[
        Literal[
            "ガス給湯機",
            "ガス給湯暖房機",
            "ボイラ",
            "石油給湯機(給湯単機能)",
            "石油給湯機(給湯機付ふろがま)",
            "家庭用ヒートポンプ給湯機",
            "業務用ヒートポンプ給湯機",
            "貯湯式電気温水器",
            "電気瞬間湯沸器",
            "真空式温水発生機",
            "無圧式温水発生機",
            "地域熱供給",
        ]
    ]

    number: Optional[int] = Field(gt=0)

    rated_capacity: Optional[float] = Field(gt=0.0)
    rated_power_consumption: Optional[float] = Field(ge=0.0)
    rated_fuel_consumption: Optional[float] = Field(ge=0.0)

    info: Optional[str] = None


class HotWaterSupplySystem(BaseConfigModel):
    """Hot water supply system.

    Attributes:
        heat_source_unit: list of HeatSourceUnitItem
        insulation_type: 配管保温仕様
        pipe_size: 配管最大口径 (mm)
        solar_system_area: 太陽熱利用 有効集熱面積 (m2)
        solar_system_direction: 太陽熱利用 集熱面の方位角 (deg)
        solar_system_angle: 太陽熱利用 集熱面の傾斜角 (deg)
        info: 備考
    """

    heat_source_unit: Optional[list[HeatSourceUnitItem]]

    insulation_type: Optional[
        Literal[
            "保温仕様1",
            "保温仕様2",
            "保温仕様3",
            "裸管",
        ]
    ] = None
    pipe_size: Optional[float] = Field(None, gt=0.0)

    solar_system_area: Optional[float] = Field(None, gt=0.0)
    solar_system_direction: Optional[float] = Field(None, ge=0.0, le=360.0)
    solar_system_angle: Optional[float] = Field(None, ge=0.0, le=360.0)

    info: Optional[str] = None
