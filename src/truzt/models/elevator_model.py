from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class ElevatorItem(BaseConfigModel):
    """Elevaror item

    Attributes:
        elevator_name: 昇降機系統の名称
        number: 台数
        load_limit: 積載量 (kg)
        velocity: 速度 (m.min-1)
        transport_capacity_factor: 輸送能力係数
        control_type: 制御方式
        info: 備考
    """

    elevator_name: Optional[str]
    number: Optional[int] = Field(gt=0)
    load_limit: Optional[float] = Field(gt=0.0)
    velocity: Optional[float] = Field(gt=0.0)
    transport_capacity_factor: Optional[float] = Field(gt=0.0)
    control_type: Optional[
        Literal[
            "VVVF(電力回生なし)",
            "VVVF(電力回生あり)",
            "VVVF(電力回生なし、ギアレス)",
            "VVVF(電力回生あり、ギアレス)",
            "交流帰還制御",
        ]
    ]
    info: Optional[str] = None


# TODO: このネスト必要?
class Elevators(BaseConfigModel):
    """elevators

    Attributes:
        elevator: list of ElevatorItem
    """

    elevator: Optional[list[ElevatorItem]] = None
