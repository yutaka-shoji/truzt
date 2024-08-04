from typing import Literal
from pydantic import BaseModel, Field


class BaseRoom(BaseModel):
    name: str
    floor: str

    room_area: float = Field(gt=0)
    floor_height: float = Field(gt=0)
    ceiling_height: float = Field(gt=0)

    building_type: Literal[
        "事務所等",
        "ホテル等",
        "病院等",
        "百貨店等",
        "学校等",
        "飲食店等",
        "集会所等",
        "工場等",
        "共同住宅等",
        "既存部分",
    ]


class OfficeRoom(BaseRoom):
    room_type: Literal["事務所等"]
    room_type_detail: Literal[
        "事務室",
        "電子計算機事務室",
        "会議室",
        "喫茶室" "社員食堂",
        "中央監視室",
        "更衣室又は倉庫",
        "廊下",
        "ロビー",
        "便所",
        "喫煙室",
        "厨房",
        "屋内駐車場",
        "機械室",
        "電気室",
        "湯沸室等",
        "食品庫等",
        "印刷室等",
        "廃棄物保管場所等",
    ]


class HotelRoom(BaseRoom):
    room_type: Literal["ホテル等"]
    room_type_detail: Literal[
        "客室",
        "客室内の浴室等",
        "終日利用されるフロント," "終日利用される事務室",
        "終日利用される廊下",
        "終日利用されるロビー",
        "終日利用される共用部の便所",
        "終日利用される喫煙室",
        "宴会場",
        "会議室",
        "結婚式場",
        "レストラン",
        "ラウンジ",
        "バー",
        "店舗",
        "社員食堂",
        "更衣室又は倉庫",
        "日中のみ利用されるフロント",
        "日中のみ利用される事務室",
        "日中のみ利用される廊下",
        "日中のみ利用されるロビー",
        "日中のみ利用される共用部の便所",
        "日中のみ利用される喫煙室",
        "厨房",
        "屋内駐車場",
        "機械室",
        "電気室",
        "湯沸室等",
        "食品庫等",
        "印刷室等",
        "廃棄物保管場所等",
    ]


class HospitalRoom(BaseRoom):
    room_type: Literal["病院等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class DepartmentStoreRoom(BaseRoom):
    room_type: Literal["百貨店等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class SchoolRoom(BaseRoom):
    room_type: Literal["学校等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class RestaurantRoom(BaseRoom):
    room_type: Literal["飲食店等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class CommunityRoom(BaseRoom):
    room_type: Literal["集会所等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class FactoryRoom(BaseRoom):
    room_type: Literal["工場等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class HousingRoom(BaseRoom):
    room_type: Literal["共同住宅等"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]


class ExistingRoom(BaseRoom):
    room_type: Literal["既存部分"]
    # TODO: Define room_type_detail
    room_type_detail: Literal[""]
