import json

from truzt.webpro_model import WebproModel
from truzt.webpro_reader import read_webpro_excel


def test_webpro_model_json_serialize():
    """WebproModelのシリアライズのテスト."""
    # JSONファイルを読み込む
    with open("sample/sample_input_v3.json") as file:
        wm_dict = json.load(file)

    # WebproModelインスタンスを作成
    wm = WebproModel.model_validate(wm_dict)
    # serialize
    wm_serialized_dict = wm.model_dump(by_alias=True, exclude_unset=True)

    # check if the original dict and the serialized
    assert wm_dict == wm_serialized_dict


def test_webpro_model_excel_read():
    """ExcelファイルからWebproModelを生成するテスト."""
    # Excelファイルを読み込む
    wm_excel = read_webpro_excel("sample/sample_input_v3.xlsx")

    # JSONファイルを読み込む（参照データ）
    with open("sample/sample_input_v3.json") as file:
        wm_dict = json.load(file)

    # Excel読み込みとJSON読み込みの結果を比較
    wm_excel_dict = wm_excel.model_dump(by_alias=True, exclude_unset=True)
    print("JSON keys:", wm_dict.keys())
    print("Excel keys:", wm_excel_dict.keys())

    # 1F_EVホールの内容を比較
    json_zone = wm_dict["AirConditioningZone"]["1F_EVホール"]
    excel_zone = wm_excel_dict["AirConditioningZone"]["1F_EVホール"]

    print("\n1F_EVホール (JSON):", json.dumps(json_zone, indent=2, ensure_ascii=False))
    print("\n1F_EVホール (Excel):", json.dumps(excel_zone, indent=2, ensure_ascii=False))

    # 比較テストを実行
    assert wm_dict["AirConditioningZone"] == wm_excel_dict["AirConditioningZone"]
