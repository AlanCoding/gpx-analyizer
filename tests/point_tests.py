from nose.tools import *
from gpxstats.objects import Point

point_string = """<trkpt lat="38.934579" lon="-77.392527"><ele>202.49</ele>
<time>2014-02-22T14:45:30Z</time><extensions><gpxtpx:TrackPointExtension>
<gpxtpx:speed>4.12</gpxtpx:speed><gpxtpx:course>259.76</gpxtpx:course>
</gpxtpx:TrackPointExtension></extensions></trkpt>"""

def setup():
    pass

def teardown():
    pass

def test_point_creation():
    pt = Point(point_string, None, None)
    assert pt.speed == 4.12
