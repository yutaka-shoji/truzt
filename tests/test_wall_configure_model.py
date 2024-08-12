import json

from truzt import WallConfigure


def test_wall_configure_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # WallConfigureのdictを取得
    wc_dict = data["WallConfigure"]

    wc_serialized_dict = {}
    for key in wc_dict.keys():
        # WallConfigureインスタンスを作成
        wc = WallConfigure.model_validate(wc_dict[key])
        # serialize
        wc_serialized_dict[key] = wc.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert wc_dict == wc_serialized_dict
