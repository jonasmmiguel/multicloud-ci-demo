from hello import add, multiply


def test_add():
    assert 2 == add(1, 1)
    
    
def test_multiply():
    assert multiply(3,-2) == -6