import struct
import os
from io import BytesIO
from collections import namedtuple, OrderedDict

import win32api

from .exceptions import SWRebellionEditorDataFileHeaderMismatchError
from .constants import FieldType

FieldDef = namedtuple('StrucFormatDef', ['format', 'type'])


class SWRDataManager:
    filename = None
    file_location = 'GData'
    expected_header = None

    # Verbatim -> http://forums.swrebellion.com/viewtopic.php?f=3&t=284
    # The normal gamedata files (all *sd.dat except basicsd.dat.) have a common header. It is four DWORD long:
    # - always 1
    # - the number of things consisted
    # - the "lower" consisted family identifier
    # - the "higher" (not consisted) family identifier
    #
    # The "higher" family identifier is usually is higher by steps of four except that of the facilities which are
    # separated.
    #
    # This does not apply to the *tb.dat files which have completely different structure.
    #
    # Eg:
    # The troop family is 16, so the header of the Troopsd.dat is 1,10,16,20.
    # Next are the capital ships: 1,30,20,28 (Death Star is 24 all others are 20), the fighters: 1,8,28,32, and
    # so on ...
    #
    # However when I tried to add a new sector (data to the sectorsd.dat and name to textstrat.dll)
    # to the game I failed so the number of consisted things (or maybe the file lenghts) must be stored elsewhere too.

    header_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # always 1
        ("count", FieldDef('I', FieldType.DENORMALIZED)),   # number of elements in file
        ("family", FieldDef('I', FieldType.READ_ONLY)),  # family id
        ("unknown", FieldDef('I', FieldType.DENORMALIZED)),  # the "higher" (not consisted) family identifier
    ])

    data_fields_structure = None

    def __init__(self, data_path=None):
        self.data_path = data_path or os.getenv('SW_REBELLION_DIR')
        self.file_path = os.path.join(self.data_path, self.file_location, self.filename)
        self.header_stream = None
        self.data_stream = None
        self.data_dicts = None

    def __init_subclass__(cls):
        super().__init_subclass__()

        cls.header_struct = struct.Struct(''.join([field.format for field in cls.header_fields_structure.values()]))
        cls.data_struct = struct.Struct(''.join([field.format for field in cls.data_fields_structure.values()]))

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
                f'Expected header {self.expected_header} for data file , but got {header} instead.'
            )

        self.data_dicts = []

        for data_tuple in self.data_struct.iter_unpack(self.data_stream.read()):
            data = OrderedDict(zip(self.data_fields_structure.keys(), data_tuple))
            data['name'] = self.get_name(data['identifier_part_1'])
            self.data_dicts.append(data)

    def get_name(self, name_id):
        #https://stackoverflow.com/questions/23263599/how-to-extract-128x128-icon-bitmap-data-from-exe-in-python
        #https://github.com/team5499/pie-2015/blob/master/VrepRobotCPortable/Python/App2/Lib/site-packages/py2exe
        #/resources/StringTables.py
        # general name -> print(c['name'], ' -> ', manager.get_name(c['identifier_part_1'] + 28672))
        # commander name ->  print(c['name'], ' -> ',  manager.get_name(c['identifier_part_1'] + 26624))
        # admiral name -> print(c['name'], ' -> ', manager.get_name(c['identifier_part_1'] + 27648))
        textstra_lib = win32api.LoadLibrary(os.path.join(self.data_path, "TEXTSTRA.DLL"))
        return win32api.LoadString(textstra_lib, name_id)


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
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier, always 0
        ("detection", FieldDef('I', FieldType.EDITABLE)),
        ("shield", FieldDef('I', FieldType.EDITABLE)),
        ("sublight", FieldDef('I', FieldType.EDITABLE)),
        ("maneuverability", FieldDef('I', FieldType.EDITABLE)),
        ("hyperdrive", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_4", FieldDef('I', FieldType.UNKNOWN)),  # backup hyperdrive, always 0
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
        ("unknown_2", FieldDef('I', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier, basicly 0.45 * construction_cost
        ("detection", FieldDef('I', FieldType.EDITABLE)),
        ("shield", FieldDef('I', FieldType.EDITABLE)),
        ("sublight", FieldDef('I', FieldType.EDITABLE)),
        ("maneuverability", FieldDef('I', FieldType.EDITABLE)),
        ("hyperdrive", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_4", FieldDef('I', FieldType.UNKNOWN)),  # backup hyperdrive, always 0
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
        ("bombardment", FieldDef('I', FieldType.EDITABLE)),
        ("tractor_beam_range", FieldDef('I', FieldType.EDITABLE)),
        ("gravity_well_1", FieldDef('H', FieldType.EDITABLE)),  # 4 if present
        ("gravity_well_2", FieldDef('H', FieldType.EDITABLE)),  # 100 if present
        ("tractor_beam_power", FieldDef('I', FieldType.EDITABLE)),
        ("damage_control", FieldDef('I', FieldType.EDITABLE)),
        ("weapon_recharge", FieldDef('I', FieldType.EDITABLE)),
        ("shield_recharge", FieldDef('I', FieldType.EDITABLE)),
        ("fighter_squadrons", FieldDef('I', FieldType.EDITABLE)),
        ("troop_contingents", FieldDef('I', FieldType.EDITABLE)),
        ("unknown_5", FieldDef('I', FieldType.READ_ONLY)),  # Always 0
        ("defense", FieldDef('I', FieldType.EDITABLE))
    ])


class SectorsDataManager(SWRDataManager):
    filename = "SECTORSD.DAT"

    expected_header = (1, 20, 128, 144)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 100
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),  # usually 146
        ("identifier_part_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
        ("importance", FieldDef('I', FieldType.UNKNOWN)),  # 1-high 2-medium 3-low
        ("game_size", FieldDef('I', FieldType.UNKNOWN)),  # 1-Small 2-Medium 3-Large
        ("position_x", FieldDef('H', FieldType.EDITABLE)),
        ("position_y", FieldDef('H', FieldType.EDITABLE)),
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
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier
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
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier
        ("manufacturing_rate", FieldDef('I', FieldType.EDITABLE)),  # required days to manufacture 1 unit
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
        ("unknown_3", FieldDef('I', FieldType.UNKNOWN)),  # maybe moral modifier
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


ALL_MANAGERS = [
    SectorsDataManager,
    SystemsDataManager,
    ManufacturingFacilitiesDataManager,
    ProductionFacilitiesDataManager,
    DefensiveFacilitiesDataManager,
    TroopsDataManager,
    FightersDataManager,
    CapitalShipsDataManager,
    MajorCharacterDataManager,
    MinorCharacterDataManager
]
