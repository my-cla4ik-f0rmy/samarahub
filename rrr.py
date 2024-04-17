import xml.etree.ElementTree as ET
import json
import requests

# Загрузка XML из URL
url = "https://tosamara.ru/api/v2/classifiers/stopsFullDB.xml"
response = requests.get(url)
xml_content = response.content

# Парсинг XML
tree = ET.ElementTree(ET.fromstring(xml_content))
root = tree.getroot()

# Введите список тегов, которые вы хотите включить в JSON
tags_to_include = [
    "KS_ID","title", "adjacentStreet", "direction",
    "titleEn", "adjacentStreetEn", "directionEn",
    "busesMunicipal", "busesCommercial", "busesPrigorod",
    "busesSeason", "busesSpecial", "busesIntercity",
    "trams", "trolleybuses", "metros",
    "electricTrains", "riverTransports", "latitude", "longitude"
]

# Список для хранения остановок
stops = []

# Перебор всех элементов <stop> в XML
for stop in root.findall('stop'):
    stop_data = {}
    for elem in stop:
        if elem.tag in tags_to_include:
            if elem.tag.startswith("buses"):
                # Разделение строковых значений на списки целых чисел
                stop_data[elem.tag] = [bus.strip() for bus in elem.text.split(",")] if elem.text else []
            else:
                stop_data[elem.tag] = elem.text
    stops.append(stop_data)

# Запись данных в JSON-файл
with open('stops.json', 'w', encoding='utf-8') as f:
    json.dump(stops, f, ensure_ascii=False, indent=4)
