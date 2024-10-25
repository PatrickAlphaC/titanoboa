import boa


def test_decode_struct():
    code = """
struct Point:
    x: int8
    y: int8

point: Point

@deploy
def __init__():
    self.point = Point({x: 1, y: 2})
"""
    result = boa.loads(code)._storage.point.get()
    assert str(result) == "Point({'x': 1, 'y': 2})"


def test_decode_tuple():
    code = """
point: (int8, int8)

@deploy
def __init__():
    self.point[0] = 1
    self.point[1] = 2
"""
    assert boa.loads(code)._storage.point.get() == (1, 2)


def test_decode_string_array():
    code = """
point: int8[2]

@deploy
def __init__():
    self.point[0] = 1
    self.point[1] = 2
"""
    assert boa.loads(code)._storage.point.get() == [1, 2]


def test_decode_bytes_m():
    code = """
b: bytes2

@deploy
def __init__():
    self.b = 0xd9b6
"""
    assert boa.loads(code)._storage.b.get() == bytes.fromhex("d9b6")


def test_decode_dynarray():
    code = """
point: DynArray[int8, 10]

@deploy
def __init__():
    self.point = [1, 2]
"""
    assert boa.loads(code)._storage.point.get() == [1, 2]


def test_self_destruct():
    code = """
@external
def foo() -> bool:
    selfdestruct(msg.sender)
    """
    c = boa.loads(code)

    c.foo()


def test_contract_name():
    code = """
@external
def foo() -> bool:
    return True
    """
    c = boa.loads(code, name="return_one", filename="return_one.vy")

    assert c.contract_name == "return_one"
    assert c.filename == "return_one.vy"

    c = boa.loads(code, filename="a/b/return_one.vy")

    assert c.contract_name == "return_one"
    assert c.filename == "a/b/return_one.vy"

    c = boa.loads(code, filename=None, name="dummy_name")

    assert c.contract_name == "dummy_name"
    assert c.filename == "<unknown>"

    c = boa.loads(code, filename=None, name=None)

    assert c.contract_name == "<unknown>"
    assert c.filename == "<unknown>"
