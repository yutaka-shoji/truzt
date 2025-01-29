"""Room readerの実装を提供するモジュール."""

from .reader import ExcelReader
from .room_model import Room, Rooms


class RoomReader(ExcelReader[Rooms]):
    """RoomModelの読み込みを行うクラス."""

    def read(self) -> Rooms:
        """Excelファイルから室情報を読み込む.

        Returns:
            Rooms: 室情報の辞書.

        Raises:
            ExcelReadError: 読み込みに失敗した場合.
        """
        sheet = self.cell_mapping["sheet"]
        cells = self.cell_mapping["cells"]
        min_row = cells["min_row"]

        rooms = {}
        for i_row in range(min_row, 999):
            # 最初のセルが空白または空文字の場合は終了
            floor_value = self.read_cell(sheet, f"{cells['floor']}{i_row}", optional=True)
            if not floor_value or not str(floor_value).strip():
                break

            # 階と室名を取得
            floor = floor_value
            name = self.read_cell(sheet, f"{cells['name']}{i_row}")
            room_key = f"{floor}_{name}"

            # 室情報の読み込み
            rooms[room_key] = Room(
                main_building_type=self.read_cell(
                    sheet,
                    f"{cells['main_building_type']}{i_row}",
                ),
                building_type=self.read_cell(
                    sheet,
                    f"{cells['building_type']}{i_row}",
                ),
                room_type=self.read_cell(
                    sheet,
                    f"{cells['room_type']}{i_row}",
                ),
                room_area=self.read_cell(
                    sheet,
                    f"{cells['room_area']}{i_row}",
                ),
                floor_height=self.read_cell(
                    sheet,
                    f"{cells['floor_height']}{i_row}",
                ),
                ceiling_height=self.read_cell(
                    sheet,
                    f"{cells['ceiling_height']}{i_row}",
                ),
                zone=None,  # ゾーン情報は別途読み込み
                building_model_type=self.read_cell(
                    sheet,
                    f"{cells['building_model_type']}{i_row}",
                    optional=True,
                ),
                info=self.read_cell(
                    sheet,
                    f"{cells['info']}{i_row}",
                    optional=True,
                ),
            )

        return Rooms(root=rooms)
