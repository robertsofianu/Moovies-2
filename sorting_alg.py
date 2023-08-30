import sqlite3

import requests

from db_ import fct_omdb_movie_details

TXT_FILE_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\txt_files\all_movies.txt'
DB_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\database\users.db'


tmdb_api_key = '6260806ec1b9203c07358f07483be1bb'
tmdb_base_url = 'https://api.themoviedb.org/3'


def fct_get_all_movies():
    page = 1
    all_mov = set()
    while True:
        try:
            url = f"{tmdb_base_url}/discover/movie?api_key={tmdb_api_key}&sort_by=popularity.desc&page={page}"
            response = requests.get(url)
            data = response.json()

            for movie in data['results']:
                title = movie['title']
                # print(title, end='\r')
                all_mov.add(title)

            page += 1
        except KeyError:
            break

    with open(TXT_FILE_PATH, 'w', encoding='utf-8') as f:
        for title in all_mov:
            data = fct_omdb_movie_details(title)
            resp = data['Response']
            if resp == "True":
                f.write(f'{title}\n')
            else:
                continue
    return data


def fct_get_all_genres(db=DB_PATH):
    all_genres = set()
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT genres FROM movies')
    all_genre = cur.fetchall()
    for tuple in all_genre[:20]:
        for t in tuple:
            t = t.split(', ')
            for genre in t:
                all_genres.add(genre)

    print(all_genres)


# fct_get_all_genres()
fct_get_all_movies()
