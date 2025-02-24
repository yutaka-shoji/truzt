import json

import pytest
from openpyxl import Workbook, load_workbook

from truzt.air_conditioning_zone_model import AirConditioningZones
from truzt.building_model import Building
from truzt.room_model import Rooms

V2_TEST_CASES = [
    "sample_v2",
    "sample_v2_sp01",
    "sample_v2_sp02",
    "sample_v2_sp03",
    "sample_v2_sp04",
    "sample_v2_sp05",
    "sample_v2_sp06",
    "sample_v2_sp07",
    "sample_v2_sp08",
    "sample_v2_sp09",
    "sample_v2_sp10",
    "sample_v2_sp11",
]

V2_TEST_CASE_WORKBOOKS = {
    case: load_workbook(f"./sample/{case}.xlsm", read_only=True, data_only=True)
    for case in V2_TEST_CASES
}

V2_TEST_CASE_EXPECTED_DATA = {
    case: json.load(open(f"./sample/{case}.json")) for case in V2_TEST_CASES
}


def dict_equal_ignore_info(d1: dict, d2: dict) -> bool:
    """
    2つの辞書を比較し、"Info"キーの内容は無視して比較する

    Args:
        d1: 比較する辞書1
        d2: 比較する辞書2

    Returns:
        bool: 辞書が等しい場合はTrue
    """
    if type(d1) is not type(d2):
        return False

    if isinstance(d1, dict):
        if set(d1.keys()) != set(d2.keys()):
            return False

        return all(True if k == "Info" else dict_equal_ignore_info(v, d2[k]) for k, v in d1.items())
    elif isinstance(d1, (list, tuple)):
        if len(d1) != len(d2):
            return False
        return all(dict_equal_ignore_info(v1, v2) for v1, v2 in zip(d1, d2))
    else:
        return d1 == d2


def get_v2_test_params():
    return [
        pytest.param(
            V2_TEST_CASE_WORKBOOKS[case],
            V2_TEST_CASE_EXPECTED_DATA[case],
            id=case,
        )
        for case in V2_TEST_CASES
    ]


@pytest.mark.parametrize("wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_building_model(wb: Workbook, expected_data: dict):
    building = Building.from_workbook(wb, ver="v2")
    building_dict = building.model_dump(by_alias=True)

    assert dict_equal_ignore_info(building_dict, expected_data["Building"])


@pytest.mark.parametrize("wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_rooms_model(wb: Workbook, expected_data: dict):
    rooms = Rooms.from_workbook(wb, ver="v2")
    rooms_dict = rooms.model_dump(by_alias=True)

    assert dict_equal_ignore_info(rooms_dict, expected_data["Rooms"])


@pytest.mark.parametrize("wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_air_conditioning_zones_model(wb: Workbook, expected_data: dict):
    """AirConditioningZonesモデルへの変換テスト.

    Args:
        wb: テスト用のワークブック
        expected_data: 期待されるデータ（JSON）
    """
    zones = AirConditioningZones.from_workbook(wb, ver="v2")
    zones_dict = zones.model_dump(by_alias=True)

    assert dict_equal_ignore_info(zones_dict, expected_data["AirConditioningZone"])
