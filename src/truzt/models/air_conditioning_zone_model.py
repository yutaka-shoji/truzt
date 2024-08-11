from typing import Literal, Optional, Union

from pydantic import Field, field_validator, field_serializer

from .model_config import BaseConfigModel


class AirConditioningZone(BaseConfigModel):
    """空調ゾーン

    Attributes:
        floor: 階
        name: 室名
        is_natual_ventilation: 自然換気の有無
        is_simultaneous_supply: 冷暖同時供給の有無
        ahu_cooling_inside_load: 空調機群名称 冷房室負荷処理
        ahu_cooling_outdoor_load: 空調機群名称 冷房外気負荷処理
        ahu_heating_inside_load: 空調機群名称 暖房室負荷処理
        ahu_heeating_outdoor_load: 空調機群名称 暖房外気負荷処理
        info:
    """

    # is_natural_ventilation: Literal["有", "無"]
    is_natural_ventilation: bool = Field(
        alias="isNatualVentilation",  # builelib タイポ対応
    )
    is_simultaneous_supply: Literal[
        "有",
        "無",
        "有（室負荷）",
        "有（外気負荷）",
    ] = Field(alias="isSimultaneousSupply")

    ahu_cooling_inside_load: str = Field(
        alias="AHU_cooling_insideLoad",  # for builelib compatibility
    )
    ahu_cooling_outdoor_load: str = Field(
        alias="AHU_cooling_outdoorLoad",  # for builelib compatibility
    )
    ahu_heating_inside_load: str = Field(
        alias="AHU_heating_insideLoad",  # for builelib compatibility
    )
    ahu_heeating_outdoor_load: str = Field(
        alias="AHU_heating_outdoorLoad",  # for builelib compatibility
    )

    info: Optional[str]

    @field_validator("is_natural_ventilation", mode="before")
    @classmethod
    def convert_to_bool(cls, arg: Union[str, bool]):
        if arg == "有":
            is_natural_ventilation = True
        elif arg == "無":
            is_natural_ventilation = False
        elif isinstance(arg, bool):
            is_natural_ventilation = arg
        else:
            raise ValueError("is_natural_ventilation must be '有' or '無' or boolean")
        return is_natural_ventilation

    @field_serializer("is_natural_ventilation")
    def convert_to_str(self, arg: bool):
        if arg:
            str_arg = "有"
        else:
            str_arg = "無"
        return str_arg
