"""WEBPRO readerの実装を提供するモジュール."""

from pathlib import Path
from typing import Literal

from openpyxl import load_workbook

from .air_conditioning_zone_reader import AirConditioningZoneReader
from .building_reader import BuildingReader
from .room_reader import RoomReader
from .webpro_model import WebproModel


def read_webpro_excel(path: str, version: Literal["v2", "v3"] = "v3") -> WebproModel:
    """WEBPROのExcelファイルを読み込んでWebproModelを生成する.

    Args:
        path: Excelファイルのパス.
        version: WEBPROのバージョン ("v2" or "v3").

    Returns:
        WebproModel: 読み込んだデータ.

    Raises:
        ExcelReadError: 読み込みに失敗した場合.
        FileNotFoundError: ファイルが存在しない場合.
    """
    # Excelファイルの存在チェック
    excel_path = Path(path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excelファイルが見つかりません: {path}")

    # Excelファイルを読み込み
    wb = load_workbook(filename=str(excel_path), data_only=True)

    # 各コンポーネントの読み込み
    building = BuildingReader(wb, version).read()
    rooms = RoomReader(wb, version).read()
    air_conditioning_zones = AirConditioningZoneReader(wb, version).read()

    # WebproModelの生成
    return WebproModel(
        building=building,
        rooms=rooms,
        air_conditioning_zone=air_conditioning_zones.root,
        wall_configure={},
        window_configure={},
        envelope_set={},
        shading_configure={},
        heatsource_system={},
        secondary_pump_system={},
        air_handling_system={},
        ventilation_room={},
        ventilation_unit={},
        lighting_systems={},
        hotwater_room={},
        hotwater_supply_systems={},
        elevators={},
        photovoltaic_systems={},
        cogeneration_systems={},
        special_input_data={},
    )
