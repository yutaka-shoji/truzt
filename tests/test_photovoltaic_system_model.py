import json

from truzt import PhotovoltaicSystem


def test_photovoltaic_system_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # PhotovoltaicSystemsのdictを取得
    pvs_dict = data["PhotovoltaicSystems"]

    pvs_serialized_dict = {}
    for key in pvs_dict.keys():
        # PhotovoltaicSystemインスタンスを作成
        pvs = PhotovoltaicSystem.model_validate(pvs_dict[key])
        # serialize
        pvs_serialized_dict[key] = pvs.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert pvs_dict == pvs_serialized_dict
