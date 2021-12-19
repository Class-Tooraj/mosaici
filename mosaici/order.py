from __future__ import annotations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT TYPING
from typing import Generator

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# ORDER ABSTARCT
class BaseOrder:
    SEPARATOR: str
    MIXER: str

    def __init__(self, order: str, limited: bool) -> None:
        """
        const:
            SEPARATOR [str]: [Separator Symbol Between Pattern]
            MIXER [str]: [Symbol Mixer Starts & Ends Pattern]
        args:
            order [str]: [Order Sequence].
            limited [bool]: [Limited Order If Not Limited Wrapped EndLess] default is `True`.
        """
        if not self.SEPARATOR or not self.MIXER:
            raise NotImplementedError

        self._order = order.split(self.SEPARATOR)
        self._current = 0
        self._limited = limited

    def orderize(self) -> None:
        """
        Change Pattern When Not Limited
        """
        raise NotImplemented

    def __iter__(self) -> object:
        return self

    def __enter__(self) -> object:
        return self

    def __next__(self) -> Generator[tuple[int, int], None, None]:
        """
        Return Tuple (Start, End) Integer Value
        """
        if self._current >= len(self._order) and not self._limited:
            self.orderize()
            self._current = 0
        try:
            start, end = self._order[self._current].split(self.MIXER)
            self._current += 1
            return int(start, 16), int(end, 16)
        except IndexError:
            raise StopIteration

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseOrder):
            return self._order == other._order
        raise NotImplementedError

    def __nq__(self, other: object) -> bool:
        if isinstance(other, BaseOrder):
            return self._order != other._order
        raise NotImplementedError

    def __exit__(self, *_) -> None:
        try:
            pass
        finally:
            del self

    def __repr__(self) -> str:
        """
        Repr Of Order
        """
        order = (i.split(self.MIXER) for i in self._order)
        order = (f'({int(start, 16)}, {int(end, 16)})' for start, end in order)
        return f"{type(self).__qualname__}({'Limited' if self._limited else 'EndLess'}, {', '.join(order)})"

    def __str__(self) -> str:
        """
        Order To String
        """
        order = (i.split(self.MIXER) for i in self._order)
        order = (f'({int(start, 16)}, {int(end, 16)})' for start, end in order)
        return f"({', '.join(order)})"

    def __len__(self) -> int:
        """
        Len Order
        """
        return len(self._order)


# ORDER
class Order(BaseOrder):
    """
    Order Object Instance Of BaseOrder
    """
    SEPARATOR = ' '
    MIXER = '/'

    def __init__(self, order: str, limited: bool = True) -> None:
        super(Order, self).__init__(order, limited)

    def orderize(self) -> None:
        """
        Change Pattern With Standard Formolla
        """
        self._order = [*self._order[len(self._order)//2:], *self._order[: len(self._order)//2]]



__dir__ = ('Order', 'BaseOrder')
