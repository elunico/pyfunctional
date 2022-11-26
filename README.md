# pyfunctional

This is a collection of functional tools I like to use in Python

## Contents

```python
alleq(iterable: Iterable[S]) -> bool
```

returns True if an iterable is empty or if all elements are equal to the first

---

```python
transpose(double_iterable: Iterable[Iterable[S]])
```

an iterable object that takes a nested iterable and transposes it lazily

---

```python
repeat(element: E, count: int)
```

an iterable object that takes an element and a count and returns that element `count` times

---

```python
attempt(
  block: Callable[[Any], T],
  default: T = None,
  catch: Union[Type[Exception], Iterable[Type[Exception]]] = (Exception,),
  args: Iterable[Any],
  kwargs: Dict[Any, Any]
) -> T
```

a function that takes a callable, a default value, a list of excpetion types, an arg tuple, and a kwarg dict and calls the callable, catching the exceptions specified, and returning the function value on success, the default value on a known caught exception, and allowing any other none-accounted for exceptions bubble up.
