import sqlite3
import random
import pprint
import cssutils
import numpy as np


DB_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\database\users.db'
def fct_retrive_movies(actor: str, genre: str, user: str, db = DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute("""--sql
    SELECT title FROM movies WHERE actors LIKE ? AND genres LIKE ?
    """, ('%' + actor + '%', '%' + genre + '%'))
    matched_movies = cur.fetchall()

    cur.execute("""--sql
    SELECT title FROM movies WHERE actors LIKE ?
    """, ('%' + actor + '%', ))
    actor_movies = cur.fetchall()

    cur.execute("""--sql
    SELECT title FROM movies WHERE genres LIKE ?
    """, ('%' + genre + '%', ))
    genre_movies = cur.fetchall()

    cur.execute("""--sql
    UPDATE users SET movies_genre = ? WHERE username = ? 
    """, (genre, user, ))
    con.commit()

    return matched_movies, actor_movies, genre_movies


def fct_get_matched_movies_info(t: tuple):

    # print(t[0])
    # print(t[1])
    # print(t[2][:5])
    
    list_best_fit = t[0]
    list_second_fit = t[1]
    list_random_movies = np.array(t[2])
    all_movies = []
    random_movies_l = []
    second_fit = []
    best_fit = []

    for item in list_best_fit:
        for movie in item:
            best_fit.append(movie)

    for item in list_best_fit:
        for movie in item:
            all_movies.append(movie)
    
    for item in list_second_fit:
        for movie in item:
            second_fit.append(movie)
    
    for item in list_random_movies:
        for movie in item:
            random_movies_l.append(movie)
    
    for elem in second_fit:
        if elem in best_fit:
            continue
        else:
            all_movies.append(elem)
    

    # print(all_movies)

    choiced_movies = random.choices(random_movies_l, k = 20)
    # print(choiced_movies)
    all_movies = all_movies + choiced_movies
    # print(all_movies)
    posters = []
    for movie in all_movies:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute("""--sql
SELECT poster FROM movies WHERE title = ?
""", (movie, ))
        poster = cur.fetchall()
        for elem in poster:
            for movie in elem:
                posters.append(movie)
    print(posters)
    return posters 


def fct_all_titles():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""--sql
SELECT title FROM movies        
""")
    all_titles_t = cur.fetchall()
    all_titles = []
    for elem in all_titles_t:
        for movie in elem:
            all_titles.append(movie)
    
    choiced = random.choices(all_titles, k = 20)
    all_posters_t = []
    posters = []

    for movie in choiced:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute("""--sql
SELECT poster FROM movies WHERE title = ?
""", (movie, ))
        poster = cur.fetchall()
        all_posters_t.append(poster)
    # print(all_posters_t)
    for list in all_posters_t:
        for tuple in list:
            for movie in tuple:
                posters.append(movie)
    # print(posters)
    
    return posters

if __name__ == "__main__":
    print('main')
    # con = sqlite3.connect(DB_PATH)
    # cur = con.cursor()
    # cur.execute("""--sql
    # SELECT actors FROM movies WHERE title = ?
    # """, ('Breaking Bad', ))
    # print(cur.fetchall())
    # tup = fct_retrive_movies('aaron paul', 'drama', 'u')
    # dict1 = fct_get_matched_movies_info(tup)
    # for key in dict1.keys():
    #     print(dict1[key])
    # import numpy as np
    
    # arr = np.array((1, 2, 3, 4, 5))

    # print(arr[0])
    fct_all_titles()

    