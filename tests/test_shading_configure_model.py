from truzt.shading_configure_model import ShadingConfigure


# TODO: sample/sample_v3.jsonでは
# ShadingConfigureの入力がないからがないから意味ないけど
def test_shading_configure_json_serialize(v3_test_case_dict):
    data = v3_test_case_dict

    # ShadingConfigureのdictを取得
    sc_dict = data["ShadingConfigure"]

    sc_serialized_dict = {}
    for key in sc_dict.keys():
        # ShadingConfigureインスタンスを作成
        sc = ShadingConfigure.model_validate(sc_dict[key])
        # serialize
        sc_serialized_dict[key] = sc.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert sc_dict == sc_serialized_dict
