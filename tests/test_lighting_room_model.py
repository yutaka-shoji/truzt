from truzt.lighting_room_model import LightingRoom


def test_lighting_room_json_serialize(v3_test_case_dict):
    data = v3_test_case_dict

    # LightingSystemsのdictを取得
    lr_dict = data["LightingSystems"]

    lr_serialized_dict = {}
    for key in lr_dict.keys():
        # LightingRoomインスタンスを作成
        lr = LightingRoom.model_validate(lr_dict[key])
        # serialize
        lr_serialized_dict[key] = lr.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert lr_dict == lr_serialized_dict
