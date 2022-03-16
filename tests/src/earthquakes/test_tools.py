import pytest

from src.earthquakes import tools


def test_haversine_distance():
    ## REFERENCE https://www.vcalc.com/wiki/vCalc/Haversine+-+Distance
    target_value = 314.4
    assert pytest.approx(tools.compute_haversine(latitude_1=1, longitude_1=2, latitude_2=3, longitude_2=4,
                                                 radius=tools.EARTH_RADIUS) - target_value, target_value*0.01) == 0.0

    target_value = 2662.2
    assert pytest.approx(tools.compute_haversine(latitude_1=50, longitude_1=60, latitude_2=70, longitude_2=80,
                                                 radius=tools.EARTH_RADIUS) - target_value, target_value*0.01) == 0.0