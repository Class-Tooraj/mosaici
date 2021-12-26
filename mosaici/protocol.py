from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
from functools import lru_cache

# IMPORT LOCAL
from mosaici.pattern import Convertor


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# PROTOCOL ABSTRACT
class BaseProtocol:
    """
    Protocol
    """
    SEPARATOR: tuple[str, bytes]

    def __init__(self, convertor: Convertor) -> None:
        """
        Initialize Protocol

        const:
            SEPARATOR [tuple[str, bytes]]: [Separator String and Bytes For Joining Together].

        args:
            convertor [Convertor]: [Standard Convertor Type].
        """
        if not self.SEPARATOR:
            raise NotImplementedError

        self._convertor = convertor

    def __call__(self, value: int | str, type_io: str) -> int | str:
        """
        This Method Calls For Validate Value To Protocol
        args:
            value [int | str]: [Value Must be int Or Standard String]

        return:
            [int | str]: [Validate Value With Protocol]
        """
        raise NotImplementedError

    @lru_cache(1)
    def __getitem__(self, name: str) -> str | bytes:
        """
        Get Separator
        args:
            name [str]: [Name of separator].
                ** VALID NAMES : (string >> ['w', 'a', 'str', 's']), (bytes >> ['wb', 'ab', 'bytes', 'b'])

        return:
            [str | bytes]: [Separator By Name].
        """
        match name:
            case 'w' | 'a' | 'str' | 's':
                return self.SEPARATOR[0]
            case 'wb' | 'ab' | 'bytes' | 'b':
                return self.SEPARATOR[-1]

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(STR_SEPARATOR: [{self.SEPARATOR[0]}], BYTES_SEPARATOR: [{self.SEPARATOR[-1]}])"


# STANDARD WRITE PROTOCOL
class WriteProtocol(BaseProtocol):
    SEPARATOR: tuple[str, bytes] = ('', b'')

    def __init__(self) -> None:
        """
        Standard Write Protocol
        """
        super(WriteProtocol, self).__init__(Convertor())
        self._str_validate = lambda x: self._convertor.std_hex(x)
        self._byt_validate = lambda x: bytes([self._convertor.std_int(x)])

    @lru_cache(256)
    def __call__(self, value: int | str, type_io: str) -> str | bytes:
        """
        Value To Standard Protocol For Write To File - String or Bytes.
        if `type_io` is String `Text` return Type is String.
        if `type_io` is Bytes `Binarray` return Type is Bytes.
        args:
            value [int | str]: [Value Must be int Or Standard String].
            type_io [str]: [IO Mode 'w' or 'wb' or 'a' or 'ab'].

        return:
            [str | bytes]: [Standard Value String or Bytes].
        """
        match type_io:
            case 'w' | 'a':
                return self._str_validate(value)
            case 'wb' | 'ab':
                return self._byt_validate(value)


# STANDARD READ PROTOCOL
class ReadProtocol(BaseProtocol):
    # TODO: Need Work
    pass



__dir__ = ('BaseProtocol', 'WriteProtocol', 'ReadProtocol')
