# pyfunctional

Find it [on PyPI](https://pypi.org/project/pyfunctional-elunico/)

This is a collection of functional tools I like to use in Python

## Contents

```python
def alleq(iterable: Iterable[S]) -> bool
```

returns True if an iterable is empty or if all elements are equal to the first

---

```python
def transpose(double_iterable: Iterable[Iterable[S]])
```

an iterable object that takes a nested iterable and transposes it lazily

---

```python
def repeat(element: E, count: int)
```

an iterable object that takes an element and a count and returns that element `count` times

---

```python
def attempt(
  block: Callable[[Any], T],
  default: T = None,
  catch: Union[Type[Exception], Iterable[Type[Exception]]] = (Exception,),
  args: Iterable[Any],
  kwargs: Dict[Any, Any]
) -> T
```

a function that takes a callable, a default value, a list of excpetion types, an arg tuple, and a kwarg dict and calls the callable, catching the exceptions specified, and returning the function value on success, the default value on a known caught exception, and allowing any other none-accounted for exceptions bubble up.

---

```python
def rreduce(
    reduction: Callable[[R, E], R],
    indexable: Indexable,
    initvalue: Union[R, Sentinel] = sentinel
) -> R
```

Performs the same operation as `functools.reduce` but working from the right side (high indices) of the collection rather than the start (lower indices) of the collection. Requires the collection to support `len()` and indexing (iterators do not support `__getitem__` but lists and tuples--for example--do)

Not the specification for `Indexable` below

```python
from typing import Protocol

class Indexable(Protocol):
  def __getitem__(self, index: int) -> Any: ...
  def __len__(self) -> int: ...
```

---

```python
def commute(fn: Callable[[S, T], R]) -> Callable[[T, S], R]
```

Commutes the operands of a binary function. Does not (yet) work for varargs or functions other than 2-arity

---

```python
def identity(x: T) -> T
```

The identity function

---

```python
def bind(fn: Callable[[Any], R], arg: Any, position: int = 0) -> Callable[[Any], R]
```

Given a `n`-arity function `fn`, bind `arg` to the `position`th argument of `fn` and return a new function which takes `n-1` args. The new function behaves as if the positional argument at `posititon` was removed from the argument order.

The argument count is 0 based

If `fn.__code__.co_argcount` is less or equal to `posititon` the function will raise a `ValueError`

---

```python
def full(fn: Callable[[Any], R], *args: Any) -> Callable[[], R]
```

Like functools.partial, except requires you to fill in **all** the arguments of `fn`. Returns a new function
that passes `*args` to `fn` but takes no arguments itself and returns the return value of `fn`
