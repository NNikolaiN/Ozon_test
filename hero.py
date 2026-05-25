import requests

BASE_URL = "https://akabab.github.io/superhero-api/api"


def get_heroes(HERO_API: str):
    response = requests.get(f"{HERO_API}/all.json", timeout=5)
    response.raise_for_status()
    return response.json()
            
def edit_height(height: str):
    try:
        edited_height = height.split()[0]
        if "meter" in height:
            return float(edited_height) * 100
        return float(edited_height)
    except (ValueError, IndexError, AttributeError):
        return 0.0

def get_tallest_hero(sex: str, work:bool):
    filtered_heroes = []
    
    list_of_heroes = get_heroes(BASE_URL)
    for hero in list_of_heroes:
        if hero["appearance"].get("gender") != sex:
            continue
        base = hero['work'].get('base')
        has_work = (base != '-')
        
        if has_work == work:
            height = edit_height(hero["appearance"]["height"][1])
            if height == 0:
                continue
            filtered_heroes.append({"id": hero["id"], "name" : hero["name"], "height": height})            
    
    if not filtered_heroes:
        return None
    tallest = max(filtered_heroes, key=lambda hero: hero["height"])
    return tallest

