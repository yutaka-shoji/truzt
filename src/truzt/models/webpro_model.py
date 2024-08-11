from typing import Any, Optional, Union

from pydantic import Field

from .air_conditioning_zone_model import AirConditioningZone
from .air_handling_system_model import AirHandlingSystem
from .building_model import Building
from .cogeneration_system_model import CogenerationSystem
from .elevator_model import Elevators
from .envelope_set_model import EnvelopeSet
from .heat_source_system_model import HeatSourceSystem
from .hot_water_room_model import HotWaterRoom
from .hot_water_supply_system_model import HotWaterSupplySystem
from .lighting_room_model import LightingRoom
from .model_config import BaseConfigModel
from .photovoltaic_system_model import PhotovoltaicSystem
from .room_model import (
    CommunityRoom,
    DepartmentStoreRoom,
    FactoryRoom,
    HospitalRoom,
    HotelRoom,
    OfficeRoom,
    ResidentialComplexRoom,
    RestaurantRoom,
    SchoolRoom,
)
from .secondary_pump_system_model import SecondaryPumpSystem
from .shading_configure_model import ShadingConfigure
from .ventilation_room_model import VentilationRoom
from .ventilation_unit_model import VentilationUnit
from .wall_configure_model import WallConfigure
from .window_configure_model import WindowConfigure


class WebproModel(BaseConfigModel):
    """WEBPRO model

    Attributes:
        building: 建物情報
        rooms: 室情報
        air_conditioning_zone: 空調ゾーン
        wall_configure: 外壁構成
        window_configure: 窓仕様
        envelope_set: 外皮
        shading_configure: 日除け(?)
        heat_source_system: 熱源
        secondary_pump_system: 2次ポンプ
        air_handling_system: 空調システム
        ventilation_room: 換気室
        ventilation_unit: 換気送風機
        lighting_systems: 照明
        hotwater_room: 給湯室
        hotwater_supply_systems: 給湯機器
        elevators: 昇降機
        photovoltaic_systems: 太陽光発電
        cogeneration_systems: コジェネレーション
    """

    building: Building = Field(
        None,
    )
    rooms: dict[
        str,
        Union[
            OfficeRoom,
            HotelRoom,
            HospitalRoom,
            DepartmentStoreRoom,
            SchoolRoom,
            RestaurantRoom,
            CommunityRoom,
            FactoryRoom,
            ResidentialComplexRoom,
        ],
    ] = Field(
        None,
    )
    air_conditioning_zone: Optional[dict[str, AirConditioningZone]] = Field(
        None,
    )
    wall_configure: Optional[dict[str, WallConfigure]] = Field(
        None,
    )
    window_configure: Optional[dict[str, WindowConfigure]] = Field(
        None,
    )
    envelope_set: Optional[dict[str, EnvelopeSet]] = Field(
        None,
    )
    shading_configure: Optional[dict[str, ShadingConfigure]] = Field(
        None,
    )
    heatsource_system: Optional[dict[str, HeatSourceSystem]] = Field(
        None,
    )
    secondary_pump_system: Optional[dict[str, SecondaryPumpSystem]] = Field(
        None,
    )
    air_handling_system: Optional[dict[str, AirHandlingSystem]] = Field(
        None,
    )
    ventilation_room: Optional[dict[str, VentilationRoom]] = Field(
        None,
    )
    ventilation_unit: Optional[dict[str, VentilationUnit]] = Field(
        None,
    )
    lighting_systems: Optional[dict[str, LightingRoom]] = Field(
        None,
    )
    hotwater_room: Optional[dict[str, HotWaterRoom]] = Field(
        None,
    )
    hotwater_supply_systems: Optional[dict[str, HotWaterSupplySystem]] = Field(
        None,
    )
    elevators: Optional[dict[str, Elevators]] = Field(
        None,
    )
    photovoltaic_systems: Optional[dict[str, PhotovoltaicSystem]] = Field(
        None,
    )
    cogeneration_systems: Optional[dict[str, CogenerationSystem]] = Field(
        None,
    )
    # TODO: builelib SPシート未対応
    special_input_data: Optional[dict[str, Any]] = Field(
        None,
    )
