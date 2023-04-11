import functools
import copy
from pyfunctional.pftyping import *


def attempt(
        block: Callable[[Any], T],
        default: Optional[T] = None,
        catch: Union[Type[BaseException], Tuple[Type[BaseException]]] = (Exception,),
        args: Iterable[Any] = tuple(),
        kwargs: Dict[Any, Any] = dict()
) -> Optional[T]:
    """
    a function that takes a callable, a default value, a list of excpetion types,
    an arg tuple, and a kwarg dict and calls the callable, catching the
    exceptions specified, and returning the function value on success, the
    default value on a known caught exception, and allowing any other
    none-accounted for exceptions bubble up.
    """
    if not hasattr(catch, '__iter__'):
        catch = (catch, )
    try:
        return block(*args, **kwargs)
    except catch:
        return default


def alleq(iterable: Iterable[S]) -> bool:
    """returns True if an iterable is empty or if all elements are equal to the first"""
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return True  # vacuously
    return not any(i != first for i in iterator)


class transpose:
    """an iterable object that takes a nested iterable and transposes it lazily"""

    def __init__(self, double_iterable: Iterable[Iterable[S]]) -> None:
        if isinstance(double_iterable, transpose):
            self.result = double_iterable.original
            self.original = double_iterable.result
        else:
            self.original = copy.deepcopy(double_iterable)
            self.result = zip(*double_iterable)

    def __repr__(self) -> str:
        return '<transpose object at {}>'.format(hex(id(self)))

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> 'transpose':
        return self

    def __next__(self) -> Iterable[S]:
        return next(self.result)


class repeat:
    """
    an iterable object that takes an element and a count and returns that
    element `count` times

    If `copying` is True then each element from the iterator will be a copy of the original
    if `copying` is False then the same object will be returned each time next is called
    """

    def __init__(self, item: E, number: int, copying: bool = True) -> None:
        if number < 0:
            raise ValueError("Number cannot be < 0")
        if type(number) is not int:
            raise TypeError("number must be int")
        self.item = item
        self.number = number
        self.count = 0
        self.transform = copy.deepcopy if copying else identity

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
        return self.transform(self.item)


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
    """
    Performs the same operation as `functools.reduce` but working from
    the right side (high indices) of the collection rather than the start
    (lower indices) of the collection. Requires the collection to support
    `len()` and indexing (iterators do not support `__getitem__` but
    lists and tuples--for example--do)
    """
    if initvalue is sentinel and len(indexable) == 0:
        raise ValueError("rreduce() of empty sequence with no initial value")
    acc = initvalue if initvalue is not sentinel else indexable[-1]
    for i in range(-2 if initvalue is sentinel else -1, -len(indexable) - 1, -1):
        acc = reduction(acc, indexable[i])
    return acc


def commute(fn: Callable[[S, T], R]) -> Callable[[T, S], R]:
    """
    Commutes the operands of a binary function. Does not (yet) work for varargs
     or functions other than 2-arity
     """
    if not callable(fn):
        raise TypeError("Cannot commute non callable object {}".format(fn))

    if fn.__code__.argcount != 2:
        # todo: support varargs
        raise ValueError("Function must have exactly 2 arguments not")

    return functools.wraps(fn)(lambda a, b: fn(b, a))


def identity(x: T) -> T:
    """
    The identity function
    """
    return x


def alwaysfalse(*args, **kwargs) -> bool:
    return False


def alwaystrue(*args, **kwargs) -> bool:
    return True


def alwaysnone(*args, **kwargs) -> None:
    return None


def bind(fn: Callable[[Any], R], arg: Any, position: int = 0) -> Callable[[Any], R]:
    """
    Given a `n`-arity function `fn`, bind `arg` to the `position`th argument of `fn`
    and return a new function which takes `n-1` args. The new function behaves as if
    the positional argument at `position` was removed from the argument order.

    The argument count is 0 based

    If `fn.__code__.co_argcount` is less or equal to `position` the function will raise a `ValueError`
    """
    if not hasattr(fn, '__code__'):
        raise TypeError("fn is not a function")

    if fn.__code__.co_argcount <= position:
        raise ValueError("Function does not have an argument at position {}".format(position))

    return functools.wraps(fn)(lambda *args: fn(*args[:position], arg, *args[position:]))


def full(fn: Callable[[Any], R], *args: Any) -> Callable[[], R]:
    """
    Like functools.partial, except requires you to fill in **all** the arguments of `fn`. Returns a new function
    that passes `*args` to `fn` but takes no arguments itself and returns the return value of `fn`
    """
    return functools.wraps(fn)(lambda: fn(*args))
