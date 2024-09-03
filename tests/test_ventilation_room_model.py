import json

from truzt.ventilation_room_model import VentilationRoom


def test_ventilation_room_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        data = json.load(file)

    # VentilationRoomのdictを取得
    vr_dict = data["VentilationRoom"]

    vr_serialized_dict = {}
    for key in vr_dict.keys():
        # VentilationRoomインスタンスを作成
        vr = VentilationRoom.model_validate(vr_dict[key])
        # serialize
        vr_serialized_dict[key] = vr.model_dump(by_alias=True, exclude_unset=True)

    vr_serialized_json_str = json.dumps(vr_serialized_dict, indent=2, ensure_ascii=False)
    vr_json_str = json.dumps(vr_dict, indent=2, ensure_ascii=False)

    # check if the original dict and the serialized
    assert vr_serialized_json_str == vr_json_str
