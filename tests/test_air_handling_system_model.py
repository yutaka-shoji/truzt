import json

from truzt.air_handling_system_model import AirHandlingSystem


def test_air_handling_system_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        data = json.load(file)

    # AirHandlingSystemのdictを取得
    ahs_dict = data["AirHandlingSystem"]

    ahs_serialized_dict = {}
    for key in ahs_dict.keys():
        # AirHandlingSystemインスタンスを作成
        ahs = AirHandlingSystem.model_validate(ahs_dict[key])
        # serialize
        ahs_serialized_dict[key] = ahs.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert ahs_dict == ahs_serialized_dict
