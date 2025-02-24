from truzt.hot_water_room_model import HotWaterRoom


def test_hot_water_room_model_json_serialize(v3_test_case_dict):
    data = v3_test_case_dict

    # HotwaterRoomのdictを取得
    hw_room_dict = data["HotwaterRoom"]

    hw_room_serialized_dict = {}
    for key in hw_room_dict.keys():
        # HotwaterRoomインスタンスを作成
        hw_room = HotWaterRoom.model_validate(hw_room_dict[key])
        # serialize
        hw_room_serialized_dict[key] = hw_room.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert hw_room_dict == hw_room_serialized_dict
