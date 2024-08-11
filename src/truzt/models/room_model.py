from typing import Literal, Optional

from pydantic import Field

from .model_config import BaseConfigModel


class Zone(BaseConfigModel):
    """Zone info

    Attributes:
        zone_area: ゾーン面積
    """

    zone_area: Optional[float] = Field(ge=0)


class BaseRoom(BaseConfigModel):
    """全室用途に共通する基底クラス

    Attributes:
        main_building_type: 建物用途
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
        info: 備考
    """

    main_building_type: Literal[
        "事務所等",
        "ホテル等",
        "病院等",
        "百貨店等",
        "学校等",
        "飲食店等",
        "集会所等",
        "工場等",
        "共同住宅",
    ] = Field(
        None,
        alias="mainbuildingType",  # NOTE: for builelib compatibility
    )

    floor_height: float = Field(
        None,
        gt=0,
        alias="floorHeight",  # NOTE: for builelib compatibility
    )

    ceiling_height: Optional[float] = Field(
        None,
        gt=0,
        alias="ceilingHeight",  # NOTE: for builelib compatibility
    )

    room_area: float = Field(
        None,
        gt=0,
        alias="roomArea",  # NOTE: for builelib compatibility
    )

    zone: Optional[dict[str, Zone]] = Field(
        None,
        alias="zone",  # NOTE: for builelib compatibility
    )

    building_model_type: Optional[str] = Field(
        None,
        alias="modelBuildingType",  # NOTE: for builelib compatibility
    )

    building_group: Optional[str] = Field(
        None,
        alias="buildingGroup",  # NOTE: for builelib compatibility
    )

    info: Optional[str] = None


class OfficeRoom(BaseRoom):
    """事務所等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["事務所等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "事務室",
        "電子計算機器事務室",
        "会議室",
        "喫茶室",
        "社員食堂",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class HotelRoom(BaseRoom):
    """ホテル等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["ホテル等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "客室",
        "客室内の浴室等",
        "終日利用されるフロント",
        "終日利用される事務室",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class HospitalRoom(BaseRoom):
    """病院等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["病院等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "病室",
        "浴室等",
        "看護職員室",
        "終日利用される廊下",
        "終日利用されるロビー",
        "終日利用される共用部の便所",
        "終日利用される喫煙室",
        "診察室",
        "待合室",
        "手術室",
        "検査室",
        "集中治療室",
        "解剖室等",
        "レストラン",
        "事務室",
        "更衣室又は倉庫",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class DepartmentStoreRoom(BaseRoom):
    """百貨店等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["百貨店等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )
    room_type: Literal[
        "大型店の売場",
        "専門店の売場",
        "スーパーマーケットの売場",
        "荷さばき場",
        "事務室",
        "更衣室又は倉庫",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class SchoolRoom(BaseRoom):
    """学校等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["学校等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "小中学校の教室",
        "高等学校の教室",
        "職員室",
        "小中学校又は高等学校の食堂",
        "大学の教室",
        "大学の食堂",
        "事務室",
        "研究室",
        "電子計算機器演習室",
        "実験室",
        "実習室",
        "講堂又は体育館",
        "宿直室",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class RestaurantRoom(BaseRoom):
    """飲食店等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["飲食店等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "レストランの客室",
        "軽食店の客室",
        "喫茶店の客室",
        "バー",
        "フロント",
        "事務室",
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
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class CommunityRoom(BaseRoom):
    """集会所等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["集会所等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "アスレチック場の運動室",
        "アスレチック場のロビー",
        "アスレチック場の便所",
        "アスレチック場の喫煙室",
        "公式競技用スケート場",
        "公式競技用体育館",
        "一般競技用スケート場",
        "一般競技用体育館",
        "レクリエーション用スケート場",
        "レクリエーション用体育館",
        "競技場の客席",
        "競技場のロビー",
        "競技場の便所",
        "競技場の喫煙室",
        "公衆浴場の浴室",
        "公衆浴場の脱衣所",
        "公衆浴場の休憩室",
        "公衆浴場のロビー",
        "公衆浴場の便所",
        "公衆浴場の喫煙室",
        "映画館の客席",
        "映画館のロビー",
        "映画館の便所",
        "映画館の喫煙室",
        "図書館の図書室",
        "図書館のロビー",
        "図書館の便所",
        "図書館の喫煙室",
        "博物館の展示室",
        "博物館のロビー",
        "博物館の便所",
        "博物館の喫煙室",
        "劇場の楽屋",
        "劇場の舞台",
        "劇場の客席",
        "劇場のロビー",
        "劇場の便所",
        "劇場の喫煙室",
        "カラオケボックス",
        "ボーリング場",
        "ぱちんこ屋",
        "競馬場又は競輪場の客席",
        "競馬場又は競輪場の券売場",
        "競馬場又は競輪場の店舗",
        "競馬場又は競輪場のロビー",
        "競馬場又は競輪場の便所",
        "競馬場又は競輪場の喫煙室",
        "社寺の本殿",
        "社寺のロビー",
        "社寺の便所",
        "社寺の喫煙室",
        "厨房",
        "屋内駐車場",
        "機械室",
        "電気室",
        "湯沸室等",
        "食品庫等",
        "印刷室等",
        "廃棄物保管場所等",
        "非主要室",
    ] = Field(
        alias="roomType",  # NOTE: for builelib compatibility
    )


class FactoryRoom(BaseRoom):
    """工場等

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["工場等"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal["倉庫", "屋外駐車場又は駐輪場"]


class ResidentialComplexRoom(BaseRoom):
    """共同住宅

    Attributes:
        floor: 階
        name: 名称
        main_building_type: 建物用途
        building_type: 室用途(大分類)
        room_type: 室用途(小分類)
        floor_height: 階高
        ceiling_height: 天井高
        room_area: 床面積
        zone: ゾーン
        building_model_type: モデル建物
        building_group: 建物群名称
    """

    building_type: Literal["共同住宅"] = Field(
        alias="buildingType",  # NOTE: for builelib compatibility
    )

    room_type: Literal[
        "屋内廊下",
        "ロビー",
        "管理人室",
        "集会室",
        "屋外廊下",
        "屋内駐車場",
        "機械室",
        "電気室",
        "廃棄物保管場所等",
    ]
