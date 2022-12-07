import functools
from pyfunctional.pftyping import *


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


class openrange:
    def __init__(self, start: int, *, step: int = 1):
        self.start = start
        self.current = start
        self.step = step

    def __iter__(self) -> 'openrange':
        return self

    def __next__(self) -> int:
        temp = self.current
        self.current += self.step
        return temp

    def __repr__(self) -> str:
        return 'openrange({}{})'.format(self.start, ', step={}'.format(self.step) if self.step != 1 else '')

    def __str__(self) -> str:
        return repr(self)


def rreduce(
    reduction: Callable[[R, E], R],
    indexable: Indexable,
    initvalue: Union[R, Sentinel] = sentinel
) -> R:
    if initvalue is sentinel and len(indexable) == 0:
        raise ValueError("rreduce() of empty sequence with no initial value")
    acc = initvalue if initvalue is not sentinel else indexable[-1]
    for i in range(-2 if initvalue is sentinel else -1, -len(indexable) - 1, -1):
        acc = reduction(acc, indexable[i])
    return acc


def commute(fn: Callable[[S, T], R]) -> Callable[[T, S], R]:
    if not callable(fn):
        raise TypeError("Cannot commute non callable object {}".format(fn))

    if fn.__code__.argcount != 2:
        # todo: support varargs
        raise ValueError("Function must have exactly 2 arguments not")

    @functools.wraps(fn)
    def inside(a, b):
        return fn(b, a)

    return inside


def identity(x: T) -> T:
    return x
