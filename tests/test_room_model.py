import json

from truzt import OfficeRoom


def test_community_room_json_serialize():
    # TODO: implement
    pass


def test_department_store_room_json_serialize():
    # TODO: implement
    pass


def test_factory_room_json_serialize():
    # TODO: implement
    pass


def test_hospital_room_json_serialize():
    # TODO: implement
    pass


def test_hotel_room_json_serialize():
    # TODO: implement
    pass


def test_office_room_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # Roomsのdictを取得
    room_dict = data["Rooms"]

    room_serialized_dict = {}
    for key in room_dict.keys():
        # OfficeRoomインスタンスを作成
        room = OfficeRoom.model_validate(room_dict[key])
        # serialize
        room_serialized_dict[key] = room.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized ignoring the order
    assert sorted(room_dict.items()) == sorted(room_serialized_dict.items())


def test_residential_complex_room_json_serialize():
    # TODO: implement
    pass


def test_restaurant_room_json_serialize():
    # TODO: implement
    pass


def test_school_room_json_serialize():
    # TODO: implement
    pass
