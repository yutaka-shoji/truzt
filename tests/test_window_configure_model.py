import json

from truzt.window_configure_model import WindowConfigure


def test_window_configure_json_serialize():
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        data = json.load(file)

    # WindowConfigureのdictを取得
    wc_dict = data["WindowConfigure"]

    wc_serialized_dict = {}
    for key in wc_dict.keys():
        # WindowConfigureインスタンスを作成
        wc = WindowConfigure.model_validate(wc_dict[key])
        # serialize
        wc_serialized_dict[key] = wc.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert wc_dict == wc_serialized_dict
