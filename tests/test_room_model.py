import pytest
from pydantic import ValidationError

from truzt.room_model import Room, Rooms


def test_room_json_serialize(v3_test_case_dict):
    data = v3_test_case_dict

    # Roomsのreference dictを取得
    rooms_ref_dict = data["Rooms"]

    # Roomsインスタンスを作成
    rooms = Rooms.model_validate(rooms_ref_dict)
    # serialize
    rooms_dict = rooms.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized ignoring the order
    assert sorted(rooms_dict.items()) == sorted(rooms_ref_dict.items())


def test_room_type_match():
    room_dict = {
        "main_building_type": "事務所等",
        "building_type": "事務所等",
        "room_type": "廊下",
        "floor_height": 5.0,
        "ceiling_height": 2.6,
        "room_area": 10.0,
    }

    # Roomインスタンスを作成
    _ = Room.model_validate(room_dict)

    # test mismatch
    building_type = "ホテル等"
    room_dict["building_type"] = building_type

    # Roomインスタンス作成時にValidationErrorが発生することを確認
    with pytest.raises(ValidationError) as excinfo:
        Room.model_validate(room_dict)

    # エラーメッセージの検証
    error_details = excinfo.value.errors()
    assert len(error_details) == 1  # 1つのエラーが発生することを確認
    assert error_details[0]["type"] == "value_error"  # エラータイプの確認
