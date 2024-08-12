"""Module for defining the ShadingConfigure model."""

from typing import Optional

from pydantic import Field

from .model_config import BaseConfigModel


class ShadingConfigure(BaseConfigModel):
    """shading configure model.

    Attributes:
        shading_effect_c: shading effect coefficient for cooling
        shading_effect_h: shading effect coefficient for heating
        x1: NOT IMPLEMENTED
        x2: NOT IMPLEMENTED
        x3: NOT IMPLEMENTED
        y1: NOT IMPLEMENTED
        y2: NOT IMPLEMENTED
        y3: NOT IMPLEMENTED
        zx_plus: NOT IMPLEMENTED
        zx_minus: NOT IMPLEMENTED
        zy_plus: NOT IMPLEMENTED
        zy_minus: NOT IMPLEMENTED
        info:
    """

    shading_effect_c: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
    )

    shading_effect_h: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
    )

    # not implemented also in builelib
    # builelibでは日除けの形状って書いてあった
    x1: Optional[float] = None
    x2: Optional[float] = None
    x3: Optional[float] = None
    y1: Optional[float] = None
    y2: Optional[float] = None
    y3: Optional[float] = None
    zx_plus: Optional[float] = None
    zx_minus: Optional[float] = None
    zy_plus: Optional[float] = None
    zy_minus: Optional[float] = None
    info: Optional[str] = None
