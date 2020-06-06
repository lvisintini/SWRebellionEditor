import struct
import os
from io import BytesIO
from collections import namedtuple, OrderedDict

from .exceptions import SWRebellionEditorDataFileHeaderMismatchError
from .constants import FieldType


FieldDef = namedtuple('StrucFormatDef', ['format', 'type'])


class SWRDataManager:
    filename = None
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
        ("number", FieldDef('i', FieldType.READ_ONLY)),  # always 1
        ("count", FieldDef('i', FieldType.DENORMALIZED)),   # number of elements in file
        ("family", FieldDef('i', FieldType.READ_ONLY)),  # family id
        ("unknown", FieldDef('i', FieldType.DENORMALIZED)),  # the "higher" (not consisted) family identifier
    ])

    data_fields_structure = None

    def __init__(self, data_path):
        self.data_path = data_path
        self.file_path = os.path.join(data_path, self.filename)
        self.header_stream = BytesIO()
        self.data_stream = BytesIO()
        self.data_dicts = None

    def __init_subclass__(cls):
        super().__init_subclass__()

        cls.header_struct = struct.Struct(''.join([field.format for field in cls.header_fields_structure.values()]))
        cls.data_struct = struct.Struct(''.join([field.format for field in cls.data_fields_structure.values()]))

    def load_file(self):
        with open(self.file_path, "rb") as data_file:
            self.header_stream.write(data_file.read(self.header_struct.size))
            self.data_stream.write(data_file.read())

        self.header_stream.seek(0)
        self.data_stream.seek(0)

        header = self.header_struct.unpack(self.header_stream.read())

        self.header_stream.seek(0)

        if header != self.expected_header:
            raise SWRebellionEditorDataFileHeaderMismatchError(
                'Expected header %s for data file %s, but got %s instead.'
            )

        self.data_dicts = []

        for data_tuple in self.data_struct.iter_unpack(self.data_stream.read()):
            self.data_dicts.append(
                dict(zip(self.data_fields_structure.keys(), data_tuple))
            )


class FightersDataManager(SWRDataManager):
    filename = "FIGHTSD.DAT"

    expected_header = (1, 8, 28, 32)

    data_fields_structure = OrderedDict([
        ("number", FieldDef('i', FieldType.READ_ONLY)),
        ("unknown_1", FieldDef('i', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('i', FieldType.READ_ONLY)),  # always 40
        ("producing_facility_family_id_one_based", FieldDef('i', FieldType.READ_ONLY)),  # always 41
        ("family_id", FieldDef('i', FieldType.READ_ONLY)),  # always 28
        ("identifier_part_1", FieldDef('h', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("identifier_part_2", FieldDef('h', FieldType.READ_ONLY)),  # always 2
        ("alliance", FieldDef('i', FieldType.READ_ONLY)),
        ("imperial", FieldDef('i', FieldType.READ_ONLY)),
        ("construction_cost", FieldDef('i', FieldType.EDITABLE)),
        ("maintenance", FieldDef('i', FieldType.EDITABLE)),
        ("research_order", FieldDef('i', FieldType.EDITABLE)),
        ("unknown_2", FieldDef('i', FieldType.UNKNOWN)),  # maybe research difficulty
        ("unknown_3", FieldDef('i', FieldType.UNKNOWN)),  # maybe moral modifier, always 0
        ("detection", FieldDef('i', FieldType.EDITABLE)),
        ("shield", FieldDef('i', FieldType.EDITABLE)),
        ("sublight", FieldDef('i', FieldType.EDITABLE)),
        ("maneuverability", FieldDef('i', FieldType.EDITABLE)),
        ("hyperdrive", FieldDef('i', FieldType.EDITABLE)),
        ("unknown_4", FieldDef('i', FieldType.UNKNOWN)),  # backup hyperdrive, always 0
        ("turbolaser_firepower_front", FieldDef('i', FieldType.EDITABLE)),
        ("ion_firepower_front", FieldDef('i', FieldType.EDITABLE)),
        ("laser_firepower_front", FieldDef('i', FieldType.EDITABLE)),
        ("turbolaser_firepower_rear", FieldDef('i', FieldType.EDITABLE)),
        ("ion_firepower_rear", FieldDef('i', FieldType.EDITABLE)),
        ("laser_firepower_rear", FieldDef('i', FieldType.EDITABLE)),
        ("turbolaser_firepower_left", FieldDef('i', FieldType.EDITABLE)),
        ("ion_firepower_left", FieldDef('i', FieldType.EDITABLE)),
        ("laser_firepower_left", FieldDef('i', FieldType.EDITABLE)),
        ("turbolaser_firepower_right", FieldDef('i', FieldType.EDITABLE)),
        ("ion_firepower_right", FieldDef('i', FieldType.EDITABLE)),
        ("laser_firepower_right", FieldDef('i', FieldType.EDITABLE)),
        ("turbolasers_range", FieldDef('i', FieldType.EDITABLE)),
        ("ion_range", FieldDef('i', FieldType.EDITABLE)),
        ("laser_range", FieldDef('i', FieldType.EDITABLE)),
        ("turbolaser_firepower_sum", FieldDef('i', FieldType.DENORMALIZED)),
        ("ion_firepower_sum", FieldDef('i', FieldType.DENORMALIZED)),
        ("laser_firepower_sum", FieldDef('i', FieldType.DENORMALIZED)),
        ("firepower_sum", FieldDef('i', FieldType.DENORMALIZED)),
        ("torpedo_power", FieldDef('i', FieldType.EDITABLE)),
        ("torpedo_range", FieldDef('i', FieldType.EDITABLE)),
        ("squadron_size", FieldDef('i', FieldType.READ_ONLY)),  # always 12
        ("bombardment", FieldDef('i', FieldType.EDITABLE)),
    ])

