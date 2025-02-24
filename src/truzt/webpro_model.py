"""This module defines the WebproModel class.

Classes:
    WebproModel: A class representing the WEBPRO model.
"""

from typing import Any, Optional

from pydantic import Field

from .air_conditioning_zone_model import AirConditioningZones
from .air_handling_system_model import AirHandlingSystems
from .building_model import Building
from .cogeneration_system_model import CogenerationSystems
from .elevator_model import ElevatorSystems
from .envelope_set_model import EnvelopeSets
from .heat_source_system_model import HeatSourceSystems
from .hot_water_room_model import HotWaterRooms
from .hot_water_supply_system_model import HotWaterSupplySystems
from .lighting_room_model import LightingRooms
from .model_config import BaseConfigModel
from .photovoltaic_system_model import PhotovoltaicSystems
from .room_model import Rooms
from .secondary_pump_system_model import SecondaryPumpSystems
from .shading_configure_model import ShadingConfigures
from .ventilation_room_model import VentilationRooms
from .ventilation_unit_model import VentilationUnits
from .wall_configure_model import WallConfigures
from .window_configure_model import WindowConfigures


class WebproModel(BaseConfigModel):
    """WEBPRO model.

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

    building: Optional[Building] = Field(
        None,
    )
    rooms: Optional[Rooms] = Field(
        None,
    )
    air_conditioning_zone: Optional[AirConditioningZones] = Field(
        None,
    )
    wall_configure: Optional[WallConfigures] = Field(
        None,
    )
    window_configure: Optional[WindowConfigures] = Field(
        None,
    )
    envelope_set: Optional[EnvelopeSets] = Field(
        None,
    )
    shading_configure: Optional[ShadingConfigures] = Field(
        None,
    )
    heatsource_system: Optional[HeatSourceSystems] = Field(
        None,
    )
    secondary_pump_system: Optional[SecondaryPumpSystems] = Field(
        None,
    )
    air_handling_system: Optional[AirHandlingSystems] = Field(
        None,
    )
    ventilation_room: Optional[VentilationRooms] = Field(
        None,
    )
    ventilation_unit: Optional[VentilationUnits] = Field(
        None,
    )
    lighting_systems: Optional[LightingRooms] = Field(
        None,
    )
    hotwater_room: Optional[HotWaterRooms] = Field(
        None,
    )
    hotwater_supply_systems: Optional[HotWaterSupplySystems] = Field(
        None,
    )
    elevators: Optional[ElevatorSystems] = Field(
        None,
    )
    photovoltaic_systems: Optional[PhotovoltaicSystems] = Field(
        None,
    )
    cogeneration_systems: Optional[CogenerationSystems] = Field(
        None,
    )
    # TODO: builelib SPシート未対応
    special_input_data: Optional[dict[str, Any]] = Field(
        None,
    )
