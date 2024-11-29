import project
import requests


def test_get_wea_data():
    try:
        if requests.get("http://google.com").ok:
            data = project.get_wea_data()
            assert isinstance(data, dict)
            assert "weather" in data
    except requests.exceptions.ConnectionError:
        assert project.get_wea_data() is None


def test_get_geo_data():
    try:
        if requests.get("http://google.com").ok:
            data = project.get_geo_data()
            assert isinstance(data, dict)
            assert "moon_phase" in data
    except requests.exceptions.ConnectionError:
        assert project.get_geo_data() is None


def test_get_season():
    assert project.get_season(4) == "spring"
    assert project.get_season(7) == "summer"
    assert project.get_season(10) == "autumn"
    assert project.get_season(1) == "winter"
