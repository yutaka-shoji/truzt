"""This module defines the VentilationUnit class.

Classes:
    VentilationUnit: A class representing a ventilation unit.
"""

from typing import Literal, Optional, Union

from pydantic import Field

from .model_config import BaseConfigModel


class VentilationUnit(BaseConfigModel):
    """Ventilation unit.

    Attributes:
        number: 台数
        fan_air_volume: 設計風量
        motor_rated_power: 定格電動機出力
        power_consumption: 定格消費電力
        high_efficiency_motor: 高効率電動機の有無
        inverter: インバータの有無
        air_volume_control: 送風量制御
        ventilation_room_type: 対象室の用途
        ac_cooling_capacity: 必要冷却能力
        ac_ref_efficiency: 熱源効率(一次換算値)
        ac_pump_power: ポンプの定格消費電力
        info: 備考
    """

    number: int = Field(ge=0)
    fan_air_volume: Optional[float] = Field(ge=0.0)
    motor_rated_power: Optional[float] = Field(
        ge=0.0,
        alias="MoterRatedPower",  # NOTE: for builelib compatibility (TYPO)
    )
    power_consumption: Optional[float] = Field(ge=0.0)
    high_efficiency_motor: Literal["有", "無"]
    inverter: Literal["有", "無"]
    air_volume_control: Literal["無", "CO濃度制御", "温度制御"]
    ventilation_room_type: Optional[
        Union[Literal["電気室", "機械室", "エレベータ機械室", "その他"], float]
    ]
    ac_cooling_capacity: Optional[float] = Field(
        ge=0.0,
        alias="AC_CoolingCapacity",  # NOTE: for builelib compatibility
    )
    ac_ref_efficiency: Optional[float] = Field(
        ge=0.0,
        alias="AC_RefEfficiency",  # NOTE: for builelib compatibility
    )
    ac_pump_power: Optional[float] = Field(
        ge=0.0,
        alias="AC_PumpPower",  # NOTE: for builelib compatibility
    )
    info: Optional[str]
