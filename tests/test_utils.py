from pathlib import Path

import truzt


def test_can_convert_wb_to_json():
    wb_path = "sample/sample_input_v3.xlsx"
    json_path = "out/sample_input_v3.json"

    truzt.utils.convert_wb_to_json(Path(wb_path), Path(json_path))


if __name__ == "__main__":
    test_can_convert_wb_to_json()
