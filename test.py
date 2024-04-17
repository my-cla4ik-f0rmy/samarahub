import requests
import xml.etree.ElementTree as ET
import json
from transliterate import translit

# URL OpenStreetMap API
import requests
import xml.etree.ElementTree as ET

def get_route_data(relation_id):
    url = f"https://www.openstreetmap.org/api/0.6/relation/{relation_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        route_data = {}
        route_data['id'] = relation_id
        for tag in root.findall('.//tag'):
            if tag.attrib['k'] == 'ref':
                route_data['routeNumber'] = int(tag.attrib['v'])
            elif tag.attrib['k'] == 'name':
                route_data['routeName'] = tag.attrib['v']
        directions = []
        for member in root.findall('.//member'):
            direction_id = member.attrib['ref']
            directions.append(direction_id)
        route_data['directions'] = directions
        return route_data
    else:
        return None

print(get_route_data(1663677))

data = get_route_data(1663677)

for i in data['directions']:
    print(get_route_data(i))


url = "https://www.openstreetmap.org/api/0.6/relation/1663633"
base_url = "https://www.openstreetmap.org/api/0.6/way/{}"

# Список для хранения информации остановок
stops = []


# Проверка статуса запроса
    # Парсинг XML-ответа
for i in data['directions']:
    print(i)
    a = get_route_data(i)
    for j in a['directions']:
        print(j)
        root = j
        platform_url = base_url.format(root)
        platform_response = requests.get(platform_url)
        if platform_response.status_code == 200:
            platform_root = ET.fromstring(platform_response.content)
            name_tag = platform_root.find('.//tag[@k="name"]')
            if name_tag is not None:
                platform_name_ru = name_tag.attrib['v']
                platform_name_en = translit(platform_name_ru, 'ru', reversed=True)  # Транслитерация на английский
                stop_info = {
                    "id": platform_id,
                    "ru": platform_name_ru,
                    "en": platform_name_en
                }
                stops.append(stop_info)
            else:
                print("Для остановки ID:", platform_id, "нет информации о названии")
        else:
            print("Ошибка при получении информации об остановке ID:", platform_id, "- статус код:", platform_response.status_code)
else:
    print("Ошибка при выполнении запроса:", response.status_code)

# Вывод списка остановок в формате JSON
print(json.dumps({"stops": stops}, ensure_ascii=False, indent=4))
