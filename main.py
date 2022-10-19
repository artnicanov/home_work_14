import sqlite3
import json

def main_sql_run(sql_query):
	""" в функции происходит подключение к БД """
	with sqlite3.connect('netflix.db') as connection:  # создаем coсоединение с базой данных
		connection.row_factory = sqlite3.Row  # доступ к результату запроса как к словарю, где ключ это имя столбца
		return connection.execute(sql_query).fetchall() # здесь выполнение запроса

# def main_sql_run(sql_query):
# 	""" в функции происходит подключение к БД """
# 	with sqlite3.connect('netflix.db') as connection: # соединение с базой данных
# 		coursor = connection.cursor() # механизм обработки результирующего набора select запроса
# 		return coursor.execute(sql_query).fetchall() # здесь выполнение запроса

def search_by_title(title):
# 	""" поиск по названию """
	sql_query = f"""
				SELECT title, country, release_year, listed_in, description
				FROM netflix
				WHERE title = '{title}'
				ORDER BY date_added DESC /* Если таких фильмов несколько, в результате буlет самый новый */
				LIMIT 1 /* ограничиваем вывод 1 результатом */
				"""
	result = None  # не определяем никакой тип для результата
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result = dict(row)  # результат приводим к типу словарь
	return result

def search_by_year_range(year1, year2):
	""" поиск по диапазону лет выпуска """
	sql_query = f"""
					SELECT title, release_year
					FROM netflix
					WHERE release_year BETWEEN {year1} AND {year2}
					ORDER BY release_year
					LIMIT 100  /* ограничиваем вывод 100 результатами */
				"""
	result = None  # определяем что результат это список
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result.append(dict(row))  # в список добавляем словарь
	return result

def search_by_rating(rating):
	""" поиск по рейтингу """
	rating_dict = {
		"children": ("G", "G"),  # если оставить в кортеже 1 элемент, то будет ошибка, поэтому просто дублируем
		"family": ("G", "PG", "PG-13"),
		"adult": ("R", "NC-17")
	}
	sql_query = f"""
					SELECT title, rating, description
					FROM netflix
					WHERE rating in {rating_dict[rating]}  /* находим нужный рейтинг - это один из ключей нашего словаря */ 
				"""
	result = []  # определяем что результат это список
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result.append(dict(row))  # в список добавляем словарь
	return result

def search_by_genre(genre):
	""" поиск по жанру """
	sql_query = f"""
					SELECT title, description
					FROM netflix
					WHERE listed_in LIKE '%{genre.lower()}%' /* находим нужный жанр игнорируя регистр */ 
					ORDER BY release_year DESC  /* сортируе по убыванию, чтобы показывались самые новые фильмы */ 
					LIMIT 10  /* ограничиваем вывод 10 результатами */
				"""
	result = []  # определяем что результат это список
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result.append(dict(row))  # в список добавляем словарь
	return result

def actors_check(actor1, actor2):
	""" получает в качестве аргумента имена двух актеров,
	сохраняет всех актеров из колонки cast и возвращает
	список тех, кто играет с ними в паре больше 2 раз """

	sql_query = f"""
					SELECT "cast"
					FROM netflix
					WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
				"""
	result = []  # определяем что результат это список
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result.append(dict(row))  # в список добавляем словарь
		name_dict = {}  # словарь с подсчетом сколько встречалось каждое имя
		for item in result:
			names = item.get("cast").split(", ")  # в список имен сохраняем значение каждого элемента по ключу cast
			for name in names:
				if name in name_dict.keys():
					name_dict[name] += 1  # если имя найдено среди ключей словаря, то добавляем единицу
				else:
					name_dict[name] = 1  # есkи нет, значит имя встретилось 1 раз, получаем словарь вида {'name': number}

			name_list = []  # список тех, кто играет в паре c переданными актерами больше 2 раз
			for name in name_dict:
				if name not in (actor1, actor2) and name_dict[name] > 2:
					name_list.append(name)
	return name_list

print(actors_check("Jack Black", "Dustin Hoffman"))


def search_by_type_year_genre(type, year, genre):
	""" поиск по тип картины (фильм или сериал), год выпуска и ее жанр """
	sql_query = f"""
					SELECT title, description
					FROM netflix
					WHERE type = '{type}'
					AND release_year = {year}
					AND listed_in LIKE '%{genre.lower()}%'
				"""
	result = []  # определяем что результат это список
	for row in main_sql_run(sql_query):  # обращаемся к функции с подключением к БД и перебираем результат запроса
		result.append(dict(row))  # в список добавляем словарь
	return json.dumps(result, indent=4)  # возвращаем результат в читабельном формате с отступом
