"""Module for defining the AirConditioningZoneReader class."""

from .air_conditioning_zone_model import AirConditioningZones
from .reader import ExcelReader


class AirConditioningZoneReader(ExcelReader[AirConditioningZones]):
    """Class for reading air conditioning zone data from Excel workbook."""

    @property
    def _component_name(self) -> str:
        return "air_conditioning_zone"

    def read(self) -> AirConditioningZones:
        """Read air conditioning zone data from Excel workbook.

        Returns:
            AirConditioningZones: Air conditioning zone data.
        """
        sheet_name = self.cell_mapping["sheet"]
        cells = self.cell_mapping["cells"]

        air_conditioning_zones = {}
        for i_row in range(cells["min_row"], 999):
            # break if the first cell is empty or white space
            floor = self.read_cell(sheet_name, f"{cells['floor']}{i_row}", optional=True)
            if floor is None or not str(floor).strip():
                break

            name = self.read_cell(sheet_name, f"{cells['name']}{i_row}")

            # Skip if no load
            if all(
                self.read_cell(sheet_name, f"{cells[key]}{i_row}", optional=True) is None
                for key in [
                    "ahu_cooling_inside_load",
                    "ahu_cooling_outdoor_load",
                    "ahu_heating_inside_load",
                    "ahu_heating_outdoor_load",
                ]
            ):
                continue

            room_key = f"{floor}_{name}"

            # 共通の処理
            ahu_cooling_inside_load = (
                self.read_cell(
                    sheet_name, f"{cells['ahu_cooling_inside_load']}{i_row}", optional=True
                )
                or ""
            )
            ahu_cooling_outdoor_load = (
                self.read_cell(
                    sheet_name, f"{cells['ahu_cooling_outdoor_load']}{i_row}", optional=True
                )
                or ""
            )
            ahu_heating_inside_load = (
                self.read_cell(
                    sheet_name, f"{cells['ahu_heating_inside_load']}{i_row}", optional=True
                )
                or ""
            )
            ahu_heating_outdoor_load = (
                self.read_cell(
                    sheet_name, f"{cells['ahu_heating_outdoor_load']}{i_row}", optional=True
                )
                or ""
            )
            info = self.read_cell(sheet_name, f"{cells['info']}{i_row}", optional=True) or ""

            if self.version == "v2":
                air_conditioning_zones[room_key] = {
                    "isNatualVentilation": False,
                    "isSimultaneousSupply": "無",
                    "AHU_cooling_insideLoad": ahu_cooling_inside_load,
                    "AHU_cooling_outdoorLoad": ahu_cooling_outdoor_load,
                    "AHU_heating_insideLoad": ahu_heating_inside_load,
                    "AHU_heating_outdoorLoad": ahu_heating_outdoor_load,
                    "Info": info,
                }
            else:
                air_conditioning_zones[room_key] = {
                    "isNatualVentilation": self.read_cell(
                        sheet_name, f"{cells['is_natural_ventilation']}{i_row}", optional=True
                    )
                    == "有",
                    "isSimultaneousSupply": self.read_cell(
                        sheet_name, f"{cells['is_simultaneous_supply']}{i_row}", optional=True
                    )
                    or "無",
                    "AHU_cooling_insideLoad": ahu_cooling_inside_load,
                    "AHU_cooling_outdoorLoad": ahu_cooling_outdoor_load,
                    "AHU_heating_insideLoad": ahu_heating_inside_load,
                    "AHU_heating_outdoorLoad": ahu_heating_outdoor_load,
                    "Info": info,
                }

        return AirConditioningZones.model_validate(air_conditioning_zones)
