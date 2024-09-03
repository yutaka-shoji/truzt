"""This module defines the VentilationRoom and VentilationUnitRef classes.

Classes:
    VentilationUnitRef: A class representing a reference to a ventilation unit.
    VentilationRoom: A class representing a ventilation room.
"""

from typing import Literal, Optional

from .model_config import BaseConfigModel


class VentilationUnitRef(BaseConfigModel):
    """TODO: VentilationUnitRef.

    Attributes:
        unit_type: 機器の種類
        info: 備考
    """

    unit_type: Optional[Literal["給気", "排気", "空調", "循環"]] = None
    info: Optional[str] = None


class VentilationRoom(BaseConfigModel):
    """Ventilation room.

    Attributes:
        ventilation_type: 換気方式
        ventilation_unit_ref: dict[str, VentilationUnitRef]
    """

    ventilation_type: Optional[Literal["一種換気", "二種換気", "三種換気"]] = None
    ventilation_unit_ref: dict[str, VentilationUnitRef]
