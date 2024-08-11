import json

from truzt.models import Elevators


def test_elevators_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json", "r") as file:
        data = json.load(file)

    # Elevatorsのdictを取得
    elevators_dict = data["Elevators"]

    elevators_serialized_dict = {}
    for key in elevators_dict.keys():
        # Elevatorsインスタンスを作成
        elevators = Elevators.model_validate(elevators_dict[key])
        # serialize
        elevators_serialized_dict[key] = elevators.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert elevators_dict == elevators_serialized_dict
