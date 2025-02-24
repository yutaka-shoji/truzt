import json

import pytest
from openpyxl import Workbook


@pytest.fixture
def v3_test_case_dict() -> dict:
    with open("sample/sample_v3.json") as file:
        data = json.load(file)
    return data


@pytest.fixture
def v3_test_case_wb() -> Workbook:
    with open("sample/sample_v3.xlsx") as file:
        data = json.load(file)
    return data


@pytest.fixture
def v3_test_case_excel_path() -> str:
    return "sample/sample_v3.xlsx"


@pytest.fixture
def v3_test_case_json_path() -> str:
    return "sample/sample_v3.json"
