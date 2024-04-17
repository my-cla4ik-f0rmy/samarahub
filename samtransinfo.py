import requests
from bs4 import BeautifulSoup
import json

# URL страницы с таблицей
url = "http://www.samaratrans.info/wiki/index.php?title=Самара_автобус_маршруты"

# Получаем HTML-код страницы
response = requests.get(url)
html = response.text

# Инициализируем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html, "html.parser")

# Находим таблицу по классу "wide"
table = soup.find("table", class_="wide")

# Создаем список для хранения данных о маршрутах
routes_data = []

# Парсим строки таблицы
for row in table.find_all("tr")[1:]:  # пропускаем первую строку (шапку таблицы)
    columns = row.find_all("td")
    if len(columns) >= 4:  # проверяем, что в строке достаточно столбцов
        route_number = columns[0].text.strip()
        route_name = columns[1].text.strip()
        depot = columns[2].text.strip()
        schedule = columns[3].text.strip()
        route_info = {
            "number": route_number,
            "name": route_name,
            "depo": depot,
            "operation": schedule
        }
        routes_data.append(route_info)

# Сохраняем данные в файл JSON
with open("routesbus.json", "w", encoding="utf-8") as json_file:
    json.dump(routes_data, json_file, ensure_ascii=False, indent=4)

print("Данные сохранены в файл routes.json")
