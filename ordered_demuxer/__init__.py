import uuid
from dataclasses import dataclass
from typing import Iterator, Callable, TypeVar, Union, Optional, Any, Generic, List

T = TypeVar("T")


@dataclass
class FilterCondition(Generic[T]):
    condition: Callable[[T], bool]
    name: str = str(uuid.uuid4())

    def __call__(self, x: Any) -> bool:
        return self.condition(x)


class MiniStop(Exception):
    item: Any
    condition: FilterCondition

    def __init__(self, message="", item=None, condition=None):
        self.item = item
        self.condition = condition
        super().__init__(message)


@dataclass
class _iterator(Generic[T]):
    """
        Internal Iterator for OrderedDemuxer

        :param Iterator[T] data_source:                 Mutable Data Iterator
        :param List[FilterCondition[T]] filter:         Named List of Filter Conditions
        :param Optional[FilterCondition] condition_met  Condition causing a new iterator 
                                                        to be created, will initially be NULL
    """
    data_source: Iterator[T]
    filter: List[FilterCondition[T]]
    _buffer: Optional[T] = None

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self._buffer is not None:
            item = self._buffer
            self._buffer = None
            return item
        item = self.data_source.__next__()
        for filter in self.filter:
            if filter(item):
                raise MiniStop(item=item, condition=filter)
        return item


class OrderedDemuxer(Generic[T]):
    """
    Single pass approach to Demultiplexing/Demuxing

    Break an iterator into multiple iterators based on a break filter.
    Typical demuxers will place elements into different iterators,
    such as splitting [0,1,2,3] into ([0,2], [1,3]) based on odd or
    even elements.

    Assumes an input such as
    [
        0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0
    ]
    With `split_after` as False;
    Breaking it into
    [
        [0, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]
    ]
    With `split_after` as True;
    Breaking it into
    [
        [0, 0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0]
    ]


    i.e.
    >>> x = [1, 2, 3, 4]
    >>> y = FilterCondition(lambda x: x > 2)
    >>> splt = OrderedDemuxer(data_source=iter(x), filter=y, split_after=False)
    >>> x_iter = splt.__next__()
    >>> print(list(x_iter))
        [1, 2]

    Warnings
    --------
    The iterators returned are lazy - they will do nothing if not consumed. You can 
    call __next__ infinite times and not exhaust the item as the internal iterator 
    is staying at the same point.

    :param Iterator[T] data_source:         Source Iterator
    :param Callable[[T], bool] filter:      Conditional on which to split the iterator
    :param bool repeat:                     Whether to filter each time the conditional is met
    :param bool split_after:                Create new iterator on element after filter match
    """

    data_source: Iterator[T]
    filter: List[FilterCondition]
    _buffer: Optional[T]

    def __init__(
        self,
        data_source: Iterator[T],
        filter: Union[FilterCondition, List[FilterCondition]],
        repeat: bool = False,
        split_after: bool = True,
    ):
        self.data_source = data_source
        self.filter = filter if isinstance(filter, list) else [filter]
        self.repeat = repeat
        self.split_after = split_after
        self._buffer = None
        self._iterator = _iterator(self.data_source, self.filter)
        self.condition_met : Optional[FilterCondition] = None

    def __iter__(self):
        return self

    def __next__(self) -> Iterator[T]:
        try:
            yield from self._iterator
        except MiniStop as m:
            if self.split_after:
                yield m.item
                m.item = None
            self.condition_met = m.condition
            self._iterator = _iterator(
                self.data_source,
                self.filter if self.repeat else [],
                _buffer=m.item,
            )

