import json

from openpyxl import load_workbook
from truzt.building_model import Building


def test_building_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        data = json.load(file)

    # Buildingのdictを取得
    building_dict = data["Building"]

    # Buildingインスタンスを作成
    building = Building.model_validate(building_dict)

    # serialize
    building_serialized_dict = building.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert building_dict == building_serialized_dict


def test_can_convert_wb_to_building_model():
    wb_path = "sample/sample_input_v3.xlsx"
    wb = load_workbook(wb_path, read_only=True, data_only=True)

    building = Building.from_workbook(wb, ver="v3")
    building_dict = building.model_dump(by_alias=True)

    ref_json_path = "sample/sample_input_v3.json"
    with open(ref_json_path) as f:
        ref_data = json.load(f)
    ref_building_dict = ref_data["Building"]

    assert json.dumps(building_dict, indent=2, ensure_ascii=False, sort_keys=True) == json.dumps(
        ref_building_dict, indent=2, ensure_ascii=False, sort_keys=True
    )
