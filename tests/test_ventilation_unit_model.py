import json

from truzt.models import VentilationUnit


def test_ventilation_unit_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json", "r") as file:
        data = json.load(file)

    # VentilationUnitのdictを取得
    vu_dict = data["VentilationUnit"]

    vu_serialized_dict = {}
    for key in vu_dict.keys():
        # VentilationUnitインスタンスを作成
        vu = VentilationUnit.model_validate(vu_dict[key])
        # serialize
        vu_serialized_dict[key] = vu.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert vu_dict == vu_serialized_dict
