from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT LOCAL
from mosaici.order import Order, BaseOrder


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# BLOCK ABSTRACT
class BaseBlock:
    REPEAT: int
    SEPARATOR: str
    ORDER: BaseOrder
    DEFAULT_SYMBOL: tuple[str, ...]

    def __init__(self, block: tuple[int, ...] = None, order: BaseOrder | str = None, default_block: list[int] = None) -> None:
        """
        const:
            REPEAT [int]: [Repeat Pattern].
            SEPARATOR [str]: [Seprator Between Indexes].
            ORDER [BaseOrder]: [Order Object].
            DEFAULT_SYMBOL [tuple[str]]: [Symbol For Use Default Order].
        args:
            block [tuple[int]]: [Custom Block Use] default is `None`.
            order [BaseOrder | str]: [Order Object or Pattern] default is `None`.
            default_block [list[int]]: [Default Block Use For Make Block] default is `None`.
        """
        if not self.REPEAT or not self.SEPARATOR or not self.ORDER:
            raise NotImplemented

        self._block = block
        self._default = default_block

        if isinstance(order, str) and order not in self.DEFAULT_SYMBOL:
            self._order = self.ORDER(order)
        else:
            self._order = order

        if isinstance(self._order, str) and self._order in self.DEFAULT_SYMBOL:
            self._order = self.default_order(self.ORDER)

        if self._block is None:
            self._make_block()

        # For Iterable Save Last Index Wrapped
        # Iter indexes `0` to `255` then Stop Iteration If Call Again This Attr = 0 and loop Again
        self._current = 0

    def _make_block(self) -> None:
        """
        Create Block If Block is `None`
        """
        raise NotImplemented

    def index(self, value: int) -> int:
        """
        args:
            value [int]: [Target Value for Get Indexes in Block].
        return:
            [int]: Index of Value In Block.
        """
        return self._block.index(value)

    def data_to_idx(self, data: bytes) -> str:
        """
        args:
            data [bytes]: [Target Data For Translate To Indexes Sequence].
        return:
            [str]: [Sequence Of Hex Indexes].
        """
        res = []
        for i in data:
            res.append(hex(self.index(i)).removeprefix('0x').upper())
        return self.SEPARATOR.join(res)

    def idx_to_data(self, indexes: str) -> bytes:
        """
        args:
            indexes [str]: [Sequens of Indexes For Translate To Source Bytes].
        return:
            [bytes]: [Source Bytes].
        """
        indexes = indexes.split(self.SEPARATOR)
        res = b''
        for i in indexes:
            i = int(i, 16)
            res += bytes([self[i]])
        return res

    def to_hex(self) -> list[hex]:
        """
        return:
            [list[hex]]: [Block To List Of Hex Value]
        """
        return [hex(i).removeprefix('0x').upper() for i in self._block]

    def to_bytes(self) -> list[bytes]:
        """
        return:
            [list[bytes]]: [Block To List Of Bytes Value]
        """
        return [bytes([i]) for i in self._block]

    def to_bin(self) -> list[bin]:
        """
        return:
            [list[bin]]: [Block To List Of Binarry Value]
        """
        return [bin(i).removeprefix('0b') for i in self._block]

    def __iter__(self) -> object:
        """
        Iterable Block
        Any Time Call Iter Or Use Iter Current Index Cleared.
            `self._current = 0`
        """
        self._current = 0
        return self

    def __next__(self) -> int:
        """
        Iterable Items
        return:
            [int]: [Item]
        """
        try:
            get = self[self._current]
            self._current += 1
            return get
        except IndexError:
            raise StopIteration

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseBlock):
            return self._block == other._block
        raise NotImplementedError

    def __nq__(self, other: object) -> bool:
        if isinstance(other, BaseBlock):
            return self._block != other._block
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._block)

    def __getitem__(self, idx: int) -> int:
        """
        args:
            idx [int]: [Index of Value].
        return:
            [int]: [Value Places in Indexes].
        """
        return self._block[idx]

    def __contains__(self, value: int) -> bool:
        """
        args:
            value [int]: [Value Is Containes In Block].
        return:
            [bool]: [True if Exists False OtherWise]
        """
        return value in self._block

    def __enter__(self) -> object:
        return self

    def __exit__(self, *_) -> None:
        try:
            pass
        finally:
            del self

    def __repr__(self) -> str:
        """
        Repr Of Block
        """
        return f"{type(self).__qualname__}({', '.join(self.to_hex())})"

    def __str__(self) -> str:
        """
        Block To String
        """
        return f"({', '.join(self.to_hex())})"

    @staticmethod
    def default_order(order_obj: BaseOrder) -> BaseOrder:
        """
        Default Order If Use DEFAULT_SYMBOL
        args:
            order_obj [BaseOrder]: [Use Order Const For Make Default Order]
        return:
            [BaseOrder]: [Order Object With Default Pattern]
        """
        raise NotImplemented


# BLOCK
class Block(BaseBlock):
    """
    Block Object Instance Of BaseBlock
    """
    REPEAT: int = 1
    SEPARATOR: str = ' '
    ORDER: Order = Order
    DEFAULT_SYMBOL: tuple[str, ...] = ('', ' ', '/', '-', '#', '!')

    def _make_block(self) -> None:
        stack = self._default or [i for i in range(0, 256)]

        if self._order is None:
            self._block = stack
            return

        counter = 0
        while counter < self.REPEAT:

            # Check If Order Not Endless (order is limited) Then reset
            if not self._order.endless():
                self._order = iter(self._order)

            for _ in range(0, len(self._order)):
                start, end = next(self._order)
                stack = [*stack[start: end], *stack[end: ],*stack[: start]]

            counter += 1

        self._block = tuple(stack)

    @staticmethod
    def default_order(order_obj: Order) -> Order:
        SEPARATOR = order_obj.SEPARATOR
        res = []
        for i in range(0, 100):
            for j in range(100, 256):
                res.append(f'{hex(i)}/{hex(j)}')
        return order_obj(SEPARATOR.join(res))


__dir__ = ('Block', 'BaseBlock')
