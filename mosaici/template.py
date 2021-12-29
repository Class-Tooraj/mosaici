from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT LOCAL
from mosaici.order import Order, BaseOrder
from mosaici.block import Block, BaseBlock


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# DEFAULT BLOCK ITER TYPE SUPPORT
T_ITER: tuple[int, ...] | list[int] = tuple[int, ...] | list[int]

# TEMPLATE ABSTARCT
class BaseTemplate:
    REPEAT: int
    SIZE: int
    ORDER: BaseOrder
    BLOCK: BaseBlock
    SEPARATOR: str
    DEFAULT_SYMBOL: tuple[str, ...]

    def __init__(
        self,
        blocks: tuple[BaseBlock] = None,
        order: BaseOrder | str = None,
        default_block: BaseBlock | T_ITER = None,
        ) -> None:
        """
        const:
            REPEAT [int]: [Repeat Order Pattern if Use `Order` or `DefaultOrder`].
            SIZE [int]: [How Many Block in Template Only if Order is `None`].
            ORDER [BaseOrder]: [Order Object Must be instance of BaseOrder].
            BLOCK [BaseBlock]: [Block Object Must be instance of BaseBlock].
            SEPARATOR [str]: [Seperator Use For `Data to indexes` & `Indexes to Data`].
            DEFAULT_SYMBOL [tuple[str, ...]]: [Default Symbol When Want Use Default Order].
        args:
            blocks [tuple[BaseBlock]]: [Blocks if is `None` Make Blocks For Template] default is None.
            order [BaseOrder | str]: [Order for change layout Blocks & Template] default is None.
                ** order is None means without order pattern. **
                ** if want use default order use default symbol. **
            default_block [Block | T_ITER]: [Use Default Block for Making New Block Reletive With Default block] default is None.
        """

        if not self.REPEAT or not self.SIZE or not self.ORDER or not self.DEFAULT_SYMBOL:
            raise NotImplemented

        self._template = blocks
        self._default_block = default_block if default_block is not None else self.BLOCK(order=self.BLOCK.DEFAULT_SYMBOL[0])

        self._temp_block = None

        if isinstance(order, str) and order not in self.DEFAULT_SYMBOL:
            self._order = self.ORDER(order)
        else:
            self._order = order

        if isinstance(self._order, str) and self._order in self.DEFAULT_SYMBOL:
            self._order = self.default_order(self.ORDER, self.SIZE)

        if self._template is None:
            self._make_template()

        # Make This Object Iterable
        self._current = 0

    def _gen_default_block(self) -> BaseBlock:
        """
        Make Block When Order is None
        return:
            [BaseBlock]: [return new created block].
        """
        raise NotImplemented

    def _make_template(self) -> None:
        """
        Create Template
        """
        raise NotImplemented

    def to_hex(self) -> tuple[list[hex]]:
        """
        Template To Hex String
        """
        return [i.to_hex() for i in self._template]

    def to_bytes(self) -> tuple[list[bytes]]:
        """
        Template to Bytes
        """
        return [i.to_bytes() for i in self._template]

    def to_bin(self) -> tuple[list[bin]]:
        """
        Template to Binarry Strings
        """
        return [i.to_bin() for i in self._template]

    def index(self, block: int, value: int) -> int:
        """
        Index Value In Block
        args:
            block [int]: [Block Number]
            value [int]: [Value Target]
        return:
            [int]: [Indexes of Value in The Block]
        """
        block = self.valid_block(block, len(self))
        return self._template[block].index(value)

    def value(self, block: int, indexes: int) -> bytes:
        """
        Value From Indexes in Block
        args:
            block [int]: [Block Number].
            indexes [int]: [Index in Block].
        return:
            [bytes]: [Value in The Block & Indexes Place]
        """
        block = self.valid_block(block, len(self))
        return bytes([self._template[block][indexes]])

    def data_to_idx(self, data: bytes) -> str:
        """
        Data To Indexes
        args:
            data [bytes]: [Data For Convert To Indexes].
        return:
            [str]: [Indexes Of Data in Template].
        """
        res = []

        size = len(self)
        for idx_block, i in enumerate(data):
            _block = self.valid_block(idx_block, size)
            idx = self._template[_block].index(i)
            res.append(hex(idx).removeprefix('0x').upper())

        return self.SEPARATOR.join(res)

    def idx_to_data(self, indexes: str) -> bytes:
        """
        Indexes To Data
        args:
            indexes [str]: [Indexes Value].
        return:
            [bytes]: [Source Bytes].
        """
        indexes = indexes.split(self.SEPARATOR)
        res = b''

        size = len(self)
        for idx_block, i in enumerate(indexes):
            _block = self.valid_block(idx_block, size)
            value = self._template[_block][int(i, 16)]
            res += bytes([value])

        return res

    def __iter__(self) -> object:
        """
        Make Object Iterable
        """
        self._current = 0
        return self

    def __next__(self) -> BaseBlock:
        """
        Next Block
        """
        try:
            get = self._template[self._current]
            self._current += 1
        except IndexError:
            raise StopIteration

    def __enter__(self) -> object:
        return self

    def __len__(self) -> int:
        """
        Length Of Template
        """
        return len(self._template)

    def __getitem__(self, block_idx: int) -> BaseBlock:
        """
        Get Block From Indexes
        """
        return self._template[block_idx]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return self._template == other._template
        raise NotImplementedError

    def __nq__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return self._template != other._template
        raise NotImplementedError

    def __gt__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return len(self) > len(other)
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return len(self) < len(other)
        raise NotImplementedError

    def __ge__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return len(self) >= len(other)
        raise NotImplementedError

    def __le__(self, other: object) -> bool:
        if isinstance(other, BaseTemplate):
            return len(self) <= len(other)
        raise NotImplementedError

    def __contains__(self, value: int) -> bool:
        """
        All Blocks Must Be Same Value Only Value Places is Diffrent
        This Check if Value in First Block If True Means Value Existed In All Template Blocks
        args:
            value [int]: [Target Value].
        return:
            [bool]: [value contains template True OtherWise False]
        """
        return value in self[0]

    def __repr__(self) -> str:
        """
        Some Info With This Format
        'ObjectName(manyblocks, repeat, order)'
        """
        return f"{type(self).__qualname__}(blocks={len(self)}, repeat={self.REPEAT}, order={self._order})"

    def __str__(self) -> str:
        """
        Template To String With This Format - StringDict
        '{block_index: block, ...}'
        """
        to_str = (f"{n}: {str(i)}" for n,i in enumerate(self._template))
        return f"{{{', '.join(to_str)}}}"

    def __exit__(self, *_) -> None:
        try:
            pass
        finally:
            del self._temp_block, self._template, self._default_block
            del self

    @staticmethod
    def default_order(order_obj: BaseOrder, size: int) -> BaseOrder:
        """
        Created Default Order
        args:
            order_object [BaseOrder]: [self.ORDER Use When This Method Calls]
            size [int]: [self.SIZE Use When This Method Calls] 
        """
        raise NotImplemented

    @staticmethod
    def valid_block(idx_block: int, size: int) -> int:
        """
        Validate Block Number From Template
        When Block Indexes Bigger Than Blocks Validate Block Number.
        args:
            idx_block [int]: [Number Of Block].
        return:
            [int]: [Block if Exists OtherWise Converted To Existed Block].
        """
        # I Changed Algorithm - Fixed Problem Maximum Recursion & Very Low Speed For Working
        done = False
        while idx_block >= size:

            if idx_block == size:
                idx_block -= (size << 1)
                continue

            elif idx_block <= (size + (size//2)):
                idx_block <<= 1
                continue

            elif idx_block >= (size * 2):
                idx_block //= size
                continue

            else:
                idx_block -= size
                continue

        return idx_block

# TEMPLATE
class Template(BaseTemplate):
    REPEAT: int = 1
    SIZE: int = 256
    ORDER: Order = Order
    BLOCK: Block = Block
    SEPARATOR: str = ''
    DEFAULT_SYMBOL: tuple[str, ...] = ('', ' ', '/', '-', '#', '!')

    def _gen_default_block(self) -> Block:
        make_new = [*self._temp_block[1: ], *self._temp_block[: 1]]
        self._temp_block = self.BLOCK(order='', default_block=make_new)
        return self._temp_block

    def _make_template(self) -> None:
        if self._order is None:
            self._temp_block = self._default_block
            self._template = tuple((self._gen_default_block() for _ in range(0, self.SIZE)))
            return

        order = self._order
        self._temp_block = self.BLOCK(order=order, default_block=self._default_block)

        counter = 0
        template = []

        while counter < self.REPEAT:

            for _ in range(0, len(self._order)):
                template.append(self.BLOCK(order=self._order, default_block=self._temp_block))
                self._temp_block = template[-1]

            counter += 1

        self._template = template

    @staticmethod
    def default_order(order_obj: Order, size: int) -> Order:
        SEPARATOR = order_obj.SEPARATOR
        res = []
        for i in range(1, (size + 1)):
            res.append(f'{hex(i)}/{hex(i*2)}')
        return order_obj(SEPARATOR.join(res))



__dir__ = ('T_ITER', 'BaseTemplate', 'Template')
