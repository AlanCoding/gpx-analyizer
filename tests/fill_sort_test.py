from nose.tools import *
from gpxstats import processors

def setup():
    pass

def teardown():
    pass

def test_insert_position():
    pcls = processors.TopAttributes()
    array = [3, 2, 1]
    pcls.bump_insert(array, 2, 1)
    assert array == [3, 2, 2]
    array = [3, 2, 1]
    pcls.bump_insert(array, 2, 1)
    assert array == [3, 2, 2]
