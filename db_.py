import sqlite3
import time
import requests
import json
import pyautogui

DB_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\database\users.db'
TXT_MOVIES_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\txt_files\all_movies.txt'
JSON_ACTOS_PATH = r'_movies_unboxing\json\actors.json'

with open(TXT_MOVIES_PATH, encoding='UTF-8') as f:
    txt_all_movies = f.readlines()

omdb_api_key = '46316a75'
omdb_base_url = 'http://www.omdbapi.com/'

tmdb_api_key = '6260806ec1b9203c07358f07483be1bb'
tmdb_base_url = 'https://api.themoviedb.org/3'


def fct_omdb_movie_details(movie_title) -> dict:
    url = f"{omdb_base_url}?apikey={omdb_api_key}&t={movie_title}&plot=full"
    response = requests.get(url)
    data = response.json()
    return data # data is the dict that has all the info about a certain movie


    

def fct_creare_DB_notmain(nr :int, db = DB_PATH):
    if nr == 1:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute(
            """--sql
            CREATE TABLE if not exists movies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year TEXT,
                release TEXT,
                runtime TEXT,
                genres TEXT,
                director TEXT,
                writers TEXT,
                actors TEXT,
                plot TEXT,
                languages TEXT,
                poster TEXT,
                ratings TEXT,
                type TEXT,
                seasons TEXT,
                filelist_path TEXT
            )
            """
        )
        con.commit()

    elif nr == 2:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute(
            """--sql
            CREATE TABLE if not exists actors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                p_photo TEXT
            )
            """
        )
        con.commit()


def fct_insert(l: list, db = DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()

    for movie in l:
        movie : str
        movie = movie.strip()
        dict_details = fct_omdb_movie_details(movie)
        response = dict_details['Response']
        if response == 'True':           
            title = dict_details['Title']
            year = dict_details['Year']
            release = dict_details['Released']
            runtime = dict_details['Runtime']
            genres = dict_details['Genre']
            director = dict_details['Director']
            writers = dict_details['Writer']
            actrors = dict_details['Actors']
            plot = dict_details['Plot']
            languages = dict_details['Language']
            poster = dict_details['Poster']

            rating = dict_details['Ratings']
            ratings = []
            for ra in rating:
                    ratings.append(ra['Value'])
            ratings = ', '.join(ratings)

            typo = dict_details['Type']

            try:
                seasons = dict_details['totalSeasons']
            except KeyError:
                seasons = 'NULL'
            
        cur.execute("""--sql
        INSERT INTO movies (title, year, release, runtime, genres, director, writers, actors, plot, languages, poster, ratings, type, seasons) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, year, release, runtime, genres, director, writers, actrors, plot, languages, poster, ratings, typo, seasons))
        con.commit()
        # else:
        #     continue



def fct_delete_table(table_name: str, db = DB_PATH):
    import sqlite3

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()



def fct_resolve(l: list, db = DB_PATH):
    filme_negasite = 0
    total_filme = 0
    for movie in l:
        total_filme += 1
        movie : str
        movie = movie.strip()
        dict_details = fct_omdb_movie_details(movie)
        response = dict_details['Response']
        if response == 'True':           
            continue
        else:
            filme_negasite += 1
        print(f'Total filme: {total_filme} | Filme negasite: {filme_negasite}', end='\r ')
    return filme_negasite




def fct_select_movies():
    con = sqlite3.connect(database=DB_PATH)
    cur = con.cursor()

    actors = 'Chris Pratt'
    genre = "Adventure"

    cur.execute(f"""--sql
    SELECT title FROM movies WHERE actors LIKE ? AND genres LIKE ? 
    """, ('%' + actors + '%', '%' + genre + '%'))
    movies = cur.fetchall()
    con.close()
    print(movies)



def fct_select_all_tieles():
    con = sqlite3.connect(database=DB_PATH)
    cur = con.cursor()

    cur.execute(f"""--sql
    SELECT title FROM movies 
    """)
    movies = cur.fetchall()
    print(movies)



def fct_list_actori(db = DB_PATH):
    all_actors = set()
    con = sqlite3.connect(db)   
    cur = con.cursor()

    cur.execute('SELECT actors FROM movies')
    actors_all = cur.fetchall()
    for tuple in actors_all:
        for actor in tuple:
            a = actor.split(', ')
            for ac in a:
                all_actors.add(ac)
    actors = list(all_actors)

    return actors

def fct_actor_info_search(actor: str):
    formatted_actor_name = actor.replace(" ", "%20")
    url = f"https://api.themoviedb.org/3/search/person?api_key={tmdb_api_key}&query={formatted_actor_name}"
    response = requests.get(url)
    data = response.json()
    return data


def fct_inserare_act_(s: set, db=DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()
    for actor in s:
        try:
            d = fct_actor_info_search(actor)

            url = 'https://image.tmdb.org/t/p/'
            nume = actor
            response = d['results']
            response = response[0]
            p_photo_link = response['profile_path']
            size = 'w500'

            if p_photo_link == None:
                p_photo = 'NONE'
            else:
                p_photo = f'{url}{size}{p_photo_link}'
                

            cur.execute("""--sql
            INSERT INTO actors (name, p_photo) VALUES (?, ?)
            """, (nume, p_photo))
            con.commit()
        except IndexError:
            nume = actor
            p_photo = 'NONE'
            cur.execute("""--sql
            INSERT INTO actors (name, p_photo) VALUES (?, ?)
            """, (nume, p_photo))
            con.commit()


def fct_select_NONE(db = DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT name FROM actors WHERE p_photo = ?', ('https://upload.wikimedia.org/wikipedia/commons/e/ee/Unknown-person.gif', ))
    none_actors = cur.fetchall()
    return none_actors

def fct_update_DB_unknown_actors(l: list, db = DB_PATH):

    con = sqlite3.connect(db)
    cur = con.cursor()

    unknown_photo = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\static\imgs\unknownperson\Unknown-person.png'
    for tuple in l:
        for actor in tuple:
            cur.execute('UPDATE actors SET p_photo = ? WHERE name = ?', (unknown_photo, actor,))
            con.commit()
            
def fct_scrie_lista_js(l: list):
    time.sleep(4)
    for acotor in l:
        if acotor == 'N/A':
            continue
        else:
            pyautogui.press("`")
            pyautogui.write(acotor)
            pyautogui.press('right')
            pyautogui.press(',')
            pyautogui.press('enter')


def fct_update_score(l: list):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for movie in l:
        movie = movie.strip()
        first_score = 0
        second_score = 0
        third_score = 0
        final_score = 0
        ratings = []
        error = 0

        data = fct_omdb_movie_details(movie)
        try:        
            l_ratings = data['Ratings']
            for elem in l_ratings:
                raiting1 = elem["Value"]
                ratings.append(raiting1)
            
            for rat in ratings:
                if '/' in rat:
                    numere = rat.split('/')
                    if numere[1] == '10':
                        first_score = int(float(numere[0]) * 10)
                    if numere[1] == '100':
                        second_score = int(numere[0])
                elif '%' in rat:
                    third_score = int(rat.strip('%'))
            if ratings:
                final_score = (first_score + second_score + third_score) / len(ratings)
            
            rating_final = f'{int(final_score)}%'

            cur.execute("""--sql
            UPDATE movies SET ratings = ? WHERE title = ?
            """, (rating_final, movie, ))
            con.commit()

        except KeyError:
            error += 1 
            print(f'error: {error}', end='\r')
            continue


def fct_selecteaza_filme():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""--sql
    SELECT title FROM movies
    """)
    movies = cur.fetchall()
    all_movies_in_db = []
    for tuple in movies:
        for movie in tuple:
            all_movies_in_db.append(movie)
    return all_movies_in_db


def fct_ver_movies(l: list):
    movie_unfound = 0
    filme_negasite = []
    filme_gasite = 0
    total_filme = 0
    for movie in l:
        movie : str
        movie = movie.strip()
        data = fct_omdb_movie_details(movie)
        response = data['Response']
        total_filme += 1
        if response == 'True':
            # print(f'film gasit: {movie}')
            filme_gasite += 1
            continue
        else:
            movie_unfound += 1
            print(f'filme negasite: {movie_unfound} | filme gasite: {filme_gasite} | total filme: {total_filme}', end='\r')
            filme_negasite.append(movie)
        if movie_unfound == 200:
            break
    print('\n')
    print(filme_negasite)



if __name__ == '__main__':
    print()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # cur.execute("""--sql
    # SELECT actors FROM movies WHERE title = ?
    # """, ('El Camino: A Breaking Bad Movie',))
    # print(cur.fetchall())
    # fct_ver_movies(txt_all_movies)
    # print(fct_omdb_movie_details('Emmanuelle: Queen of Sados'))
    # print(fct_omdb_movie_details('EL camino: A breaking bad movie'))
    # fct_creare_DB_notmain(1)
    # fct_insert(txt_all_movies)
    # fct_delete_table('movies')
    fct_update_score(txt_all_movies)
    # cur.execute("""--sql
    # SELECT ratings FROM movies WHERE title = ?
    # """, ('Goodfellas', ))
    # rat = str(cur.fetchall())
    # print(rat)
    # cur.execute("""--sql
    # UPDATE movies SET ratings = ? WHERE title = ?
    # """, (rat, 'Goodfellas',))
    # con.commit()