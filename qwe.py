import xml.etree.ElementTree as ET
import json

# Функция для определения типа транспорта по его ID
def get_transport_type(type_id):
    types = {
        '1': 'UB',  # Городской автобус
        '2': 'MT',  # Метрополитен
        '3': 'TB',  # Троллейбус
        '4': 'TM',  # Трамвай
        '5': 'ET',  # Электропоезд
        '6': 'RT',  # Речной транспорт
    }
    return types.get(type_id, '')

# Функция для определения принадлежности маршрута по его ID
def get_affiliation(affiliation_id):
    affiliations = {
        '1': 'Городской муниципальный маршрут',
        '2': 'Коммерческий',
        '3': 'Пригородный',
        '4': 'Сезонный (дачный)',
        '5': 'Специальный',
        '6': 'Междугородный'
    }
    return affiliations.get(affiliation_id, '')

# Функция для парсинга XML и преобразования в JSON
def parse_xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    routes_data = {"routes": {}}

    for route in root.findall('route'):
        kr_id = route.find('KR_ID').text
        number = route.find('number').text
        direction = route.find('direction').text
        direction_en = route.find('directionEn').text
        transport_type_id = route.find('transportTypeID').text
        transport_type = route.find('transportType').text
        affiliation_id = route.find('affiliationID').text
        affiliation = route.find('affiliation').text
        realtime_forecast = route.find('realtimeForecast').text

        transport_type_abbr = get_transport_type(transport_type_id)
        affiliation_abbr = get_affiliation(affiliation_id)

        # Создаем ключ маршрута в словаре
        if transport_type_abbr not in routes_data["routes"]:
            routes_data["routes"][transport_type_abbr] = []

        # Создаем объект маршрута
        route_obj = {
            "id": kr_id,
            "routeNumber": number,
            "ru": {
                "directions": {}
            },
            "en": {
                "directions": {
                    "firstStop": direction_en,
                    "lastStop": direction_en
                }
            }
        }

        # Проверяем, является ли маршрут кольцевым
        if direction != route.find('directionEs').text:
            route_obj["ru"]["directions"]["D1"] = {
                "firstStop": direction,
                "lastStop": route.find('directionEs').text
            }
        else:
            route_obj["ru"]["directions"]["D1"] = ""

        routes_data["routes"][transport_type_abbr].append(route_obj)

    return json.dumps(routes_data, ensure_ascii=False, indent=4)

# Пример использования
xml_file_path = 'routes.xml'
json_data = parse_xml_to_json(xml_file_path)
print(json_data)
