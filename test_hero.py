import pytest
import requests_mock
from hero import BASE_URL, get_tallest_hero

# Создал мок чтобы можно было сделать больше тестов и проверить на устойчвость функцию
@pytest.fixture
def mock_hero_api():
    return [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {
                "gender": "Male",
                "height": ["6'8", "203 cm"]
            },
            "work": {
                "base": "New York"
            }
        },
        {
            "id": 2,
            "name": "Superman",
            "appearance": {
                "gender": "Male",
                "height": ["7'1", "2.15 meters"]
            },
            "work": {
                "base": "Metropolis"
            }
        },
        {
            "id": 3,
            "name": "Batman",
            "appearance": {
                "gender": "Male",
                "height": ["6'2", "188 cm"]
            },
            "work": {
                "base": "-"
            }
        },
        {
            "id": 4,
            "name": "Wonder Woman",
            "appearance": {
                "gender": "Female",
                "height": ["6'0", "183 cm"]
            },
            "work": {
                "base": "Themyscira"
            }
        },
        {
            "id": 5,
            "name": "Broken height Hero",
            "appearance": {
                "gender": "Male",
                "height": ["-", "unknown"]
            },
            "work": {
                "base": "NYC"
            }
        }
    ]


# Попарное тестирование
@pytest.mark.parametrize("sex, work, expected_name", [
    ("Male", True, "Superman"),
    ("Male", False, "Batman"),
    ("Female", True, "Wonder Woman"),
    ("Female", False, None)
])
def test_get_tallest_hero(sex, work, expected_name, mock_hero_api):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/all.json", json=mock_hero_api)
        tallest = get_tallest_hero(sex, work)
        if expected_name is None:
            assert tallest is None
        else:
            assert tallest is not None
            assert tallest["name"] == expected_name
            assert tallest["height"] > 0


# Граничные значения
def test_empty_heroes_list():
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/all.json", json=[])
        assert get_tallest_hero("Male", True) is None

def test_single_hero():
    single_hero = [{
            "id": 1,
            "name": "A-Bomb",
            "appearance": {
                "gender": "Male",
                "height": ["6'8", "203 cm"]
            },
            "work": {
                "base": "New York"
            }
        }]
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/all.json", json=single_hero)

        tallest = get_tallest_hero("Male", True)
        assert tallest is not None
        assert tallest["name"] == "A-Bomb" 
        assert tallest["height"] == 203.0 
        
def test_broken_height(mock_hero_api):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/all.json", json=mock_hero_api)
        
        tallest = get_tallest_hero("Male", True)
        assert tallest is not None
        assert tallest["name"] == "Superman"

@pytest.mark.parametrize("sex, work", [("Male", True),("Male", False), ("Female", True), ("Female", False)])
def test_real_API_height(sex, work):
    tallest = get_tallest_hero(sex, work)
    
    assert tallest is not None
    assert isinstance(tallest["name"], str)
    assert tallest["height"] > 0