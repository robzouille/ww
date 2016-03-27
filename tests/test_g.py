
import pytest

from ww import g


def test_iter():

    for i, x in enumerate(g('abcd')):
        assert x == 'abcd'[i]

    for i, x in enumerate(g(list('abcd'))):
        assert x == 'abcd'[i]

    for i, x in enumerate(g(tuple('abcd'))):
        assert x == 'abcd'[i]

    assert set(g(set('abcd'))) == set('abcd')

    for i, x in enumerate(g(range(10))):
        assert x == i

    def foo():
        yield 0
        yield 1
        yield 2

    for i, x in enumerate(g(foo())):
        assert x == i


def test_nested():
    for i, x in enumerate(g(g(g('abcd')))):
        assert x == 'abcd'[i]


def test_accept_multi_iterables():

    numbers = list(map(int, g([1, 2, 3], '456', range(7, 10))))
    assert numbers == list(range(1, 10))


def test_next():

    gen = g('abc')
    assert next(gen) == 'a'
    assert gen.next() == 'b'


def test_cycle():

    gen = g('abc').cycle()
    assert next(gen) == 'a'
    assert next(gen) == 'b'
    assert next(gen) == 'c'
    assert next(gen) == 'a'
    assert isinstance(gen, g)


def test_add():

    gen = g('abc') + 'def'
    assert isinstance(gen, g)
    assert list(gen) == list('abcdef')

    gen = 'abc' + g('def')
    assert isinstance(gen, g)
    assert list(gen) == list('abcdef')


def test_sub():

    gen = g('abcdef') - 'ac'
    assert isinstance(gen, g)
    assert list(gen) == list('bdef')

    gen = 'abcdef' - g('ac')
    assert isinstance(gen, g)
    assert list(gen) == list('bdef')


def test_mul():

    gen = g(range(3)) * 3
    assert isinstance(gen, g)
    assert list(gen) == [0, 1, 2, 0, 1, 2, 0, 1, 2]

    gen = 2 * g(range(3))
    assert isinstance(gen, g)
    assert list(gen) == [0, 1, 2, 0, 1, 2]


def test_tee():

    gen = g(x * x for x in range(3))
    gen2, gen3 = gen.tee()

    assert list(gen2) == list(gen3) == [0, 1, 4]

    gen = g(x * x for x in range(3))
    all_gens = gen.tee(3)
    assert isinstance(all_gens, g)

    for x in all_gens:
        assert isinstance(x, g)
        assert list(x) == [0, 1, 4]

    gen = g(x * x for x in range(3))
    gen2, gen3 = gen.tee()

    with pytest.raises(RuntimeError):
        list(gen)