import json

from truzt import HeatSourceSystem


def test_heat_source_system_model_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # HeatsourceSystemのdictを取得
    hsys_dict = data["HeatsourceSystem"]

    hsys_serialized_dict = {}
    for key in hsys_dict.keys():
        # HeatSourceSystemインスタンスを作成
        hsys = HeatSourceSystem.model_validate(hsys_dict[key])
        # serialize
        hsys_serialized_dict[key] = hsys.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert hsys_dict == hsys_serialized_dict
