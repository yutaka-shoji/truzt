import json
from webpro_data_model import (
    WebProModel,
    Building,
    BuildingAddress,
    CoefficientDHC,
    OfficeRoom,
)

building = Building(
    name="test",
    region=1,
    annual_solar_region="A1",
    building_floor_area=1000.0,
    coefficient_dhc=CoefficientDHC(),
    building_address=BuildingAddress(),
)
office_room = OfficeRoom(
    name="officeroom",
    floor="1F",
    room_area=10.0,
    floor_height=2.7,
    ceiling_height=2.5,
    building_type="事務所等",
    room_type="事務所等",
    room_type_detail="事務室",
)

model = WebProModel(
    building=building,
    rooms=[office_room],
)

model_dict = model.model_dump()
model_json = model.model_dump_json(indent=2)
print(model_json)
# save to file
with open("model.json", "w") as f:
    f.write(model_json)

model2 = WebProModel(**model_dict)
model2.rooms[0].room_area = -10.0
print(model2.model_dump_json(indent=2))
