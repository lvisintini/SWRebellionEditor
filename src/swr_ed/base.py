from abc import ABC, abstractmethod
import hashlib
import os
import logging
import struct
from collections import OrderedDict
from functools import cached_property
from io import BytesIO

from . import ALL_MANAGERS, MANAGERS_BY_FILE
from .exceptions import SWRebellionEditorDataFileHeaderMismatchError
from .constants import FieldType
from .dll_wrappers import TextStraWrapper

log = logging.getLogger(__name__)


class FieldDef:
    def __init__(self, struct_format, field_type, help_text=None):
        self.format = struct_format
        self.type = field_type
        self.help_text = help_text


class SWRBaseManager(ABC):
    """
    This class contains the basic facilities to load a GDATA file and parse its contents.
    It assumes that all files would have a header structure, though what that structure is would be up to subclasses

    """
    filename = None
    file_location = 'GDATA'
    header_struct_format = None
    expected_header = None
    expected_md5_checksum = None
    byte_order = '<'  # we assume little-endian https://docs.python.org/3/library/struct.html#struct-alignment

    @property
    @abstractmethod
    def data_struct(self) -> struct.Struct:
        raise NotImplementedError

    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.file_path = os.path.join(self.data_path, self.file_location, self.filename)
        self.header_struct = struct.Struct(self.byte_order + self.header_struct_format)
        self.header_count = None
        self.data = None
        self.md5_checksum = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.filename:
            ALL_MANAGERS.append(cls)
            ALL_MANAGERS.sort(key=lambda m: m.filename)
            MANAGERS_BY_FILE[cls.filename] = cls

    def load_stream_from_file(self):
        file_stream = BytesIO()
        with open(self.file_path, "rb") as file_obj:
            file_stream.write(file_obj.read())
        file_stream.seek(0)
        self.md5_checksum = hashlib.md5(file_stream.read()).hexdigest()
        file_stream.seek(0)
        return file_stream

    def load(self):
        header_stream = BytesIO()
        data_stream = BytesIO()

        file_stream = self.load_stream_from_file()

        loaded_md5_checksum = hashlib.md5(file_stream.read()).hexdigest()
        file_stream.seek(0)

        header_stream.write(file_stream.read(self.header_struct.size))
        data_stream.write(file_stream.read())
        header_stream.seek(0)
        data_stream.seek(0)

        header = self.header_struct.unpack(header_stream.read())

        if loaded_md5_checksum != self.expected_md5_checksum:
            if header != self.expected_header:
                raise SWRebellionEditorDataFileHeaderMismatchError(
                    f'Manager {self.__class__.__name__} expected header '
                    f'{self.expected_header} for data file , but got {header} instead.'
                )
        else:
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
            data = self.upgrade_data(data_tuple)
            self.data.append(data)

    def prepare_output_stream(self):
        stream = BytesIO()
        new_header = [self.expected_header[0], self.get_count()] + list(self.expected_header[2:])

        stream.write(self.header_struct.pack(*new_header))

        for entry in self.data:
            data_tuple = self.downgrade_data(entry)
            stream.write(self.data_struct.pack(*data_tuple))

        stream.seek(0)
        return stream

    def save(self):
        stream = self.prepare_output_stream()
        self.save_stream_to_file(stream)

    def save_stream_to_file(self, stream):
        stream.seek(0)
        with open(self.file_path, "wb") as file_obj:
            file_obj.write(stream.read())
        stream.seek(0)
        self.md5_checksum = hashlib.md5(stream.read()).hexdigest()

    def get_count(self):
        return len(self.data)

    def upgrade_data(self, data_tuple):
        """
        A method to enhance each data row after it has been unpacked from the file.
        By default, it turns each data row into a list that is easy to manipulate.
        This method is later overridden by subclasses that turn the output of the files
        into dicts that are still far more useful
        """
        return list(data_tuple)

    def downgrade_data(self, data):
        """
        This method should do the reverse of the upgrade data method.
        It is meant to simplify data in order for it to be stored into the relevant files again.
        """
        return data


class SimpleSWRManager(SWRBaseManager):
    data_struct_format = None
    data_struct = None

    def __init__(self, data_path=None):
        super().__init__(data_path=data_path)
        self.data_struct = struct.Struct(self.byte_order + self.data_struct_format)


class FieldsMeta(type):
    def __new__(mcs, classname, bases, namespace):
        fields = OrderedDict()
        for attr in list(namespace.keys()):
            if isinstance(namespace[attr], FieldDef):
                field = namespace.pop(attr)
                fields[attr] = field

        if fields:
            namespace['fields'] = fields

        cls = type.__new__(mcs, classname, bases, namespace)

        return cls


class SWRBaseFieldManagerIntermediateMeta(type(SWRBaseManager), FieldsMeta):
    pass


class SWRDataManager(SWRBaseManager, metaclass=SWRBaseFieldManagerIntermediateMeta):
    # The data in the headers appears to support that:
    # - The second number is the row count in the file
    # - The third number is the lowest family_id value in the file
    header_struct_format = "IIII"

    fields = None

    @cached_property
    def data_struct(self):
        return struct.Struct(
            self.byte_order + ''.join([field.format for field in self.fields.values()])
        )

    def __init__(self, data_path=None):
        super().__init__(data_path=data_path)

        self.header_struct = struct.Struct(
            self.byte_order + self.header_struct_format
        )
        self.text_stra = TextStraWrapper(self.data_path)

    def upgrade_data(self, data_tuple):
        data_dict = OrderedDict(zip(list(self.fields.keys()), data_tuple))
        if 'name_id_1' in data_dict:
            data_dict.update(self.get_texts(name=data_dict['name_id_1']))
        return data_dict

    def downgrade_data(self, data):
        return (data[attr] for attr in list(self.fields.keys()))

    def get_texts(self, **kwargs):
        res = {}
        for attr, text_id in kwargs.items():
            res[attr] = self.get_text(text_id)
        return res

    def get_text(self, text_id):
        return self.text_stra.get_text(text_id)


class TableDataManager(SWRDataManager):
    header_struct_format = "III13s"


class ProbabilityTableManager(TableDataManager):
    index = FieldDef('I', FieldType.READ_ONLY)
    one = FieldDef('I', FieldType.READ_ONLY)
    score = FieldDef('i', FieldType.READ_ONLY)
    probability = FieldDef('I', FieldType.READ_ONLY)


class SimpleTableDataManager(SimpleSWRManager):
    header_struct_format = "III13s"
    data_struct_format = 'IIiI'


class GroupedTableManager(SimpleSWRManager):
    header_struct_format = "III20s"
    data_struct_format = 'IIHBB'

    def get_count(self):
        return max([entry[0] for entry in self.data])
