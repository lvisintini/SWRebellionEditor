import struct
import os
from io import BytesIO
from collections import namedtuple, OrderedDict
from . import ALL_MANAGERS
from .exceptions import SWRebellionEditorDataFileHeaderMismatchError
from .constants import FieldType

FieldDef = namedtuple('StrucFormatDef', ['format', 'type'])


class SWRBaseDataManager:
    filename = None
    file_location = 'GDATA'
    header_struct_format = None
    expected_header = None
    byte_order = '<'  # we assume little-endian https://docs.python.org/3/library/struct.html#struct-alignment

    def __init__(self, data_path=None):
        self.data_path = data_path or os.getenv('SW_REBELLION_DIR')
        self.file_path = os.path.join(self.data_path, self.file_location, self.filename)
        self.header_struct = struct.Struct(self.byte_order + self.header_struct_format)
        self.header_stream = None
        self.data_struct = None
        self.data_stream = None
        self.data = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.filename:
            ALL_MANAGERS.append(cls)
            ALL_MANAGERS.sort(key=lambda m: m.filename)

    def load_file(self):
        self.header_stream = BytesIO()
        self.data_stream = BytesIO()
        with open(self.file_path, "rb") as data_file:
            self.header_stream.write(data_file.read(self.header_struct.size))
            self.data_stream.write(data_file.read())

        self.header_stream.seek(0)
        self.data_stream.seek(0)

        header = self.header_struct.unpack(self.header_stream.read())

        self.header_stream.seek(0)

        if header != self.expected_header:
            raise SWRebellionEditorDataFileHeaderMismatchError(
                f'Manager {self.__class__.__name__} expected header '
                f'{self.expected_header} for data file , but got {header} instead.'
            )

        self.data = []
        for data_tuple in self.data_struct.iter_unpack(self.data_stream.read()):
            data = self.process_data_tuple(data_tuple)
            self.data.append(data)

    def process_data_tuple(self, data_tuple):
        return data_tuple


class SimpleSWRDataManager(SWRBaseDataManager):
    data_struct_format = None

    def __init__(self, data_path=None):
        super().__init__(data_path=data_path)
        self.data_struct = struct.Struct(self.byte_order + self.data_struct_format)


class SWRDataManager(SWRBaseDataManager):

    # The data in the headers appears to support that:
    # - The second number is the row count in the file
    # - The third number is the lowest family_id value in the file
    header_struct_format = "IIII"

    data_fields_structure = None

    def __init__(self, data_path=None, fetch_name=False):
        super().__init__(data_path=data_path)
        self.fetch_names = fetch_name

        self.field_names = list(self.data_fields_structure.keys())

        self.header_struct = struct.Struct(
            self.byte_order + self.header_struct_format
        )
        self.data_struct = struct.Struct(
            self.byte_order + ''.join([field.format for field in self.data_fields_structure.values()])
        )

    def process_data_tuple(self, data_tuple):
        data_dict = dict(zip(self.field_names, data_tuple))
        if 'identifier_part_1' in data_dict and self.fetch_names:
            name = self.get_name(data_dict['identifier_part_1'])
            if name:
                data_dict['name'] = name
        return data_dict

    def get_name(self, name_id):
        #https://stackoverflow.com/questions/23263599/how-to-extract-128x128-icon-bitmap-data-from-exe-in-python
        #https://github.com/team5499/pie-2015/blob/master/VrepRobotCPortable/Python/App2/Lib/site-packages/py2exe
        #/resources/StringTables.py
        # general name -> print(c['name'], ' -> ', manager.get_name(c['identifier_part_1'] + 28672))
        # commander name ->  print(c['name'], ' -> ',  manager.get_name(c['identifier_part_1'] + 26624))
        # admiral name -> print(c['name'], ' -> ', manager.get_name(c['identifier_part_1'] + 27648))
        try:
            import win32api
            import pywintypes
        except ModuleNotFoundError:
            return None
        try:
            textstra_lib = win32api.LoadLibrary(os.path.join(self.data_path, "TEXTSTRA.DLL"))
            return win32api.LoadString(textstra_lib, name_id)
        except pywintypes.error:
            return None


class FightersDataManager(SWRDataManager):
    filename = "FIGHTSD.DAT"
    expected_header = (1, 8, 28, 32)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 40
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 41
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 28
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_1", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier, always 0
        ("detection", FieldDef('I', FieldType.EDITABLE)),
        ("shield", FieldDef('I', FieldType.EDITABLE)),
        ("sublight_speed", FieldDef('I', FieldType.EDITABLE)),
        ("maneuverability", FieldDef('I', FieldType.EDITABLE)),
        ("hyperdrive", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # backup hyperdrive, always 0
        ("turbolaser_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("turbolasers_range", FieldDef('I', FieldType.EDITABLE)),
        ("ion_range", FieldDef('I', FieldType.EDITABLE)),
        ("laser_range", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("ion_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("laser_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("torpedo_power", FieldDef('I', FieldType.EDITABLE)),
        ("torpedo_range", FieldDef('I', FieldType.EDITABLE)),
        ("squadron_size", FieldDef('I', FieldType.EDITABLE)),  # always 12
        ("bombardment", FieldDef('I', FieldType.EDITABLE)),
    ])


class TroopsDataManager(SWRDataManager):
    filename = "TROOPSD.DAT"
    expected_header = (1, 10, 16, 20)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 41
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 42
        ("family_id", FieldDef('I', FieldType.EDITABLE)),  # always 16
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier, always 0
        ("detection", FieldDef('I', FieldType.EDITABLE)),
        ("bombardment_defense", FieldDef('I', FieldType.EDITABLE)),
        ("attack", FieldDef('I', FieldType.EDITABLE)),
        ("defense", FieldDef('I', FieldType.EDITABLE)),
    ])


class CapitalShipsDataManager(SWRDataManager):
    filename = "CAPSHPSD.DAT"
    expected_header = (1, 30, 20, 28)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 40
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 41
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # 20 for the Capital Ships and 24 for the Death Star
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.READ_ONLY)),
        ("imperial", FieldDef('I', FieldType.READ_ONLY)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_1", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier, basicly 0.45 * construction_cost
        ("detection", FieldDef('I', FieldType.EDITABLE)),
        ("shield", FieldDef('I', FieldType.EDITABLE)),
        ("sublight_speed", FieldDef('I', FieldType.EDITABLE)),
        ("maneuverability", FieldDef('I', FieldType.EDITABLE)),
        ("hyperdrive", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # backup hyperdrive, always 0
        ("turbolaser_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_front", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_rear", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_left", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("ion_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("laser_firepower_right", FieldDef('I', FieldType.EDITABLE)),
        ("turbolasers_range", FieldDef('I', FieldType.EDITABLE)),
        ("ion_range", FieldDef('I', FieldType.EDITABLE)),
        ("laser_range", FieldDef('I', FieldType.EDITABLE)),
        ("turbolaser_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("ion_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("laser_firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("firepower_sum", FieldDef('I', FieldType.DENORMALIZED)),
        ("hull", FieldDef('I', FieldType.EDITABLE)),
        ("tractor_beam_power", FieldDef('I', FieldType.EDITABLE)),
        ("tractor_beam_range", FieldDef('I', FieldType.EDITABLE)),
        ("gravity_well_1", FieldDef('H', FieldType.EDITABLE)),  # 4 if present
        ("gravity_well_2", FieldDef('H', FieldType.EDITABLE)),  # 100 if present
        ("unknown_4", FieldDef('I', FieldType.READ_ONLY)),  # Always 0
        ("bombardment", FieldDef('I', FieldType.EDITABLE)),
        ("damage_control", FieldDef('I', FieldType.EDITABLE)),
        ("weapon_recharge", FieldDef('I', FieldType.EDITABLE)),
        ("shield_recharge", FieldDef('I', FieldType.EDITABLE)),
        ("fighter_squadrons", FieldDef('I', FieldType.EDITABLE)),
        ("troop_contingents", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_5", FieldDef('I', FieldType.EDITABLE))
    ])


class SectorsDataManager(SWRDataManager):
    filename = "SECTORSD.DAT"
    expected_header = (1, 20, 128, 144)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 100
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 128
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("importance", FieldDef('I', FieldType.EDITABLE)),  # 1-high 2-medium 3-low
        ("game_size", FieldDef('I', FieldType.EDITABLE)),  # 1-Small 2-Medium 3-Large
        ("position_x", FieldDef('H', FieldType.EDITABLE)),
        ("position_y", FieldDef('H', FieldType.EDITABLE)),
    ])


class MissionDataManager(SWRDataManager):
    filename = "MISSNSD.DAT"
    expected_header = (1, 25, 64, 128)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("active", FieldDef('I', FieldType.UNKNOWN)),
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.READ_ONLY)),
        ("imperial", FieldDef('I', FieldType.READ_ONLY)),
        ("tbd_03", FieldDef('I', FieldType.READ_ONLY)),  # Number
        ("tbd_04", FieldDef('I', FieldType.READ_ONLY)),  # Number
        ("tbd_05", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_06", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_07", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_08", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_09", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_10", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_11", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_12", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_13", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_14", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_15", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_16", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_17", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_18", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_19", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_20", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_21", FieldDef('I', FieldType.READ_ONLY)),  # 10
        ("tbd_22", FieldDef('I', FieldType.READ_ONLY)),  # 10
    ])


class SystemsDataManager(SWRDataManager):
    filename = "SYSTEMSD.DAT"
    expected_header = (1, 200, 144, 152)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 100
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # 144 core systems and 146 for out rim systems
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("sector_number", FieldDef('I', FieldType.EDITABLE)),  # starting from 20
        ("type", FieldDef('I', FieldType.EDITABLE)),  # picture? 1-26
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # always 1
        ("position_x", FieldDef('H', FieldType.EDITABLE)),
        ("position_y", FieldDef('H', FieldType.EDITABLE)),
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # always 0
    ])


class DefensiveFacilitiesDataManager(SWRDataManager):
    filename = "DEFFACSD.DAT"
    expected_header = (1, 6, 34, 40)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 1
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 42
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 43
        # 34 for ion, 35 for lasers, 36 for shields and 37 for Death Star shield
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("bombardment_defense", FieldDef('I', FieldType.UNKNOWN)),
        ("firepower", FieldDef('I', FieldType.EDITABLE)),
        ("shield_generation", FieldDef('I', FieldType.EDITABLE)),
    ])


class ManufacturingFacilitiesDataManager(SWRDataManager):
    filename = "MANFACSD.DAT"
    expected_header = (1, 6, 40, 44)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 1
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 42
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 43
        # 40 for shipyards, 41 for training facilities and 42 for construction yards
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("bombardment_defense", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier
        ("manufacturing_rate", FieldDef('I', FieldType.EDITABLE)),  # required days to manufacture 1 unit
    ])


class SpecialForcesDataManager(SWRDataManager):
    filename = "SPECFCSD.DAT"
    expected_header = (1, 9, 60, 64)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("active", FieldDef('I', FieldType.UNKNOWN)),
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),
        ("research_order", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("unknown_5", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("diplomacy_base", FieldDef('I', FieldType.EDITABLE)),
        ("diplomacy_variance", FieldDef('I', FieldType.EDITABLE)),
        ("espionage_base", FieldDef('I', FieldType.EDITABLE)),
        ("espionage_variance", FieldDef('I', FieldType.EDITABLE)),
        ("ship_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("ship_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("troop_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("troop_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("facility_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("facility_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("combat_base", FieldDef('I', FieldType.EDITABLE)),
        ("combat_variance", FieldDef('I', FieldType.EDITABLE)),
        ("leadership_base", FieldDef('I', FieldType.EDITABLE)),
        ("leadership_variance", FieldDef('I', FieldType.EDITABLE)),
        ("loyalty_base", FieldDef('I', FieldType.EDITABLE)),
        ("loyalty_variance", FieldDef('I', FieldType.EDITABLE)),
        ("mission_available", FieldDef('I', FieldType.EDITABLE)),  # related to MISSIONSD ?
    ])


class ProductionFacilitiesDataManager(SWRDataManager):
    filename = "PROFACSD.DAT"
    expected_header = (1, 2, 44, 48)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # 1 for both
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 42
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 43
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # 44 for mines and 45 for refineries
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.EDITABLE)),
        ("maintenance", FieldDef('I', FieldType.EDITABLE)),  # 0 for both
        ("research_order", FieldDef('I', FieldType.EDITABLE)),   # 0 for both
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("bombardment_defense", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier
        ("production _rate", FieldDef('I', FieldType.EDITABLE)),  # required days to manufacture 1 unit
    ])


class CharacterBaseDataManager(SWRDataManager):
    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 576
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        # 48 for Mon Mothma, 49 for Leia Organa, 50 for Luke Skywalker, 51 for Han Solo, 52 for Emperor Palpatine,
        # 52 for Darth Vader  and 56 for Minor characters
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('I', FieldType.EDITABLE)),
        ("imperial", FieldDef('I', FieldType.EDITABLE)),
        ("construction_cost", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("maintenance", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("research_order", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("unknown_5", FieldDef('I', FieldType.UNKNOWN)),  # always 0
        ("diplomacy_base", FieldDef('I', FieldType.EDITABLE)),
        ("diplomacy_variance", FieldDef('I', FieldType.EDITABLE)),
        ("espionage_base", FieldDef('I', FieldType.EDITABLE)),
        ("espionage_variance", FieldDef('I', FieldType.EDITABLE)),
        ("ship_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("ship_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("troop_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("troop_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("facility_research_base", FieldDef('I', FieldType.EDITABLE)),
        ("facility_research_variance", FieldDef('I', FieldType.EDITABLE)),
        ("combat_base", FieldDef('I', FieldType.EDITABLE)),
        ("combat_variance", FieldDef('I', FieldType.EDITABLE)),
        ("leadership_base", FieldDef('I', FieldType.EDITABLE)),
        ("leadership_variance", FieldDef('I', FieldType.EDITABLE)),
        ("loyalty_base", FieldDef('I', FieldType.EDITABLE)),
        ("loyalty_variance", FieldDef('I', FieldType.EDITABLE)),
        ("jedi_probability", FieldDef('I', FieldType.EDITABLE)),
        ("known_jedi", FieldDef('I', FieldType.EDITABLE)),
        ("jedi_level_base", FieldDef('I', FieldType.EDITABLE)),
        ("jedi_level_variance", FieldDef('I', FieldType.EDITABLE)),
        ("can_be_admiral", FieldDef('I', FieldType.EDITABLE)),
        ("can_be_commander", FieldDef('I', FieldType.EDITABLE)),
        ("can_be_general", FieldDef('I', FieldType.EDITABLE)),
        ("wont_betray_own_side", FieldDef('I', FieldType.EDITABLE)),
        ("can_train_jedis", FieldDef('I', FieldType.EDITABLE)),
    ])


class MajorCharacterDataManager(CharacterBaseDataManager):
    filename = "MJCHARSD.DAT"
    expected_header = (1, 6, 48, 56)


class MinorCharacterDataManager(CharacterBaseDataManager):
    filename = "MNCHARSD.DAT"
    expected_header = (1, 54, 56, 60)


class SystemFacilityTableDataManager(SWRDataManager):
    header_struct_format = "III14s"

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("number2", FieldDef('I', FieldType.READ_ONLY)),  # always 1
        ("percent", FieldDef('I', FieldType.READ_ONLY)),
        ("level", FieldDef('H', FieldType.READ_ONLY)),
        ("unknown", FieldDef('B', FieldType.READ_ONLY)),  # always 0
        ("family_id", FieldDef('B', FieldType.READ_ONLY)),
    ])


class SystemFacilityCoreTableDataManager(SystemFacilityTableDataManager):
    filename = "SYFCCRTB.DAT"
    expected_header = (1, 8, 14, b'SeedTableEntry')


class SystemFacilityRimTableDataManager(SystemFacilityTableDataManager):
    filename = "SYFCRMTB.DAT"
    expected_header = (1, 7, 14, b'SeedTableEntry')


class TableDataBaseManager(SWRDataManager):
    header_struct_format = "III13s"


class ProbabilityTableDataBaseManager(TableDataBaseManager):
    data_fields_structure = OrderedDict([
        ("index", FieldDef('I', FieldType.READ_ONLY)),
        ("one", FieldDef('I', FieldType.READ_ONLY)),
        ("score", FieldDef('i', FieldType.READ_ONLY)),
        ("probability", FieldDef('I', FieldType.READ_ONLY)),
    ])


class AssassinationMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "ASSNMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class AbductionMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "ABDCMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class DiplomacyMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "DIPLMSTB.DAT"
    expected_header = (1, 10, 13, b'IntTableEntry')


class DeathStarSabotageMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "DSSBMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class EspionageMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "ESPIMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class InciteUprisingMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "INCTMSTB.DAT"
    expected_header = (1, 13, 13, b'IntTableEntry')


class ReconnaissanceMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "RCRTMSTB.DAT"
    expected_header = (1, 11, 13, b'IntTableEntry')


class RescueMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "RESCMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class SabotageMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "SBTGMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')


class SubdueUprisingMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "SUBDMSTB.DAT"
    expected_header = (1, 13, 13, b'IntTableEntry')


class TroopDecoyTableDataManager(ProbabilityTableDataBaseManager):
    filename = "TDECOYTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')


class FleetDecoyTableDataManager(ProbabilityTableDataBaseManager):
    filename = "FDECOYTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')


class FoilMissionTableDataManager(ProbabilityTableDataBaseManager):
    filename = "FOILTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')


class SimpleTableDataManager(SimpleSWRDataManager):
    header_struct_format = "III13s"
    data_struct_format = 'IIiI'


class Uprising1TableDataManager(SimpleTableDataManager):
    filename = "UPRIS1TB.DAT"
    expected_header = (1, 3, 13, b'IntTableEntry')


class Uprising2TableDataManager(SimpleTableDataManager):
    filename = "UPRIS2TB.DAT"
    expected_header = (1, 4, 13, b'IntTableEntry')


class InformantsTableDataManager(SimpleTableDataManager):
    filename = "INFORMTB.DAT"
    expected_header = (1, 8, 13, b'IntTableEntry')


class EscapeAttemptTableDataManager(ProbabilityTableDataBaseManager):
    filename = "ESCAPETB.DAT"
    expected_header = (1, 9, 13, b'IntTableEntry')


class ResearchMissionTableDataManager(SimpleTableDataManager):
    filename = "RESRCTB.DAT"
    expected_header = (1, 4, 13, b'IntTableEntry')


class EvadeCaptureTableDataManager(ProbabilityTableDataBaseManager):
    filename = "RLEVADTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')


class GroupedTableBaseDataManager(SimpleSWRDataManager):
    header_struct_format = "III20s"
    data_struct_format = 'IIHBB'


class AllianceFleetHomeTableDataManager(GroupedTableBaseDataManager):
    filename = "CMUNEFTB.DAT"

    expected_header = (1, 1, 20, b'SeedFamilyTableEntry')

    # (1, 1, 1, 0, 0)
    # (1, 1, 10, 0, 0)
    # (1, 0, 133, 0, 20)
    # (1, 0, 5, 0, 28)
    # (1, 0, 5, 0, 28)
    # (1, 0, 5, 0, 28)
    # (1, 0, 5, 0, 28)
    # (1, 0, 5, 0, 28)
    # (1, 0, 5, 0, 28)
    # (1, 0, 6, 0, 16)
    # (1, 0, 6, 0, 16)
    # (1, 0, 6, 0, 16)


class EmpireFleetHomeTableDataManager(GroupedTableBaseDataManager):
    filename = "CMUNAFTB.DAT"
    expected_header = (1, 2, 20, b'SeedFamilyTableEntry')

    # (1, 1, 1, 0, 0)
    # (1, 1, 1, 0, 0)
    # (1, 0, 69, 0, 20)
    # (2, 1, 2, 0, 0)
    # (1, 1, 3, 0, 0)
    # (1, 0, 70, 0, 20)
    # (1, 0, 1, 0, 16)
    # (1, 0, 1, 0, 16)
