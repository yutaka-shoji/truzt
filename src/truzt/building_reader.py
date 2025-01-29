"""Building readerの実装を提供するモジュール."""

from .building_model import Building, BuildingAddress, CoefficientDHC
from .reader import ExcelReader


class BuildingReader(ExcelReader[Building]):
    """BuildingModelの読み込みを行うクラス."""

    def read(self) -> Building:
        """Excelファイルから建物情報を読み込む.

        Returns:
            Building: 建物情報.

        Raises:
            ExcelReadError: 読み込みに失敗した場合.
        """
        sheet = self.cell_mapping["sheet"]

        # 建物住所の読み込み
        building_address = BuildingAddress(
            prefecture=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["building_address"]["prefecture"],
            ),
            city=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["building_address"]["city"],
                optional=True,
            ),
            address=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["building_address"]["address"],
            ),
        )

        # DHC係数の読み込み
        coefficient_dhc = CoefficientDHC(
            cooling=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["coefficient_dhc"]["cooling"],
            ),
            heating=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["coefficient_dhc"]["heating"],
            ),
        )

        # 建物情報の読み込み
        return Building(
            name=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["name"],
            ),
            building_address=building_address,
            region=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["region"],
            ),
            annual_solar_region=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["annual_solar_region"],
            ),
            building_floor_area=self.read_cell(
                sheet,
                self.cell_mapping["cells"]["building_floor_area"],
            ),
            coefficient_dhc=coefficient_dhc,
        )
