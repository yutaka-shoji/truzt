"""Module for defining the HotWaterRoom and HotWaterSystemItem models."""

from typing import Literal, Optional

from openpyxl import Workbook
from pydantic import Field, RootModel

from .model_config import BaseConfigModel


class HotWaterSystemItem(BaseConfigModel):
    """Hot water system.

    Attributes:
        system_name: 給湯システム名称
        usage_type: 給湯用途
        hot_water_saving_system: 節湯器具
        info: 備考
    """

    system_name: Optional[str]
    usage_type: Optional[
        Literal[
            "便所",
            "浴室",
            "厨房",
            "その他",
        ]
    ] = None
    hot_water_saving_system: Optional[
        Literal[
            "自動給湯栓",
            "節湯B1",
            "無",
        ]
    ] = None
    info: Optional[str] = None


class HotWaterRoom(BaseConfigModel):
    """Hot water room.

    Attributes:
        hot_water_system: list of HotWaterSystemItem
    """

    hot_water_system: Optional[list[HotWaterSystemItem]] = Field(
        None,
        alias="HotwaterSystem",
    )


class HotWaterRooms(RootModel):
    """HotWaterRoom dict.

    Attributes:
        root: HotWaterRoom dict.
    """

    root: dict[str, HotWaterRoom]

    @classmethod
    def from_workbook(cls, wb: Workbook, ver: Literal["v2", "v3"] = "v3") -> "HotWaterRooms":
        """WorkbookからHotWaterRoomsモデルを生成する.

        Args:
            wb: Workbook
            ver: WEBPRO input workbook version (v2 or v3).

        Returns:
            dict[str, HotWaterRoom]: HotWaterRoom dict
        """
        raise NotImplementedError
