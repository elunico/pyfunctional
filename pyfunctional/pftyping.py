from typing import *
import sys

if sys.version.startswith('3.7'):
    class Protocol:
        pass


class Indexable(Protocol):
    # Protocols for indexable object for rreduce
    def __getitem__(self, index: int) -> Any: ...
    def __len__(self) -> int: ...


# return values
R = TypeVar('R')

# element type values
E = TypeVar('E')

# any type
S = TypeVar('S')

# any type
T = TypeVar('T')

# exception types
X = TypeVar('X', bound=BaseException)


class Sentinel(object):
    # used instead of None so defaults can support items with None
    pass


# sentinel for default args that support None
sentinel = Sentinel()
