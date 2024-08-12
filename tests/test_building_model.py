import json

from truzt import Building


def test_building_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # Buildingのdictを取得
    building_dict = data["Building"]

    # Buildingインスタンスを作成
    building = Building.model_validate(building_dict)

    # serialize
    building_serialized_dict = building.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert building_dict == building_serialized_dict
