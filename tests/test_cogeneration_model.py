import json

from truzt.cogeneration_system_model import CogenerationSystem


def test_cogeneration_system_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        data = json.load(file)

    # CogenerationSystemのdictを取得
    cgs_dict = data["CogenerationSystems"]

    cgs_serialized_dict = {}
    for key in data["CogenerationSystems"].keys():
        # CogenerationSystemインスタンスを作成
        cgs = CogenerationSystem.model_validate(cgs_dict[key])
        # serialize
        cgs_serialized_dict[key] = cgs.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert cgs_dict == cgs_serialized_dict
