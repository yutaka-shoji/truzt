from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class HeatSourceItem(BaseConfigModel):
    """heat source item

    Attributes:
        heat_source_type: 熱源機種
        number: 台数
        supply_water_temp_summer: 送水温度 夏期
        supply_water_temp_middle: 送水温度 中間期
        supply_water_temp_winter: 送水温度 冬期
        heat_source_rated_capacity: 熱源本体 定格能力
        heat_source_rated_power_consumption: 熱源主機 定格消費電力
        heat_source_rated_fuel_consumption: 熱源主機 定格燃料消費量
        heat_source_sub_rated_power_consumption: 熱源補機 定格消費電力
        primary_pump_power_consumption: 一次ポンプ 定格消費電力
        primary_pump_control_type: 一次ポンプ 制御方式
        cooling_tower_capacity: 冷却塔 定格能力
        cooling_tower_fan_power_consumption: 冷却塔 ファン消費電
        cooling_tower_pump_power_consumption: 冷却塔 ポンプ消費電
        cooling_tower_control_type: 冷却塔 制御方式
        info: 備考
    """

    heat_source_type: Optional[str] = Field(
        None,
        alias="HeatsourceType",  # NOTE: for builelib compatibility
    )
    number: Optional[int] = Field(None, gt=0)
    supply_water_temp_summer: Optional[float] = None
    supply_water_temp_middle: Optional[float] = None
    supply_water_temp_winter: Optional[float] = None
    heat_source_rated_capacity: Optional[float] = Field(
        None,
        ge=0.0,
        alias="HeatsourceRatedCapacity",  # NOTE: for builelib compatibility
    )
    heat_source_rated_power_consumption: Optional[float] = Field(
        None,
        ge=0.0,
        alias="HeatsourceRatedPowerConsumption",  # NOTE: for builelib compatibility
    )
    heat_source_rated_fuel_consumption: Optional[float] = Field(
        None,
        ge=0.0,
        alias="HeatsourceRatedFuelConsumption",  # NOTE: for builelib compatibility
    )
    heat_source_sub_rated_power_consumption: Optional[float] = Field(
        None,
        ge=0.0,
        alias="Heatsource_sub_RatedPowerConsumption",  # NOTE: for builelib compatibility
    )
    primary_pump_power_consumption: Optional[float] = Field(None, ge=0.0)
    primary_pump_control_type: Optional[Literal["有", "無"]] = Field(
        None,
        alias="PrimaryPumpContolType",  # NOTE: for builelib typo compatibility
    )
    cooling_tower_capacity: Optional[float] = Field(None, ge=0.0)
    cooling_tower_fan_power_consumption: Optional[float] = Field(None, ge=0.0)
    cooling_tower_pump_power_consumption: Optional[float] = Field(None, ge=0.0)
    cooling_tower_control_type: Optional[Literal["有", "無"]] = Field(
        None,
        alias="CoolingTowerContolType",  # NOTE: for builelib TYPO compatibility
    )
    info: Optional[str] = None

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class HeatSource(BaseConfigModel):
    """heat source

    Attributes:
        storage_type: 蓄熱の種類
        storage_size: 蓄熱容量
        is_staging_control: 台数制御
        heat_source: list of HeatSourceItem
    """

    storage_type: Optional[
        Literal[
            "水蓄熱(混合型)",
            "水蓄熱(成層型)",
            "氷蓄熱",
        ]
    ] = None
    storage_size: Optional[float] = Field(None, gt=0.0)

    is_staging_control: Optional[Literal["有", "無"]] = Field(
        None,
        alias="isStagingControl",  # NOTE: for builelib compatibility
    )
    heat_source: Optional[list[HeatSourceItem]] = Field(
        None,
        alias="Heatsource",  # NOTE: for builelib compatibility
    )

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class HeatSourceSystem(BaseConfigModel):
    cooling: Optional[HeatSource] = Field(
        None,
        alias="冷房",
    )
    heating: Optional[HeatSource] = Field(
        None,
        alias="暖房",
    )
    cooling_with_heat_storage: Optional[HeatSource] = Field(
        None,
        alias="冷房(蓄熱)",
    )
    heating_with_heat_storage: Optional[HeatSource] = Field(
        None,
        alias="暖房(蓄熱)",
    )
