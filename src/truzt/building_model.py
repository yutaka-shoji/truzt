"""Module for defining the Building model and related classes."""

from typing import Literal, Optional

from pydantic import Field, field_serializer

from .model_config import BaseConfigModel


class BuildingAddress(BaseConfigModel):
    """Building Address.

    Attributes:
        prefecture: 都道府県
        city: 市区町村
        address: 丁目、番地
    """

    prefecture: Optional[str]
    city: Optional[str]
    address: Optional[str]


class CoefficientDHC(BaseConfigModel):
    """Coefficient DHC.

    Attributes:
        cooling: 冷熱
        heating: 温熱
    """

    cooling: Optional[float] = Field(ge=0)
    heating: Optional[float] = Field(ge=0)


class Building(BaseConfigModel):
    """Building info.

    Attributes:
        name: 建築物の名称
        building_address: 建築物所在地
        region: 地域の区分
        annual_solar_region: 年間日射地
        building_floor_area: 延べ面積 (m2)
        coefficient_dhc: 「他人から供給された熱」の一次エネルギー換算係数
    """

    name: str = "Anonymous"

    building_address: Optional[BuildingAddress]

    region: int = Field(ge=1, le=8)

    annual_solar_region: Literal[
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
    ]

    building_floor_area: float = Field(ge=0)

    coefficient_dhc: Optional[CoefficientDHC] = Field(
        alias="Coefficient_DHC",  # for builelib compatibility
    )

    @field_serializer("region")
    def _serialize_region(self, region: int) -> str:
        return str(region)
