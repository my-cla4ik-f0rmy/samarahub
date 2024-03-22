import xml.etree.ElementTree as ET

def convert_routes_to_xml(routes):
    buses_municipal = ET.Element("busesMunicipal")
    for route in routes:
        route_element = ET.SubElement(buses_municipal, "route")
        number_element = ET.SubElement(route_element, "number")
        number_element.text = route.strip()  # Удаляем лишние пробелы и добавляем номер маршрута
    return buses_municipal

def process_xml_file(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for buses_municipal in root.iter('busesMunicipal'):
        if buses_municipal.text:
            routes = buses_municipal.text.split(',')
            buses_municipal.clear()
            buses_municipal.extend(convert_routes_to_xml(routes).findall('route'))

    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def convert_routes_to_xml(routes):
    buses_municipal = ET.Element("busesSeason")
    for route in routes:
        route_element = ET.SubElement(buses_municipal, "route")
        number_element = ET.SubElement(route_element, "number")
        number_element.text = route.strip()  # Удаляем лишние пробелы и добавляем номер маршрута
    return buses_municipal

def process_xml_file(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for buses_municipal in root.iter('busesSeason'):
        if buses_municipal.text:
            routes = buses_municipal.text.split(',')
            buses_municipal.clear()
            buses_municipal.extend(convert_routes_to_xml(routes).findall('route'))

    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def remove_spanish_titles(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for stop in root.iter('stop'):
        title_es = stop.find('titleEs')
        if title_es is not None:
            stop.remove(title_es)
        
        adjacent_street_es = stop.find('adjacentStreetEs')
        if adjacent_street_es is not None:
            stop.remove(adjacent_street_es)
        
        direction_es = stop.find('directionEs')
        if direction_es is not None:
            stop.remove(direction_es)

    tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Используйте путь к вашему XML файлу
input_file = 'stopsFullDB.xml'
output_file = 'modified_xml_file.xml'

process_xml_file('modified_xml_file.xml', output_file)
""" remove_spanish_titles('modified_xml_file.xml', output_file) """