from typing import Literal, Optional

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel

from .model_config import BaseConfigModel


class WindowConfigure(BaseConfigModel):
    """窓仕様

    Attributes:
        window_area: 窓面積
        window_width: 窓の幅
        window_height: 窓の高さ
        input_method: 窓性能の入力方法
        frame_type: 建具の種類
        glass_id: ガラス建築確認記号
        layer_type: ガラスの層数
        glass_uvalue: ガラスの熱貫流率
        glass_ivalue: ガラスの日射熱取得率
        window_uvalue: 窓の熱貫流率
        window_ivalue: 窓の日射熱取得率
        info: 備考
    """

    # NOTE: builelibでここだけcamelCaseになっているのでその対応
    model_config = ConfigDict(alias_generator=to_camel)

    window_area: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_width: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_height: Optional[float] = Field(
        None,
        ge=0.0,
    )
    input_method: Optional[
        Literal[
            "性能値を入力",
            "ガラスの性能を入力",
            "ガラスの種類を入力",
        ]
    ] = Field(
        None,
    )
    frame_type: Optional[
        Literal[
            "樹脂製",
            "木製",
            "金属樹脂複合製",
            "金属木複合製",
            "金属製",
        ]
    ] = Field(
        None,
    )
    glass_id: Optional[str] = Field(
        None,
        alias="glassID",  # NOTE: for builelib compatibility
    )
    layerType: Optional[Literal["複層", "単層"]] = Field(
        None,
    )
    glass_uvalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    glass_ivalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_uvalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    window_ivalue: Optional[float] = Field(
        None,
        ge=0.0,
    )
    info: Optional[str] = Field(
        None,
        alias="Info",  # NOTE: for builelib compatibility
    )
