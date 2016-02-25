from nose.tools import *
from alancodinggpx import processors

def setup():
    pass

def teardown():
    pass

def test_insert_position():
    array = [3, 2, 1]
    processors.bump_insert(array, 2)
    assert array == [3, 2, 2]
