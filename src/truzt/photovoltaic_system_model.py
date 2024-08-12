"""Module for defining the PhotovoltaicSystem model."""

from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class PhotovoltaicSystem(BaseConfigModel):
    """Photovoltaic system.

    Attributes:
        power_conditioner_efficiency: パワーコンディショナの効率
        cell_type: 太陽電池の種類
        array_setup_type: アレイ設置方式
        array_capacity: アレイのシステム容量 (kW)
        direction: パネルの方位角 (deg)
        angle: パネルの傾斜角 (deg)
        info: 備考
    """

    power_conditioner_efficiency: Optional[float] = Field(ge=0.0, le=1.0)
    cell_type: Optional[
        Literal[
            "結晶系",
            "結晶系以外",
        ]
    ] = None
    array_setup_type: Optional[
        Literal[
            "架台設置形",
            "屋根置き形",
            "その他",
        ]
    ] = None
    array_capacity: Optional[float] = Field(gt=0.0)

    direction: Optional[float] = Field(ge=0.0, le=360.0)
    angle: Optional[float] = Field(ge=0.0, le=180.0)

    info: Optional[str] = None
