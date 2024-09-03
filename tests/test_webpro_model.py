import json

from truzt.webpro_model import WebproModel


def test_webpro_model_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        wm_dict = json.load(file)

    # WebproModelインスタンスを作成
    wm = WebproModel.model_validate(wm_dict)
    # serialize
    wm_serialized_dict = wm.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert wm_dict == wm_serialized_dict
