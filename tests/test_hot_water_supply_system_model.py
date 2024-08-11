import json

from truzt.models import HotWaterSupplySystem


def test_hot_water_supply_system_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json", "r") as file:
        data = json.load(file)

    # HotWaterSupplySystemsのdictを取得
    hwss_dict = data["HotwaterSupplySystems"]

    hwss_serialized_dict = {}
    for key in hwss_dict.keys():
        # HotWaterSupplySystemインスタンスを作成
        hwss = HotWaterSupplySystem.model_validate(hwss_dict[key])
        # serialize
        hwss_serialized_dict[key] = hwss.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert hwss_dict == hwss_serialized_dict
