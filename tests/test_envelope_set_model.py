import json

from truzt import EnvelopeSet


def test_envelope_set_json_serialize():
    # JSONファイルを読み込む
    with open("sample/WEBPRO_inputSheet_sample_input.json") as file:
        data = json.load(file)

    # EnvelopeSetのdictを取得
    es_dict = data["EnvelopeSet"]

    es_serialized_dict = {}
    for key in es_dict.keys():
        # EnvelopeSetインスタンスを作成
        es = EnvelopeSet.model_validate(es_dict[key])
        # serialize
        es_serialized_dict[key] = es.model_dump(by_alias=True)

    # check if the original dict and the serialized
    assert es_dict == es_serialized_dict
