import hashlib
import os
import logging
import struct
from collections import namedtuple, OrderedDict
from io import BytesIO

from . import ALL_MANAGERS, MANAGERS_BY_FILE
from .exceptions import SWRebellionEditorDataFileHeaderMismatchError
from .constants import FieldType

FieldDef = namedtuple('StrucFormatDef', ['format', 'type'])

log = logging.getLogger(__name__)


class SWRBaseManager:
    """
    This class contains the basic facilities to load a GDATA file and parse its contents.
    It assumes that all files would have a header structure, though what that structure is would be up to subclasses

    """
    filename = None
    file_location = 'GDATA'
    header_struct_format = None
    expected_header = None
    md5_checksum = None
    byte_order = '<'  # we assume little-endian https://docs.python.org/3/library/struct.html#struct-alignment

    def __init__(self, data_path=None):
        self.data_path = data_path or os.getenv('SW_REBELLION_DIR')
        self.file_path = os.path.join(self.data_path, self.file_location, self.filename)
        self.header_struct = struct.Struct(self.byte_order + self.header_struct_format)
        self.header_count = None
        self.data_struct = None
        self.data = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.filename:
            ALL_MANAGERS.append(cls)
            ALL_MANAGERS.sort(key=lambda m: m.filename)
            MANAGERS_BY_FILE[cls.filename] = cls

    def load_file(self):
        header_stream = BytesIO()
        data_stream = BytesIO()
        file_stream = BytesIO()

        with open(self.file_path, "rb") as file_obj:
            file_stream.write(file_obj.read())

        file_stream.seek(0)
        md5_checksum = hashlib.md5(file_stream.read()).hexdigest()

        file_stream.seek(0)
        header_stream.write(file_stream.read(self.header_struct.size))
        data_stream.write(file_stream.read())
        header_stream.seek(0)
        data_stream.seek(0)

        header = self.header_struct.unpack(header_stream.read())

        if md5_checksum != self.md5_checksum:
            log.warning("%s appears to have been previously modified", self.file_path)

            if header != self.expected_header:
                raise SWRebellionEditorDataFileHeaderMismatchError(
                    f'Manager {self.__class__.__name__} expected header '
                    f'{self.expected_header} for data file , but got {header} instead.'
                )
        else:
            log.info('all is good')
            # if the checksums for the original files do not match, then ignore the second value.
            # Invariably, that value is an integer that corresponds with the number items/groups in the file

            expected = [v if i != 1 else 'XXX' for i, v in enumerate(self.expected_header)]
            actual = [v if i != 1 else 'XXX' for i, v in enumerate(header)]

            if header != self.expected_header:
                raise SWRebellionEditorDataFileHeaderMismatchError(
                    f'Manager {self.__class__.__name__} expected header '
                    f'{expected} for data file , but got {actual} instead.'
                )

        self.header_count = header[1]

        self.data = []
        for data_tuple in self.data_struct.iter_unpack(data_stream.read()):
            data = self.process_data_tuple(data_tuple)
            self.data.append(data)

    def process_data_tuple(self, data_tuple):
        return data_tuple


class SimpleSWRManager(SWRBaseManager):
    data_struct_format = None

    def __init__(self, data_path=None):
        super().__init__(data_path=data_path)
        self.data_struct = struct.Struct(self.byte_order + self.data_struct_format)


class SWRDataManager(SWRBaseManager):

    # The data in the headers appears to support that:
    # - The second number is the row count in the file
    # - The third number is the lowest family_id value in the file
    header_struct_format = "IIII"

    data_fields_structure = None

    def __init__(self, data_path=None, fetch_names=False):
        super().__init__(data_path=data_path)
        self.fetch_names = fetch_names

        self.field_names = list(self.data_fields_structure.keys())

        self.header_struct = struct.Struct(
            self.byte_order + self.header_struct_format
        )
        self.data_struct = struct.Struct(
            self.byte_order + ''.join([field.format for field in self.data_fields_structure.values()])
        )

    def process_data_tuple(self, data_tuple):
        data_dict = OrderedDict(zip(self.field_names, data_tuple))
        if 'name_id_1' in data_dict and self.fetch_names:
            data_dict.update(self.get_texts(name=data_dict['name_id_1']))
        return data_dict

    def get_texts(self, **kwargs):
        res = {}
        for attr, text_id in kwargs.items():
            res[attr] = self.get_text(text_id)
        return res

    def get_text(self, text_id):
        #https://stackoverflow.com/questions/23263599/how-to-extract-128x128-icon-bitmap-data-from-exe-in-python
        #https://github.com/team5499/pie-2015/blob/master/VrepRobotCPortable/Python/App2/Lib/site-packages/py2exe
        #/resources/StringTables.py
        try:
            import win32api
            import pywintypes
        except ModuleNotFoundError:
            return None
        try:
            textstra_lib = win32api.LoadLibrary(os.path.join(self.data_path, "TEXTSTRA.DLL"))
            return win32api.LoadString(textstra_lib, text_id)
        except pywintypes.error:
            return None


class CharacterBaseDataDataManager(SWRDataManager):
    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),  # starting from 576
        ("active", FieldDef('I', FieldType.UNKNOWN)),  # maybe the active flag, always 1
        ("producing_facility_family_id", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        ("producing_facility_family_id_one_based", FieldDef('I', FieldType.READ_ONLY)),  # always 0
        # 48 for Mon Mothma, 49 for Leia Organa, 50 for Luke Skywalker, 51 for Han Solo, 52 for Emperor Palpatine,
        # 52 for Darth Vader  and 56 for Minor characters
        ("family_id", FieldDef('I', FieldType.READ_ONLY)),
        ("name_id_1", FieldDef('H', FieldType.READ_ONLY)),  # can be used get the name from Textstrat.dll
        ("name_id_2", FieldDef('H', FieldType.READ_ONLY)),  # always 2
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

    def process_data_tuple(self, data_tuple):
        data_dict = OrderedDict(zip(self.field_names, data_tuple))
        data_dict.update(
            self.get_texts(
                name=data_dict['name_id_1'],
                name_general=data_dict['name_id_1'] + 28672,
                name_commander=data_dict['name_id_1'] + 26624,
                name_admiral=data_dict['name_id_1'] + 27648,
            )
        )
        return data_dict


class SystemFacilityTableDataDataManager(SWRDataManager):
    header_struct_format = "III14s"

    data_fields_structure = OrderedDict([
        ("number", FieldDef('I', FieldType.READ_ONLY)),
        ("number2", FieldDef('I', FieldType.READ_ONLY)),  # always 1
        ("percent", FieldDef('I', FieldType.READ_ONLY)),
        ("level", FieldDef('H', FieldType.READ_ONLY)),
        ("unknown", FieldDef('B', FieldType.READ_ONLY)),  # always 0
        ("family_id", FieldDef('B', FieldType.READ_ONLY)),
    ])


class TableDataBaseDataManager(SWRDataManager):
    header_struct_format = "III13s"


class ProbabilityTableDataBaseManager(TableDataBaseDataManager):
    data_fields_structure = OrderedDict([
        ("index", FieldDef('I', FieldType.READ_ONLY)),
        ("one", FieldDef('I', FieldType.READ_ONLY)),
        ("score", FieldDef('i', FieldType.READ_ONLY)),
        ("probability", FieldDef('I', FieldType.READ_ONLY)),
    ])


class SimpleTableDataManager(SimpleSWRManager):
    header_struct_format = "III13s"
    data_struct_format = 'IIiI'


class GroupedTableBaseDataManager(SimpleSWRManager):
    header_struct_format = "III20s"
    data_struct_format = 'IIHBB'
