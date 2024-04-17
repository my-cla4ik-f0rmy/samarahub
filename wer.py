import requests
import xml.etree.ElementTree as ET
import json

def get_route_data(relation_id):
    url = f"https://www.openstreetmap.org/api/0.6/relation/{relation_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        route_data = {"id": int(relation_id)}
        for tag in root.findall('.//tag'):
            if tag.attrib['k'] == 'ref':
                route_data['routeNumber'] = int(tag.attrib['v'])
                break
        directions = {}
        for member in root.findall('.//member'):
            direction_id = member.attrib['ref']
            directions[direction_id] = get_direction_data(direction_id)
        route_data['directions'] = directions
        return route_data
    else:
        return None

def get_direction_data(relation_id):
    url = f"https://www.openstreetmap.org/api/0.6/relation/{relation_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        direction_data = {}
        for tag in root.findall('.//tag'):
            if tag.attrib['k'] == 'ref':
                direction_data['direction'] = tag.attrib['v']
        direction_data['stops'] = []
        for member in root.findall('.//member'):
            if member.attrib['type'] == 'way' and member.attrib.get('role') == 'platform':
                stop_id = member.attrib['ref']
                stop_data = get_stop_data(stop_id)
                direction_data['stops'].append(stop_data)
        if direction_data['stops']:
            direction_data['firstStop'] = direction_data['stops'][0]['ru']
            direction_data['lastStop'] = direction_data['stops'][-1]['ru']
        return direction_data
    else:
        return None

def get_stop_data(way_id):
    url = f"https://www.openstreetmap.org/api/0.6/way/{way_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        stop_data = {}
        for tag in root.findall('.//tag'):
            if tag.attrib['k'] == 'name':
                stop_data['ru'] = tag.attrib['v']
        stop_data['id'] = way_id
        return stop_data
    else:
        return None

def main():
    initial_relation_id = "1663677"
    route_data = get_route_data(initial_relation_id)
    if route_data:
        print(json.dumps(route_data, ensure_ascii=False, indent=4))  # Вывод данных о маршруте в формате JSON
    else:
        print("Failed to fetch route data.")

if __name__ == "__main__":
    main()
