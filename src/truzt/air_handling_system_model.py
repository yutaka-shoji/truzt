"""Module for defining the AirHandlingSystem and AirHandlingUnitItem models."""

from typing import Literal, Optional, Union

from pydantic import Field, field_serializer, field_validator

from .model_config import BaseConfigModel


class AirHandlingUnitItem(BaseConfigModel):
    """Air handling unit item.

    Attributes:
        type: 構成機種
        number: 台数
        rated_capacity_cooling: 定格能力（冷房）
        rated_capacity_heating: 定格能力（暖房）
        fan_type: 送風機種類
        fan_air_volume: 設計風量
        fan_power_consumption: 定格消費電力
        fan_control_type: 風量制御方式
        fan_min_opening_rate: 最小風量比
        air_heat_exchange_ratio_cooling: 全熱交換効率 冷房時
        air_heat_exchange_ratio_heating: 全熱交換効率 暖房時
        air_heat_exchanger_effective_air_volume_ratio: 全熱交換器 有効換気量率
        air_heat_exchanger_control: 自動換気切替機能の有無
        air_heat_exchanger_power_consumption: ローター回転用電動機消費電力
        is_air_heat_exchanger: 全熱交換器の有無
        air_heat_exchanger_name: 全熱交換器名称
        info: 備考
    """

    type: Optional[
        Literal[
            "空調機",
            "FCU",
            "送風機",
            "室内機",
            "全熱交ユニット",
            "放熱器",
            "天井放射冷暖房パネル",
        ]
    ] = None
    number: Optional[int] = Field(None, gt=0)
    rated_capacity_cooling: Optional[float] = Field(None, gt=0)
    rated_capacity_heating: Optional[float] = Field(None, ge=0)
    fan_type: Optional[
        Literal[
            "給気",
            "還気",
            "外気",
            "排気",
            "循環",
            "ポンプ",
        ]
    ] = None
    fan_air_volume: Optional[float] = Field(None, gt=0)
    fan_power_consumption: Optional[float] = Field(None, gt=0)
    fan_control_type: Optional[
        Literal[
            "無",
            "定風量制御",
            "回転数制御",
        ]
    ] = None
    fan_min_opening_rate: Optional[float] = Field(None, ge=0)
    air_heat_exchange_ratio_cooling: Optional[float] = Field(None, ge=0)
    air_heat_exchange_ratio_heating: Optional[float] = Field(None, ge=0)
    air_heat_exchanger_effective_air_volume_ratio: Optional[float] = Field(None, ge=0)
    air_heat_exchanger_control: Optional[bool] = None
    air_heat_exchanger_power_consumption: Optional[float] = Field(None, ge=0)

    is_air_heat_exchanger: Optional[bool] = Field(
        None,
        alias="isAirHeatExchanger",  # NOTE: for builelib compatibility
    )
    air_heat_exchanger_name: Optional[str] = Field(
        None,
        alias="AirHeatExchanger_name",  # NOTE: for builelib compatibility
    )

    info: Optional[str] = None

    @field_validator(
        "air_heat_exchanger_control", "is_air_heat_exchanger", mode="before"
    )
    @classmethod
    def _convert_to_bool(cls, arg: Union[str, bool]) -> bool:
        if arg == "有":
            arg = True
        elif arg == "無":
            arg = False
        elif isinstance(arg, bool):
            arg = arg
        else:
            raise ValueError("must be '有' or '無' or boolean")
        return arg

    @field_serializer("air_heat_exchanger_control", "is_air_heat_exchanger")
    def _convert_to_str(self, arg: bool) -> Literal["有", "無"]:
        if arg:
            str_arg = "有"
        else:
            str_arg = "無"
        return str_arg


class AirHandlingSystem(BaseConfigModel):
    """Air handling system.

    Attributes:
        is_economizer: 外気冷房制御の有無
        economizer_max_air_volume: 外気冷房制御 最大
        is_outdoor_air_cut: 予熱時外気取入量制御の有無
        pump_cooling: 二次ポンプ群名称 冷房
        pump_heating: 二次ポンプ群名称 暖房
        heat_source_cooling: 熱源群名称 冷房
        heat_source_heating: 熱源群名称 暖房
        air_handling_unit: list of AirHandlingUnitItem
    """

    is_economizer: Optional[bool] = Field(
        None,
        alias="isEconomizer",  # NOTE: for builelib compatibility
    )
    economizer_max_air_volume: Optional[float] = Field(None, ge=0.0)
    is_outdoor_air_cut: Optional[bool] = Field(
        None,
        alias="isOutdoorAirCut",  # NOTE: for builelib compatibility
    )

    pump_cooling: Optional[str] = Field(
        None,
        alias="Pump_cooling",  # NOTE: for builelib compatibility
    )
    pump_heating: Optional[str] = Field(
        None,
        alias="Pump_heating",  # NOTE: for builelib compatibility
    )

    heat_source_cooling: Optional[str] = Field(
        None,
        alias="HeatSource_cooling",  # NOTE: for builelib compatibility
    )
    heat_source_heating: Optional[str] = Field(
        None,
        alias="HeatSource_heating",  # NOTE: for builelib compatibility
    )

    air_handling_unit: Optional[list[AirHandlingUnitItem]] = None

    @field_validator("is_economizer", "is_outdoor_air_cut", mode="before")
    @classmethod
    def _convert_to_bool(cls, arg: Union[str, bool]) -> bool:
        if arg == "有":
            arg = True
        elif arg == "無":
            arg = False
        elif isinstance(arg, bool):
            arg = arg
        else:
            raise ValueError("must be '有' or '無' or boolean")
        return arg

    @field_serializer("is_economizer", "is_outdoor_air_cut")
    def _convert_to_str(self, arg: bool) -> Literal["有", "無"]:
        if arg:
            str_arg = "有"
        else:
            str_arg = "無"
        return str_arg
