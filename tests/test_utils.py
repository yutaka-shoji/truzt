from pathlib import Path

import truzt


def test_can_convert_wb_to_json(v3_test_case_excel_path, tmp_path: Path):
    # file name without extensionを取得して、jsonファイル名を作成
    json_path = v3_test_case_excel_path.replace(".xlsx", ".out.json")
    truzt.utils.convert_wb_to_json(Path(v3_test_case_excel_path), Path(json_path))
