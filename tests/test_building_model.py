from truzt.building_model import Building


def test_building_json_serialize(v3_test_case_dict):
    data = v3_test_case_dict

    # Buildingのdictを取得
    building_dict = data["Building"]

    # Buildingインスタンスを作成
    building = Building.model_validate(building_dict)

    # serialize
    building_serialized_dict = building.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert building_dict == building_serialized_dict
