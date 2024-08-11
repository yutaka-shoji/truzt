from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class WindowListItem(BaseConfigModel):
    """窓
    NOTE: builelibでは窓面積をWindowNumberに入れている?

    Attributes:
        window_id: 開口部仕様名称
        window_number: 建具等個数
        is_blind: ブラインドの有無
        eaves_id: 日除けの名称
        info: 備考
    """

    window_id: Optional[str] = Field(
        None,
        alias="WindowID",  # NOTE: for builelib compatibility
    )
    window_number: Optional[float] = Field(
        None,
        gt=0,
    )
    is_blind: Optional[Literal["有", "無"]] = Field(
        None,
        alias="isBlind",  # NOTE: for builelib compatibility
    )
    eaves_id: Optional[str] = Field(
        None,
        alias="EavesID",  # NOTE: for builelib compatibility
    )
    info: Optional[str] = None

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class WallListItem(BaseConfigModel):
    """壁

    Attributes:
        direction: 方位
        envelope_area: 外皮面積
        envelope_width: 外皮の幅
        envelope_height: 外皮の高さ
        wall_spec: 断熱仕様名称
        wall_type: 外壁の種類
        window_list: 窓リスト
    """

    direction: Optional[
        Literal[
            "北",
            "北東",
            "東",
            "南東",
            "南",
            "南西",
            "西",
            "北西",
            "水平（上）",
            "水平（下）",
        ]
    ] = None

    envelope_area: Optional[float] = Field(
        None,
        gt=0,
    )

    envelope_width: Optional[float] = Field(
        None,
        gt=0,
    )

    envelope_height: Optional[float] = Field(
        None,
        gt=0,
    )

    wall_spec: Optional[str] = Field(
        None,
    )

    wall_type: Optional[
        Literal[
            "日の当たる外壁",
            "日の当たらない外壁",
            "地盤に接する外壁",
            "内壁",
        ]
    ] = None

    window_list: Optional[list[WindowListItem]] = None


class EnvelopeSet(BaseConfigModel):
    """外皮

    Attributes:
        is_air_conditioned: 空調の有無
        wall_list: 壁リスト
    """

    is_air_conditioned: Optional[Literal["有", "無"]] = Field(
        None,
        alias="isAirconditioned",  # NOTE: for builelib compatibility
    )
    wall_list: Optional[list[WallListItem]] = None

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean
