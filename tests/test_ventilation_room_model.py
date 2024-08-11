import json

from truzt.models import VentilationRoom


def test_ventilation_room_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json", "r") as file:
        data = json.load(file)

    # VentilationRoomのdictを取得
    vr_dict = data["VentilationRoom"]

    vr_serialized_dict = {}
    for key in vr_dict.keys():
        # VentilationRoomインスタンスを作成
        vr = VentilationRoom.model_validate(vr_dict[key])
        # serialize
        vr_serialized_dict[key] = vr.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert vr_dict == vr_serialized_dict
