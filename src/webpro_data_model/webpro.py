from pydantic import BaseModel
from typing import Union
from webpro_data_model.room import (
    OfficeRoom,
    HotelRoom,
    HospitalRoom,
    DepartmentStoreRoom,
    SchoolRoom,
    RestaurantRoom,
    CommunityRoom,
    FactoryRoom,
    HousingRoom,
    ExistingRoom,
)
from webpro_data_model.building import Building


class WebProModel(BaseModel):
    building: Building
    rooms: list[
        Union[
            OfficeRoom,
            HotelRoom,
            HospitalRoom,
            DepartmentStoreRoom,
            SchoolRoom,
            RestaurantRoom,
            CommunityRoom,
            FactoryRoom,
            HousingRoom,
            ExistingRoom,
        ]
    ]
