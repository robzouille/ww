from typing import Union, Callable, Iterable, Any
from itertools import takewhile, dropwhile, chain, islice


def starts_when(self, condition: Union[Callable, Any]):
    """Start yielding items when a condition arise.

    Args:
        condition: if the callable returns True once, start yielding
                   items. If it's not a callable, it will be converted
                   to one as `lambda condition: condition == item`.

    Example:

        >>> g(range(10)).starts(lambda x: x > 5).list()
        [6, 7, 8, 9]
        >>> g(range(10)).starts(7).list()
        [7, 8, 9]
    """
    if not callable(condition):
        value = condition
        condition = lambda x: value == x
    return g(dropwhile(lambda x: not condition(x), self.iterable))

def stops_when(self, condition: Union[Callable, Any]):
    """Stop yielding items when a condition arise.

    Args:
        condition: if the callable returns True once, stop yielding
                   items. If it's not a callable, it will be converted
                   to one as `lambda condition: condition == item`.

    Example:

        >>> g(range(10)).stops(lambda x: x > 5).list()
        [0, 1, 2, 3, 4, 5]
        >>> g(range(10)).stops(7).list()
        [0, 1, 2, 3, 4, 5, 6]
    """
    if not callable(condition):
        value = condition
        condition = lambda x: value == x
    return g(takewhile(lambda x: not condition(x), self.iterable))


def skip_duplicates(iterable: Iterable, key: Callable=lambda x: x):
    """
        Returns a generator that will yield all objects from iterable, skipping
        duplicates.

        Duplicates are identified using the `key` function to calculate a
        unique fingerprint. This does not use natural equality, but the
        result use a set() to remove duplicates, so defining __eq__
        on your objects would have no effect.

        By default the fingerprint is the object itself,
        which ensure the functions works as-is with an iterable of primitives
        such as int, str or tuple.

        :Example:

            >>> list(skip_duplicates([1, 2, 3, 4, 4, 2, 1, 3 , 4]))
            [1, 2, 3, 4]

        The return value of `key` MUST be hashable, which means for
        non hashable objects such as dict, set or list, you need to specify
        a a function that returns a hashable fingerprint.

        :Example:

            >>> list(skip_duplicates(([], [], (), [1, 2], (1, 2)), lambda x: tuple(x)))
            [[], [1, 2]]
            >>> list(skip_duplicates(([], [], (), [1, 2], (1, 2)), lambda x: (type(x), tuple(x))))
            [[], (), [1, 2], (1, 2)]

        For more complex types, such as custom classes, the default behavior
        is to remove nothing. You MUST provide a `key` function is you wish
        to filter those.

        :Example:

            >>> class Test(object):
            ...    def __init__(self, foo='bar'):
            ...        self.foo = foo
            ...    def __repr__(self):
            ...        return "Test('%s')" % self.foo
            ...
            >>> list(skip_duplicates([Test(), Test(), Test('other')]))
            [Test('bar'), Test('bar'), Test('other')]
            >>> list(skip_duplicates([Test(), Test(), Test('other')], lambda x: x.foo))
            [Test('bar'), Test('other')]

    """
    fingerprints = set()

    try:
        # duplicate some code to gain perf in the most common case
        if key is None:
            for x in iterable:
                if x not in fingerprints:
                    yield x
                    fingerprints.add(x)
        else:
            for x in iterable:
                fingerprint = key(x)
                if fingerprint not in fingerprints:
                    yield x
                    fingerprints.add(fingerprint)
    except TypeError:
        try:
            hash(fingerprint)
        except TypeError:
            raise TypeError(
                "The 'key' function returned a non hashable object of type "
                "'%s' when receiving '%s'. Make sure this function always "
                "returns a hashable object. Hint : immutable primitives like"
                "int, str or tuple, are hashable while dict, set and list are "
                "not." % (type(fingerprint), x))
        else:
            raise


def chunks(self, chunksize, process=tuple):
    """
        Yields items from an iterator in iterable chunks.
    """
    it = iter(self)
    while True:
        yield process(chain([next(it)], islice(it, chunksize - 1)))


def window(iterable, size=2, cast=tuple):
    """
        Yields iterms by bunch of a given size, but rolling only one item
        in and out at a time when iterating.

        >>> list(window([1, 2, 3]))
        [(1, 2), (2, 3)]

        By default, this will cast the window to a tuple before yielding it;
        however, any function that will accept an iterable as its argument
        is a valid target.

        If you pass None as a cast value, the deque will be returned as-is,
        which is more performant. However, since only one deque is used
        for the entire iteration, you'll get the same reference everytime,
        only the deque will contains different items. The result might not
        be what you want :

        >>> list(window([1, 2, 3], cast=None))
        [deque([2, 3], maxlen=2), deque([2, 3], maxlen=2)]

    """
    iterable = iter(iterable)
    d = deque(islice(iterable, size), size)
    if cast:
        yield cast(d)
        for x in iterable:
            d.append(x)
            yield cast(d)
    else:
        yield d
        for x in iterable:
            d.append(x)
            yield d