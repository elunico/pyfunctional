from typing import *

T = TypeVar('T')
X = TypeVar('X', bound=BaseException)


def attempt(
        block: Callable[[Any], T],
        default: Optional[T] = None,
        catch: Union[Type[BaseException], Tuple[Type[BaseException]]] = (Exception,),
        args: Iterable[Any] = tuple(),
        kwargs: Dict[Any, Any] = dict()
) -> Optional[T]:
    if not hasattr(catch, '__iter__'):
        catch = (catch, )
    try:
        return block(*args, **kwargs)
    except catch:
        return default


S = TypeVar('S')


def alleq(iterable: Iterable[S]) -> bool:
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return True  # vacuously
    return not any(i != first for i in iterator)


class transpose:
    def __init__(self, double_iterable: Iterable[Iterable[S]]) -> None:
        self.result = zip(*double_iterable)

    def __repr__(self) -> str:
        return 'transpose object at {}'.format(hex(id(self)))

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> 'transpose':
        return self

    def __next__(self) -> Iterable[S]:
        return next(self.result)


E = TypeVar("E")


class repeat:
    def __init__(self, item: E, number: int) -> None:
        if number < 0:
            raise ValueError("Number cannot be < 0")
        if type(number) is not int:
            raise TypeError("number must be int")
        self.item = item
        self.number = number
        self.count = 0

    def __repr__(self) -> str:
        return 'repeat({}, {})'.format(repr(self.item), repr(self.number))

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> 'repeat':
        return self

    def __next__(self) -> E:
        if self.count == self.number:
            raise StopIteration()
        self.count += 1
        return self.item
