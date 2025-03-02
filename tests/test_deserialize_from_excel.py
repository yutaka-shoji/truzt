import json

import pytest
from openpyxl import Workbook, load_workbook

from truzt.air_conditioning_zone_model import AirConditioningZones
from truzt.building_model import Building
from truzt.room_model import Rooms
from truzt.wall_configure_model import WallConfigures
from truzt.window_configure_model import WindowConfigures

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


def remove_info_recursively(data):
    """
    データから"Info"キーを再帰的に削除する

    Args:
        data: 処理対象のデータ

    Returns:
        "Info"キーが削除されたデータ
    """
    if isinstance(data, dict):
        return {k: remove_info_recursively(v) for k, v in data.items() if k != "Info"}
    elif isinstance(data, (list, tuple)):
        return [remove_info_recursively(v) for v in data]
    else:
        return data


def remove_null_recursively(data):
    """データがNoneの場合そのデータを削除する."""
    if isinstance(data, dict):
        return {k: remove_null_recursively(v) for k, v in data.items() if v is not None}
    elif isinstance(data, (list, tuple)):
        return [remove_null_recursively(v) for v in data if v is not None]
    else:
        return data


def dict_equal_ignore_info(d1: dict, d2: dict):
    """
    2つの辞書を比較し、"Info"キーの内容は無視して比較する

    Args:
        d1: 比較する辞書1
        d2: 比較する辞書2

    Returns:
        bool: 辞書が等しい場合はTrue
    """
    d1_cleaned = remove_info_recursively(remove_null_recursively(d1))
    d2_cleaned = remove_info_recursively(remove_null_recursively(d2))
    assert d1_cleaned == d2_cleaned


def get_v2_test_params():
    return [
        pytest.param(
            case,
            V2_TEST_CASE_WORKBOOKS[case],
            V2_TEST_CASE_EXPECTED_DATA[case],
            id=case,
        )
        for case in V2_TEST_CASES
    ]


@pytest.mark.parametrize("case, wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_building_model(case: str, wb: Workbook, expected_data: dict):
    building = Building.from_workbook(wb, ver="v2")
    building_dict = building.model_dump(by_alias=True)

    dict_equal_ignore_info(building_dict, expected_data["Building"])


@pytest.mark.parametrize("case, wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_rooms_model(case: str, wb: Workbook, expected_data: dict):
    rooms = Rooms.from_workbook(wb, ver="v2")
    rooms_dict = rooms.model_dump(by_alias=True)

    dict_equal_ignore_info(rooms_dict, expected_data["Rooms"])


@pytest.mark.parametrize("case, wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_air_conditioning_zones_model(
    case: str, wb: Workbook, expected_data: dict
):
    """AirConditioningZonesモデルへの変換テスト.

    Args:
        wb: テスト用のワークブック
        expected_data: 期待されるデータ（JSON）
    """
    zones = AirConditioningZones.from_workbook(wb, ver="v2")
    zones_dict = zones.model_dump(by_alias=True)

    dict_equal_ignore_info(zones_dict, expected_data["AirConditioningZone"])


@pytest.mark.parametrize("case, wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_wall_configure_model(
    case: str, wb: Workbook, expected_data: dict, tmp_path
):
    """WallConfigureモデルへの変換テスト.

    Args:
        wb: テスト用のワークブック
        expected_data: 期待されるデータ（JSON）
    """
    wall_configure = WallConfigures.from_workbook(wb, ver="v2")
    wall_configure_dict = wall_configure.model_dump(by_alias=True)

    # tmp_pathにsave
    with open(f"{tmp_path}/{case}_wall_configure_test.json", "w") as f:
        json.dump(wall_configure_dict, f, indent=2, ensure_ascii=False)
    with open(f"{tmp_path}/{case}_wall_configure_expected.json", "w") as f:
        json.dump(expected_data["WallConfigure"], f, indent=2, ensure_ascii=False)

    dict_equal_ignore_info(wall_configure_dict, expected_data["WallConfigure"])


@pytest.mark.parametrize("case, wb, expected_data", get_v2_test_params())
def test_can_convert_v2_wb_to_window_configure_model(
    case: str, wb: Workbook, expected_data: dict, tmp_path
):
    """WindowConfigureモデルへの変換テスト.

    Args:
        wb: テスト用のワークブック
        expected_data: 期待されるデータ（JSON）
    """
    window_configure = WindowConfigures.from_workbook(wb, ver="v2")
    window_configure_dict = window_configure.model_dump(by_alias=True)

    # tmp_pathにsave
    with open(f"{tmp_path}/{case}_window_configure_test.json", "w") as f:
        json.dump(window_configure_dict, f, indent=2, ensure_ascii=False)
    with open(f"{tmp_path}/{case}_window_configure_expected.json", "w") as f:
        json.dump(expected_data["WindowConfigure"], f, indent=2, ensure_ascii=False)

    dict_equal_ignore_info(window_configure_dict, expected_data["WindowConfigure"])
