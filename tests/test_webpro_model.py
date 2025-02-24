from truzt.webpro_model import WebproModel


def test_webpro_model_json_serialize(v3_test_case_dict):
    """WebproModelのシリアライズのテスト."""
    wm_dict = v3_test_case_dict

    # WebproModelインスタンスを作成
    wm = WebproModel.model_validate(wm_dict)
    # serialize
    wm_serialized_dict = wm.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert wm_dict == wm_serialized_dict
