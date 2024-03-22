import xml.etree.ElementTree as ET
import html

# Декодирование HTML
# Загрузить XML файл
tree = ET.parse('stopsFullDB.xml')
root = tree.getroot()

""" # Итерироваться по всем элементам 'title' и заменить текст, если он начинается с 'ул. '
for title in root.iter('title'):
    if title.text.startswith('ул. '):
        title.text = title.text.replace('ул. ', 'Улица ').strip()

for title in root.iter('title'):
    if title.text.startswith('пос. '):
        title.text = title.text.replace('пос. ', 'Посёлок ').strip()

for cluster in root.findall('.//cluster '):
    cluster.clear()  # очищаем содержимое
    root.remove(cluster)  # """



# Функция для переформатирования номеров маршрутов
# Функция для переформатирования номеров маршрутов
def reformat_routes(routes_str):
    if routes_str is None:
        return ''
    routes = routes_str.split(', ')
    formatted_routes = []
    for route in routes:
        formatted_routes.append(f'<route><number>{route}</number></route>')
    return '\n'.join(formatted_routes)


# Найти и изменить теги <busesMunicipal>
for busesMunicipal in root.iter('busesMunicipal'):
    routes_str = busesMunicipal.text
    formatted_routes = reformat_routes(routes_str)
    busesMunicipal.clear()
    busesMunicipal.text = html.unescape(formatted_routes)


# Сохранить изменения в XML файл
tree.write('modified_xml_file.xml', encoding='utf-8', xml_declaration=True)
