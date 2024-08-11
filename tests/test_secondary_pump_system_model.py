import json

from truzt.models import SecondaryPumpSystem


def test_secondary_pump_system_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json", "r") as file:
        data = json.load(file)

    # SecondaryPumpSystemのdictを取得
    spsys_dict = data["SecondaryPumpSystem"]

    spsys_serialized_dict = {}
    for key in spsys_dict.keys():
        # SecondaryPumpSystemインスタンスを作成
        spsys = SecondaryPumpSystem.model_validate(spsys_dict[key])
        # serialize
        spsys_serialized_dict[key] = spsys.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert spsys_dict == spsys_serialized_dict
