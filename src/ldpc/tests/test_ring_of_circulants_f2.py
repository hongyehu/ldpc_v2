from ldpc.protograph import RingOfCirculantsF2

a = RingOfCirculantsF2([1, 3])
b = RingOfCirculantsF2([3, 1])
c = RingOfCirculantsF2([2, 3])
d = RingOfCirculantsF2([1])
e = RingOfCirculantsF2([])


def test_init_RingOfCirculants():
    assert d.coefficients == 1


def test_equality():
    assert (a == b) == True
    assert (a == c) == False
    assert a == [1, 3]
    assert d == [1]


def test_addition_RingOfCirculants():
    assert a+b == e
    assert (a+c) == [1, 2]
    assert (d+c) != [1, 2]

def test_len():
    assert len(a) == 2
