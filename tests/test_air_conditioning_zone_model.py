import json

from truzt import AirConditioningZone


def test_air_conditioning_zone_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # AirConditioningZoneのdictを取得
    ac_zone_dict = data["AirConditioningZone"]

    ac_zone_serialized_dict = {}
    for key in ac_zone_dict.keys():
        # AirConditioningZoneインスタンスを作成
        ac_zone = AirConditioningZone.model_validate(ac_zone_dict[key])
        # serialize
        ac_zone_serialized_dict[key] = ac_zone.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert ac_zone_dict == ac_zone_serialized_dict
