"""Module for defining the EnvelopeSet model."""

from typing import Annotated, Any, Literal, Optional

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import Field, RootModel, field_validator

from truzt.model_config import BaseConfigModel


class WindowListItem(BaseConfigModel):
    """Window list item.

    NOTE: builelibでは窓面積をWindowNumberに入れている?

    Attributes:
        window_id: 開口部仕様名称
        window_number: 建具等個数
        is_blind: ブラインドの有無
        eaves_id: 日除けの名称
        info: 備考
    """

    window_id: Annotated[
        Optional[str],
        Field(
            alias="WindowID",  # NOTE: for builelib compatibility
        ),
    ] = None
    window_number: Optional[float] = Field(
        None,
        gt=0,
    )
    is_blind: Annotated[
        Optional[Literal["有", "無"]],
        Field(
            alias="isBlind",  # NOTE: for builelib compatibility
        ),
    ] = None
    eaves_id: Annotated[
        Optional[str],
        Field(
            alias="EavesID",  # NOTE: for builelib compatibility
        ),
    ] = None
    info: Optional[str] = None

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class WallListItem(BaseConfigModel):
    """Wall list item.

    Attributes:
        direction: 方位
        envelope_area: 外皮面積
        envelope_width: 外皮の幅
        envelope_height: 外皮の高さ
        wall_spec: 断熱仕様名称
        wall_type: 外壁の種類
        window_list: 窓リスト
    """

    direction: Optional[
        Literal[
            "北",
            "北東",
            "東",
            "南東",
            "南",
            "南西",
            "西",
            "北西",
            "水平（上）",
            "水平（下）",
        ]
    ] = None

    @field_validator("direction", mode="before")
    @classmethod
    def normalize_direction(cls, v: Any) -> Any:
        """方位の値を正規化する.

        Args:
            v: 方位の値

        Returns:
            正規化された方位の値
        """
        if v is None:
            return None

        # 文字列に変換
        v_str = str(v)

        if v_str == "日陰":
            return "北"
        elif v_str == "水平":
            return "水平（下）"
        return v

    envelope_area: Optional[float] = Field(
        None,
        gt=0,
    )

    envelope_width: Optional[float] = Field(
        None,
        gt=0,
    )

    envelope_height: Optional[float] = Field(
        None,
        gt=0,
    )

    wall_spec: Optional[str] = Field(
        None,
    )

    wall_type: Optional[
        Literal[
            "日の当たる外壁",
            "日の当たらない外壁",
            "地盤に接する外壁",
            "内壁",
        ]
    ] = None

    window_list: list[WindowListItem]


class EnvelopeSet(BaseConfigModel):
    """Envelope set.

    Attributes:
        is_air_conditioned: 空調の有無
        wall_list: 壁リスト
    """

    is_air_conditioned: Annotated[
        Optional[Literal["有", "無"]],
        Field(
            alias="isAirconditioned",  # NOTE: for builelib compatibility
        ),
    ] = None
    wall_list: list[WallListItem]

    # TODO: not implemented field serializer and validator yet
    # to convert "有" or "無" to boolean


class EnvelopeSets(RootModel):
    """EnvelopeSet dict.

    Attributes:
        root: EnvelopeSet dict.
    """

    root: dict[str, EnvelopeSet]

    @classmethod
    def from_workbook(cls, wb: Workbook, ver: Literal["v2", "v3"] = "v3") -> "EnvelopeSets":
        """WorkbookからEnvelopeSetsモデルを生成する.

        Args:
            wb: Workbook
            ver: WEBPRO input workbook version (v2 or v3).

        Returns:
            dict[str, EnvelopeSets]: EnvelopeSet dict
        """
        if ver == "v2":
            return cls._from_workbook_v2(wb)
        else:
            # TODO: v3のセル参照定義
            raise NotImplementedError("v3 is not implemented yet")

    @classmethod
    def _from_workbook_v2(cls, wb: Workbook) -> "EnvelopeSets":
        """WorkbookからEnvelopeSetsモデルを生成する (v2).

        Args:
            wb: Workbook

        Returns:
            EnvelopeSets: EnvelopeSet dict
        """
        # シート名と開始行の定義
        sheet_name = "2-4) 外皮 "
        start_row = 11  # DATA_START_ROW + 1 (0-indexedから1-indexedへの変換)

        # シートの取得
        try:
            ws = wb[sheet_name]
        except KeyError:
            # シートが存在しない場合は空のデータを返す
            return cls(root={})

        # データ格納用の辞書
        envelope_sets: dict[str, EnvelopeSet] = {}

        # 現在処理中のroomKey
        room_key = None

        # 行のループ
        for row in range(start_row, ws.max_row + 1):
            # row の全cellがNoneもしくは空文字の場合は終了
            if all(cell.value is None or cell.value == "" for cell in ws[row]):
                break

            # 行データの取得
            row_data = cls._extract_row_data(ws, row)
            floor, room = row_data["floor"], row_data["room"]
            direction = row_data["direction"]

            # 数値で入力された室名を文字列に変換
            if isinstance(room, (int, float)):
                room = str(int(room))

            # 階と室名が空欄でない場合 - 新しい部屋の開始
            if floor and room:
                room_key = f"{floor}_{room}"
                envelope_sets[room_key] = cls._create_new_envelope_set(row_data)

            # 階と室名が空欄である場合（既存のroomKeyに対する追加情報）
            elif room_key and room_key in envelope_sets:
                if not direction and row_data["wall_name"]:
                    # 方位が空白で外壁名称に入力があるケース（エラーケース）
                    continue
                elif not direction:
                    # 方位が空白である場合 → 既存の壁に窓を追加
                    cls._add_window_to_last_wall(envelope_sets[room_key], row_data, append=True)
                else:
                    # 方位が空白ではない場合 → 新しい壁を追加
                    cls._add_new_wall_to_envelope_set(envelope_sets[room_key], row_data)

        return cls(root=envelope_sets)

    @classmethod
    def _extract_row_data(cls, ws: Worksheet, row: int) -> dict:
        """ワークシートの行からデータを抽出する.

        Args:
            ws: ワークシート
            row: 行番号

        Returns:
            dict: 抽出されたデータ
        """
        return {
            "floor": ws.cell(row=row, column=1).value,  # 階
            "room": ws.cell(row=row, column=2).value,  # 室名
            "direction": ws.cell(row=row, column=3).value,  # 方位
            "wall_name": ws.cell(row=row, column=6).value,  # 外壁名称
            "env_area": ws.cell(row=row, column=7).value,  # 外皮面積
            "window_name": ws.cell(row=row, column=8).value,  # 開口部名称
            "window_area": ws.cell(row=row, column=9).value,  # 窓面積
            "blind": ws.cell(row=row, column=10).value,  # ブラインドの有無
            "remarks": ws.cell(row=row, column=11).value,  # 備考
        }

    @classmethod
    def _create_wall_data(cls, row_data: dict) -> dict:
        """壁データを作成する.

        Args:
            row_data: 行データ

        Returns:
            dict: 壁データ
        """
        direction = row_data["direction"]
        env_area = row_data["env_area"]
        wall_name = row_data["wall_name"]

        wall_type = cls._normalize_direction(str(direction)) if direction else None

        return {
            "direction": direction,
            "envelope_area": float(str(env_area)) if env_area is not None else None,
            "envelope_width": None,
            "envelope_height": None,
            "wall_spec": wall_name,
            "wall_type": wall_type,
            "window_list": [],
        }

    @classmethod
    def _create_window_data(cls, row_data: dict) -> dict:
        """窓データを作成する.

        Args:
            row_data: 行データ

        Returns:
            dict: 窓データ
        """
        window_name = row_data["window_name"]
        window_area = row_data["window_area"]
        blind = row_data["blind"]
        remarks = row_data["remarks"]

        if window_name:
            return {
                "window_id": window_name,
                "window_number": float(str(window_area)) if window_area else None,
                "is_blind": blind if blind else "無",
                "eaves_id": "無",
                "info": remarks,
            }
        else:
            return {
                "window_id": "無",
                "window_number": None,
                "is_blind": "無",
                "eaves_id": "無",
                "info": None,
            }

    @classmethod
    def _create_new_envelope_set(cls, row_data: dict) -> EnvelopeSet:
        """新しいEnvelopeSetを作成する.

        Args:
            row_data: 行データ

        Returns:
            EnvelopeSet: 作成されたEnvelopeSet
        """
        wall_data = cls._create_wall_data(row_data)
        wall = WallListItem(**wall_data)

        envelope_set = EnvelopeSet(
            is_air_conditioned="有",
            wall_list=[wall],
        )

        # 窓情報の追加
        cls._add_window_to_last_wall(envelope_set, row_data)

        return envelope_set

    @classmethod
    def _add_window_to_last_wall(
        cls, envelope_set: EnvelopeSet, row_data: dict, append: bool = False
    ) -> None:
        """最後の壁に窓を追加する.

        Args:
            envelope_set: EnvelopeSet
            row_data: 行データ
            append: 追加モード（Trueの場合は追加、Falseの場合は上書き）
        """
        window_data = cls._create_window_data(row_data)
        window = WindowListItem(**window_data)

        if append:
            envelope_set.wall_list[-1].window_list.append(window)
        else:
            envelope_set.wall_list[-1].window_list = [window]

    @classmethod
    def _add_new_wall_to_envelope_set(cls, envelope_set: EnvelopeSet, row_data: dict) -> None:
        """EnvelopeSetに新しい壁を追加する.

        Args:
            envelope_set: EnvelopeSet
            row_data: 行データ
        """
        wall_data = cls._create_wall_data(row_data)
        wall = WallListItem(**wall_data)

        envelope_set.wall_list.append(wall)

        # 窓情報の追加
        cls._add_window_to_last_wall(envelope_set, row_data)

    @staticmethod
    def _normalize_direction(direction: Optional[str]) -> Optional[str]:
        """方位の「日陰」と「水平」を正規化する.

        Args:
            direction: 方位

        Returns:
            正規化された方位
        """
        if not direction:
            return None

        if direction == "日陰":
            return "日の当たらない外壁"
        elif direction == "水平":
            return "日の当たる外壁"
        else:
            return "日の当たる外壁"
