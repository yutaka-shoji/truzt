from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class SecondaryPumpItem(BaseConfigModel):
    """Secondary pump item

    Attributes:
        number: 台数
        rated_water_flow_rate: 定格流量
        rated_power_consumption: 定格消費電力
        control_type: 制御方式
        min_opening_rate: 最小流量比
        info: 備考
    """

    number: Optional[int] = Field(
        None,
        ge=0,
    )
    rated_water_flow_rate: Optional[float] = Field(
        None,
        ge=0.0,
    )
    rated_power_consumption: Optional[float] = Field(
        None,
        ge=0.0,
    )
    control_type: Optional[Literal["無", "定流量制御", "回転数制御"]] = Field(
        None,
        alias="ContolType",  # NOTE: for builelib compatibility (TYPO)
    )
    min_opening_rate: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
    )
    info: Optional[str] = None


class SecondaryPump(BaseConfigModel):
    """Secondary pump

    Attributes:
        temperature_difference: 設計温度差
        is_staging_control: 台数制御の有無
        secondary_pump: list of SecondaryPumpItem
    """

    temperature_difference: Optional[float] = Field(
        None,
        ge=0.0,
    )
    is_staging_control: Optional[Literal["有", "無"]] = Field(
        None,
        alias="isStagingControl",  # NOTE: for builelib compatibility
    )
    secondary_pump: Optional[list[SecondaryPumpItem]] = None

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class SecondaryPumpSystem(BaseConfigModel):
    cooling: Optional[SecondaryPump] = Field(
        None,
        alias="冷房",  # NOTE: for builelib compatibility
    )
    heating: Optional[SecondaryPump] = Field(
        None,
        alias="暖房",  # NOTE: for builelib compatibility
    )
