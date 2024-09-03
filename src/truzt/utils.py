"""Utility functions."""

import json
from pathlib import Path

import openpyxl

from .room_model import Rooms

WEBPRO_SHEETS = (
    "0) 基本情報",
    "1) 室仕様",
    "2-1) 空調ゾーン",
    "2-2) 外壁構成 ",
    "2-3) 窓仕様",
    "2-4) 外皮 ",
    "2-5) 熱源",
    "2-6) 2次ﾎﾟﾝﾌﾟ",
    "2-7) 空調機",
    "2-8) 熱源水温度",
    "2-9) 全熱交換器",
    "3-1) 換気室",
    "3-2) 換気送風機",
    "3-3) 換気空調機",
    "3-4) 年間平均負荷率",
    "4) 照明",
    "5-1) 給湯室",
    "5-2) 給湯機器",
    "6) 昇降機",
    "7-1) 太陽光発電",
    "7-3) コージェネレーション設備",
    "8) 非空調外皮",
)


def convert_wb_to_json(wb_path: Path, json_path: Path) -> None:
    """Convert WEBPRO input workbook to JSON file.

    Args:
        wb_path: The path to the Excel workbook file.
        json_path: The path to the output JSON file.
    """
    model_dict = convert_wb_to_dict(wb_path)

    with open(json_path, "w") as f:
        json.dump(model_dict, f, indent=2, ensure_ascii=False)


def convert_wb_to_dict(wb_path: Path) -> dict:
    """Convert WEBPRO input workbook to dict.

    Args:
        wb_path: The path to the Excel workbook file.
    """
    wb = openpyxl.load_workbook(wb_path, read_only=True, data_only=True)

    # TODO: implement webpro version check
    ver = "v3"

    # WEBPRO_SHEETSのシートがすべて存在するか確認
    for sheet_name in WEBPRO_SHEETS:
        if sheet_name not in wb.sheetnames:
            raise ValueError(f"Sheet named '{sheet_name}' is not found.")

    # building = Building.from_workbook(wb, ver=ver)
    rooms = Rooms.from_workbook(wb, ver=ver)

    # TODO: implement other models

    model_dict = rooms.model_dump()

    return model_dict
