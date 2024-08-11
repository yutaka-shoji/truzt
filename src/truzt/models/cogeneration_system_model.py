from typing import Literal, Optional, Union

from pydantic import Field, field_validator, field_serializer

from .model_config import BaseConfigModel


class CogenerationSystem(BaseConfigModel):
    """Cogeneration system

    Attributes:
        rated_capacity: 定格発電出力 (kW)
        number: 台数
        power_generation_efficiency_100: 発電効率 負荷率1.00
        power_generation_efficiency_75: 発電効率 負荷率0.75
        power_generation_efficiency_50: 発電効率 負荷率0.50
        heat_generation_efficiency_100: 排熱効率 負荷率1.00
        heat_generation_efficiency_75: 排熱効率 負荷率0.75
        heat_generation_efficiency_50: 排熱効率 負荷率0.50
        heat_recovery_priority_cooling: 排熱利用優先順位 空調冷熱源
        heat_recovery_priority_heating: 排熱利用優先順位 空調温熱源
        heat_recovery_priority_hot_water: 排熱利用優先順位 給湯
        is_24hour_operation: 24時間運転の有無
        cooling_system: 排熱利用系統 空調 冷熱
        heating_system: 排熱利用系統 空調 温熱
        hot_water_system: 排熱利用系統 給湯
        info: 備考
    """

    rated_capacity: Optional[float] = Field(None, gt=0.0)
    number: Optional[int] = Field(None, gt=0)
    power_generation_efficiency_100: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="PowerGenerationEfficiency_100",
    )
    power_generation_efficiency_75: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="PowerGenerationEfficiency_75",
    )
    power_generation_efficiency_50: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="PowerGenerationEfficiency_50",
    )
    heat_generation_efficiency_100: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="HeatGenerationEfficiency_100",
    )
    heat_generation_efficiency_75: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="HeatGenerationEfficiency_75",
    )
    heat_generation_efficiency_50: Optional[float] = Field(
        None,
        gt=0.0,
        le=1.0,
        alias="HeatGenerationEfficiency_50",
    )
    heat_recovery_priority_cooling: Optional[
        Literal[
            "1番目",
            "2番目",
            "3番目",
        ]
    ] = None
    heat_recovery_priority_heating: Optional[
        Literal[
            "1番目",
            "2番目",
            "3番目",
        ]
    ] = None
    heat_recovery_priority_hot_water: Optional[
        Literal[
            "1番目",
            "2番目",
            "3番目",
        ]
    ] = None
    is_24hour_operation: Optional[bool] = Field(
        None,
        alias="24hourOperation",
    )
    cooling_system: Optional[str] = None
    heating_system: Optional[str] = None
    hot_water_system: Optional[str] = Field(
        None,
        alias="HowWaterSystem",  # builelibのタイポ対応
    )
    info: Optional[str] = None

    @field_validator("is_24hour_operation", mode="before")
    @classmethod
    def convert_to_bool(cls, arg: Union[str, bool]):
        if arg == "有":
            arg = True
        elif arg == "無":
            arg = False
        elif isinstance(arg, bool):
            arg = arg
        else:
            raise ValueError("must be '有' or '無' or boolean")
        return arg

    @field_serializer("is_24hour_operation")
    def convert_to_str(self, arg: bool):
        if arg:
            str_arg = "有"
        else:
            str_arg = "無"
        return str_arg
