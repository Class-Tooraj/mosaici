from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

# IMPORT
import os

# IMPORT TYPING
from typing import Iterable, Generator, NamedTuple

# IMPORT LOCAL
from mosaici.exceptions import *

from mosaici.order import Order, BaseOrder
from mosaici.block import Block, BaseBlock
from mosaici.pattern import Convertor, Wrapped
from mosaici.template import BaseTemplate, BaseFileTemplate, Template, FileTemplate, T_ITER
from mosaici.store import BaseStoreIndexes, StoreFileIndexes, StoreObjectIndexes
from mosaici.indexpack import BaseIndexes, FilePathIndexes
from mosaici.protocol import ModeName

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# MOSAIC ABSTRACT
class BaseMosaic:
    """
    Base Mosaic Module
    """
    # Use For Making New Template See 'make_template()' Static Method
    TEMPLATE: BaseTemplate
    # Active Making Template If Needed - If template arguments in Constructor is None
    ACTIVE_MAKER: bool
    # Load Template Needed FILE_TEMPLATE
    FILE_TEMPLATE: BaseFileTemplate
    # Store For Mosaic Pattern
    STORE_INDEXES: BaseStoreIndexes

    def __init__(
        self,
        template: BaseTemplate = None,
        order: BaseOrder | str = None,
        default_block: BaseBlock | T_ITER = None,
        ) -> None:
        """
        Initialize Mosaic
        const:
            TEMPLATE [BaseTemplate]: [Template instance of BaseTemplate].
            ACTIVE_MAKER [bool]: [`True` if template is `None` Create Template, `False` Do Nothing].
            FILE_TEMPLATE [BaseFileTemplate]: [Use For Loading Template].

        args:
            template [BaseTemplate]: [Created Template Use This Template For Converting] default is `None`.
                ** `None` Means Make Template with `make_template()` Static Method if ACTIVE_MAKER is `True`.
            order [BaseOrder | str]: [Order For Making Template See 'Template' Module] default is `None`.
                ** `None` Means Without Order See 'Template' Module.
            default_block [BaseBlock | T_ITER]: [Default Block For Generating Template] default is `None`.
                ** `None` Means Default Block See 'Block' Module.

        ** NOTE: If Use `load_template` Method without `with` Statement Must Be Close `FileTemplate` After Don Working with `close` Method.
            -- Can Check is Open or Closed With `closed` Method. `load_template` Method Create `close, closed` Method.
        ** `with` Statement Supported in This Module And Recomented For Use.
        ** `with` Statement Automatic Closing if Template is FileTemplate.
        ** Recommended Use `with` Statement.
        """

        if not self.TEMPLATE or not self.FILE_TEMPLATE or not self.STORE_INDEXES:
            raise NotImplementedError

        if template is not None:
            # Attached Template
            self._template = template

        elif template is None and self.ACTIVE_MAKER:
            # Making Template
            self._template = self.make_template(self.TEMPLATE, order=order, default_block=default_block)

        else:
            # Template is Not Active
            self._template = None

    @property
    def template(self) -> BaseTemplate:
        """
        Property Template -
        return:
            [BaseTemplate]: [Active Template]
        """
        return self._template

    @template.setter
    def template(self, template: BaseTemplate) -> None:
        """
        Property Setter Template
        Change Active Template
        """
        # Fix File Template Closing Before Removed
        # See - template.deleter
        if self._template is not None:
            del self.template

        self._template = template

    @template.deleter
    def template(self) -> None:
        """
        Property Deleter Template
        """
        if hasattr(self, 'close'):
            self.close()
            delattr(self, 'close')
            delattr(self, 'closed')

        self._template = None

    def index(self, block: int, value: int | bytes | str, order: str | Wrapped = Wrapped.INT) -> int | str:
        """
        Index From Template
        args:
            block [int]: [Block For Get Index of Value].
            value [int | bytes | str]: [Value Placed Index From Block].
            order [str | Wrapped]: [Order For Index Type] default is `Wrapped.INT` == 'int'.
                ** Support [Wrapped.INT, Wrapped.BIN, Wrapped.HEX, Wrapped.OCT] or by Name ['int', 'bin', 'hex', 'oct']
                ** More Info See `convertor()` Static Method.

        return:
            [int | str]: [Value Placed In Index Of Block]
        """
        if isinstance(value, int):
            return self.convertor(self._template.index(block, value), order)

        return self.convertor(self._template.index(block, self.convertor(value, Wrapped.INT)), order)

    def value(self, block: int, index: int | bytes | str) -> bytes:
        """
        Value From Template
        args:
            block [int]: [Block For Get Value from Index].
            index [int | bytes | str]: [Index Of Block For Get Value].

        return:
            [bytes]: [Value Placed In Index Of Block]
        """
        if isinstance(index, int):
            return self._template.value(block, index)

        return self._template.value(block, self.convertor(index, Wrapped.INT))

    def data_to_idx(self, data: bytes | Iterable[bytes], start_block: int = 0) -> Generator[int, None, None]:
        """
        Data To Indexes
        args:
            data [bytes | Iterable[bytes]]: [Bytes Data Target For Converting To Template Indexes]
            start_block [int]: [Start Block] default is `0`.

        return:
            [Generator[int, None, None]]: [Generator Yield Indexes].
        """
        for block, value in enumerate(data, start_block):
            yield self._template.index(block, value)

    def to_mosaici(self, data: bytes | Iterable[bytes], start_block: int = 0) -> BaseStoreIndexes:
        """
        To Mosaic - Same as `data_to_idx` Method but Return BaseStoreIndexes
        args:
            data [bytes | Iterable[bytes]]: [Bytes Data Target For Converting To Template Indexes]
            start_block [int]: [Start Block] default is `0`.

        return:
            [BaseStoreIndexes]: [Instance Of BaseStoreIndexes].
            ** More info See `StoreIndexes` Module.
        """
        return self.STORE_INDEXES(self.data_to_idx(data, start_block))

    def idx_to_data(self, indexes: BaseIndexes, start_block: int = 0) -> Generator[bytes, None, None]:
        """
        Indexes To Data
        args:
            indexes [BaseIndexes]: [Indexes Target For Converting To Data]
            start_block [int]: [Start Block] default is `0`.

        return:
            [Generator[bytes, None, None]]: [Generator Yield Value Bytes].
        """
        for block, value in enumerate(indexes, start_block):
            yield self._template.value(block, value)

    def to_data(self, indexes: BaseIndexes, start_block: int = 0) -> Iterable[bytes]:
        """
        To Data  - Same as `idx_to_data` Method But Return Iterable[bytes]
        args:
            indexes [BaseIndexes]: [Indexes Target For Converting To Data]
            start_block [int]: [Start Block] default is `0`.

        return:
            [Generator[bytes, None, None]]: [Iterable Of Bytes].
        """
        return (i for i in self.idx_to_data(indexes, start_block))

    def save_template(self, path: str) -> NamedTuple[int, int, int]:
        """
        Save Template - More Info See 'Template.save_template' Method.
        args:
            path [str]: [Path File For Save Template].

        return:
            [NamedTuple[int, int, int]]: [Save Template Info (write, block, member)].
            ** More Info See from `Template` Module `save_template` Method.
        """
        return self._template.save_template(path)

    def load_template(self, path: str, member: int) -> None:
        """
        Load Template
        Load Saved Template & Set To Active Template.
        When This Method Calls Created 'close' Method For Closing and 'closed' Method For Check Closed FileTemplate Or Open.
        NOTE: Do not Forget Closing Template if Do not Want Use `with` Statement.
        ** If Use `with` Statement FileTemplate Automatic Closed After Done Working.
        ** More Info See `FileTemplate` Module.
        args:
            path [str]: [Path Of Saved Template].
            member [int]: [Block Member Size].
        """
        # Fix Closing Template if File Template
        # See - 'template.deleter'
        if self._template is not None:
            del self.template

        self._template = self.FILE_TEMPLATE(path, member)
        self.close = self._template.close
        self.closed = lambda: self._file.closed

    def __enter__(self) -> object:
        return self

    def __exit__(self, *_) -> None:
        try:
            pass
        finally:
            # Check If Loaded Template - Closing Template File
            if hasattr(self, 'close'):
                self.close()
            del self._template
            del self

    @staticmethod
    def convertor(value: int | bytes | str, order: str | Wrapped) -> int | str:
        """
        Converting Value To Order `Static Method` - More Info See `Convertor` Module
        args:
            value [int | bytes | str]: [Value For Converting To Order].
            order [str | Wrapped]: [Order For Converting].
                ** Support (`int`, `bin`, `hex`, `oct`) by Name
                ** [Wrapped.INT, Wrapped.BIN, Wrapped.HEX, Wrapped.OCT]. `more info See Wrapped Module`

        return:
            [int | str]: [Standard Mosaici Value By Order].

        ** Example:
            convertor(1, 'bin')     -> '00000001' [str]
            convertor(1, 'hex')     -> '01'       [str]
            convertor(1, 'oct')     -> '001'      [str]
            convertor('001', 'int') -> 1          [str]

            convertor('01', Wrapped.BIN)     -> '00000001' [str]

        ** NOTE: Value Support type int or bytes or str String Must `Standard 'bin', 'hex', 'oct'`
        """
        if isinstance(order, str):
            order = Wrapped.by_name(order)

        if isinstance(value, int):
            return Convertor.int_to_order(value, order)
        elif isinstance(value, str):
            value = Convertor.std_int(value)
        elif isinstance(value, bytes):
            value = int.from_bytes(value, 'little')

        return Convertor.int_to_order(value, order)

    @staticmethod
    def make_template(
        template_obj: BaseTemplate,
        blocks: tuple[BaseBlock, ...] = None,
        order: BaseOrder | str = None,
        default_block: BaseBlock | T_ITER = None,
        ) -> BaseTemplate:
        """
        Make Template - Static Method
        ** More Info See `Template` Module
        args:
            template_obj [BaseTemplate]: [Template Object For Creating Template].
            blocks [tuple[BaseBlock]]: [Blocks] default is `None`.
            order [BaseOrder | str]: [Order] default is `None`.
            default_block [BaseBlock | T_ITER]: [Default Block] default is `None`.

        return:
            [BaseTemplate]: [Created Template].
        """
        return template_obj(blocks=blocks, order=order, default_block=default_block)


# MOSAIC LOAD TEMPLATE ABSTRACT
class BaseMosaicFileTemplate(BaseMosaic):
    """
    Base Mosaic Module
    """

    TEMPLATE: BaseTemplate
    ACTIVE_MAKER: bool
    FILE_TEMPLATE: BaseFileTemplate
    STORE_INDEXES: BaseStoreIndexes

    def __init__(
        self,
        file_template: tuple[str | os.PathLike, int] = None,
        template: Template = None,
        order: Order | str = None,
        default_block: Block | T_ITER = None,
        active_maker: bool = True
        ) -> None:
        """
        Initialize MosaicFile - Instance of `BaseMosaic`
        const:
            TEMPLATE [BaseTemplate]: [Template instance of BaseTemplate].
            ACTIVE_MAKER [bool]: [`True` if template is `None` Create Template, `False` Do Nothing].
            FILE_TEMPLATE [BaseFileTemplate]: [Use For Loading Template].

        args:
            file_template [tuple[str | PathLike, int]]: [Load Template File] default is `None`.
                ** For Use Need Tuple Of Path And Member Count -> (templatefilepath.tt, 256).
            template [BaseTemplate]: [Created Template Use This Template For Converting] default is `None`.
                ** `None` Means Make Template with `make_template()` Static Method if ACTIVE_MAKER is `True`.
            order [BaseOrder | str]: [Order For Making Template See 'Template' Module] default is `None`.
                ** `None` Means Without Order See 'Template' Module.
            default_block [BaseBlock | T_ITER]: [Default Block For Generating Template] default is `None`.
                ** `None` Means Default Block See 'Block' Module.
            active_maker [bool]: [if True And template or file_template is `None` Generate Template] default is `True`.

        ** NOTE: If Use `load_template` Method without `with` Statement Must Be Close `FileTemplate` After Don Working with `close` Method.
            -- Can Check is Open or Closed With `closed` Method. `load_template` Method Create `close, closed` Method.
        ** `with` Statement Supported in This Module And Recomented For Use.
        ** `with` Statement Automatic Closing if Template is FileTemplate.
        ** Recommended Use `with` Statement.
        """
        if not self.TEMPLATE or not self.FILE_TEMPLATE or not self.STORE_INDEXES:
            raise NotImplementedError

        if file_template is None:
            self.ACTIVE_MAKER = active_maker
            super(BaseMosaicFileTemplate, self).__init__(template, order, default_block)

        else:
            self.ACTIVE_MAKER = False
            super(BaseMosaicFileTemplate, self).__init__(None, None, None)
            self.load_template(*file_template)
            self.ACTIVE_MAKER = active_maker


# STANDARD MOSAIC FILE
class MosaicFile(BaseMosaicFileTemplate):
    """
    MosaicFile - Instance of BaseMosaicFileTemplate
    This Module Customized For Working Better With File
    """
    TEMPLATE: Template = Template
    ACTIVE_MAKER: bool = None
    FILE_TEMPLATE: FileTemplate = FileTemplate
    STORE_INDEXES: StoreFileIndexes = StoreFileIndexes
    FILE_INDEXES: FilePathIndexes = FilePathIndexes

    def to_mosaici(
        self,
        path: str | os.PathLike,
        idx_path: str | os.PathLike,
        start_block: int = 0,
        idx_mode: str = 'wb',
        write_protocol: bool = True
        ) -> NamedTuple[int, str | os.PathLike, str]:
        """
        File To Mosaici
        Customize `to_mosaici` Method For FileMosaic Module - Overwrite [`to_mosaici` parrent method]
        args:
            path [str | PathLike]: [Target File Path For Convert To Indexes File].
            idx_path [str | PathLike]: [Target Indexes File Path For Saving Indexes].
            start_block [int]: [Relative Start Block For Converting To Indexes] default is `0`.
            idx_mode [str]: [Indexes File Mode 'wb' is Binarray Mode `w` is Text Mode] default is `wb`.
                ** NOTE: idx_mode Must Can Write To File.
                ** More Info See `ModeName` & `Protocol` & `StoreFileIndexes` Module.
            write_protocol [bool]: [Write Indexes File With Protocol] default is `True`.
                ** `False` Means Write raw - Default StoreIndexes Support Only StandardProtocol.

        return:
            [NamedTuple[int, str | os.PathLike, str]]: [Write Info].
                ** 'WriteMosaicInfo('write': int, 'path': int, 'type': str)'
                ** More Info See `write_info` Static Method.
        """
        # Check Can Write
        _can_write = self.mode_name(idx_mode).can_write

        if not _can_write:
            raise FileIsNotWritableError

        # To Real Path With `realpaths` Static Method
        path, idx_path = self.realpaths(path, idx_path)

        # Open File & Index Out File
        with open(path, "rb") as f, open(idx_path, idx_mode) as of:
            # Iterable Read
            data =  (i for i in f.read())
            # Check Write Protocol
            if write_protocol:
                # Write With Protocol
                writes = super(MosaicFile, self).to_mosaici(data, start_block).write(of)
            else:
                # Write Witout Protocol
                writes = super(MosaicFile, self).to_mosaici(data, start_block).write_raw(of)

        return self.write_info(writes, idx_path, 1)

    def to_data(
        self,
        idx_path: str | os.PathLike,
        path: str | os.PathLike,
        start_block: int = 0,
        idx_mode: str = 'rb'
        ) -> NamedTuple[int, str | os.PathLike]:
        """
        Mosaici `Indexes` File To Data
        Customize `to_data` Method For FileMosaic Module - Overwrite [`to_data` parrent method]
        NOTE : Only Protocol Writes File Support
        args:
            idx_path [str | PathLike]: [Target Indexes File Path For Converting To Data].
            path [str | PathLike]: [Target Result File Path].
            start_block [int]: [Relative Start Block For Converting To Indexes] default is `0`.
            idx_mode [str]: [Indexes File Mode 'rb' is Binarray Mode `r` is Text Mode] default is `rb`.
                ** NOTE: idx_mode Must Can Read From File.
                ** More Info See `ModeName` & `Protocol` & `StoreFileIndexes` Module.

        return:
            [NamedTuple[int, str | os.PathLike, str]]: [Write Info].
                ** 'WriteMosaicInfo('write': int, 'path': int, 'type': str)'
                ** More Info See `write_info` Static Method.
        """
        # Check Can Write
        _can_read = self.mode_name(idx_mode).can_read

        if not _can_read:
            raise FileIsNotReadableError

        # To Real Path With `realpaths` Static Method
        idx_path, path = self.realpaths(idx_path, path)

        # Load Indexes With `FILE_INDEXES` Module Open Result File For Write Result
        with self.FILE_INDEXES(idx_path, idx_mode) as ip, open(path, 'wb') as f:
            # Back To Source & Write To Result File
            writes = f.write(b''.join(super(MosaicFile, self).to_data(ip, start_block)))

        return self.write_info(writes, path, 2)

    @staticmethod
    def mode_name(mode: str) -> ModeName:
        """
        Regular File Mode To Mosaic `ModeName` Module - Static Method
        args:
            mode [str]: [mode name].
                ** More Info See `ModeName` Module.
                ** 'wb', 'w', 'r', 'rb', ...

        return:
            [ModeName]: [Mosaici ModeName Protocol].
        """
        return ModeName(mode)

    @staticmethod
    def realpaths(*paths: str | os.PathLike) -> tuple[os.PathLike, ...]:
        """
        Paths To RealPaths - Static Method
        args:
            *paths [str | PathLike]: [Paths or Path Converting To Real Path or Paths]

        return:
            [tuple[PathLike]]: [Tuple Of Converted Paths To realpaths].
        """
        return tuple((os.path.realpath(path) for path in paths))

    @staticmethod
    def write_info(write: int, path: str | os.PathLike, _type: int) -> NamedTuple[int, str | os.PathLike]:
        """
        Write Info - Static Method
        args:
            write [int]: [How Many Write To File].
            path [str|PathLike]: [Write To This Path].
            _type [int]: [Type Of This File].
                ** `1` Means Indexes File - to_mosaici use `1`.
                ** `2` Means Data File - to_data use `2`.
        """

        match _type:
            case 1:
                _type = 'INDEXES'
            case 2:
                _type = 'DATA'

        info = NamedTuple('WriteMosaicInfo', (('write', int), ('path', str | os.PathLike), ('type', str)))
        return info(write, path, _type)


# STANDARD MOSAIC
class MosaicObject(BaseMosaicFileTemplate):
    """
    Mosaic - Instance of BaseMosaicFileTemplate
    """
    TEMPLATE: Template = Template
    ACTIVE_MAKER: bool = True
    FILE_TEMPLATE: FileTemplate = FileTemplate
    STORE_INDEXES: StoreObjectIndexes = StoreObjectIndexes



__dir__ = ('BaseMosaic', 'MosaicFile', 'MosaicObject')
