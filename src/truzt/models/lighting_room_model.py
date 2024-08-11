from typing import Literal, Optional, Union

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel

from .model_config import BaseConfigModel


class LightingUnit(BaseConfigModel):
    """Lighting unit

    Attributes:
        rated_power: 定格消費電力 (W.unit-1)
        number: 台数
        occupant_sensing_ctrl: 在室検知制御
        illuminance_sensing_ctrl: 明るさ検知制御
        time_schedule_ctrl: タイムスケジュール制御
        initial_illumination_correction_ctrl: 初期照度補正制御
    """

    rated_power: Optional[float] = Field(
        None,
        ge=0.0,
    )
    number: Optional[int] = Field(
        1,
        ge=0,
    )
    occupant_sensing_ctrl: Optional[
        Union[
            Literal["無", "下限調光方式", "点滅方式", "減光方式"],
            float,
        ]
    ] = Field(
        None,
        alias="OccupantSensingCTRL",  # NOTE: for builelib compatibility (Ctrl -> CTRL)
    )
    illuminance_sensing_ctrl: Optional[
        Union[
            Literal[
                "無",
                "調光方式",
                "調光方式BL",
                "調光方式W15",
                "調光方式W15BL",
                "調光方式W20",
                "調光方式W20BL",
                "調光方式W25",
                "調光方式W25BL",
                "点滅方式",
            ],
            float,
        ]
    ] = Field(
        None,
        alias="IlluminanceSensingCTRL",  # NOTE: for builelib compatibility (Ctrl -> CTRL)
    )
    time_schedule_ctrl: Optional[
        Union[
            Literal["無", "減光方式", "点滅方式"],
            float,
        ]
    ] = Field(
        None,
        alias="TimeScheduleCTRL",  # NOTE: for builelib compatibility (Ctrl -> CTRL)
    )
    initial_illumination_correction_ctrl: Optional[
        Union[
            Literal[
                "無",
                "タイマ方式(LED)",
                "タイマ方式(蛍光灯)",
                "センサ方式(LED)",
                "センサ方式(蛍光灯)",
            ],
            float,
        ]
    ] = Field(
        None,
        alias="InitialIlluminationCorrectionCTRL",  # NOTE: for builelib compatibility (Ctrl -> CTRL)
    )


class LightingRoom(BaseConfigModel):
    """Lighting room

    Attributes:
        room_width: 室指数 室の間口 (m)
        room_depth: 室指数 室の奥行 (m)
        unit_height: 室指数 器具高さ (m)
        room_index: 室指数
        lighting_unit: LightingUnit
    """

    # NOTE: builelibでここだけcamelCaseになっているのでその対応
    model_config = ConfigDict(alias_generator=to_camel)

    room_width: Optional[float] = Field(gt=0.0)
    room_depth: Optional[float] = Field(gt=0.0)
    unit_height: Optional[float] = Field(gt=0.0)
    room_index: Optional[float] = Field(gt=0.0)
    lighting_unit: dict[str, LightingUnit]
