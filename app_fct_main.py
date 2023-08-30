import hashlib
import json
import pprint
import random
import sqlite3

import cssutils
import numpy as np

DB_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\database\users.db'


def fct_retrive_movies(actor: str, genre: str, user: str, db=DB_PATH):
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

    choiced_movies = random.choices(random_movies_l, k=20)
    # print(choiced_movies)
    all_movies = all_movies + choiced_movies
    # print(all_movies)
    ids = []
    for movie in all_movies:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""--sql
        SELECT id FROM movies WHERE title = ?
        """, (movie, ))
        ides = cur.fetchall()

        for t in ides:
            for id in t:
                ids.append(id)

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
    return posters, ids


def fct_is_valid_credit_card(card_number):

    card_number = ''.join(filter(str.isdigit, card_number))

    doubled_digits = []
    for i in range(len(card_number) - 2, -1, -2):
        doubled_digit = int(card_number[i]) * 2
        if doubled_digit > 9:
            doubled_digit -= 9
        doubled_digits.append(doubled_digit)

    total_sum = sum(doubled_digits) + sum(int(digit)
                                          for digit in card_number[-1::-2])

    val = total_sum % 10 == 0
    resp = 0  # invalid card

    if val:
        resp = 1  # valid card
    if not card_number.isdigit():
        resp = 0
    print(resp)
    return resp


def fct_paymanet_info_validation(user, c_n, c_h, m, y, cvv: str):
    response = ''
    validation_cn = fct_is_valid_credit_card(c_n)
    val = True
    if validation_cn == 0:
        val = False
        response = -1  # INVALID CARD NUMBER
    elif c_h == '' or c_h == None:
        val = False
        response = 1  # INVALID CREDITALS
    elif m == '' or m == None:
        val = False
        response = 1  # INVALID CREDITALS
    elif y == '' or y == None:
        val = False
        response = 1  # INVALID CREDITALS
    elif cvv == '' or cvv == None or not cvv.isdigit():
        val = False
        response = 1  # INVALID CREDITALS

    if val:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        c_n = hashlib.sha256(c_n.encode()).hexdigest()
        c_h = hashlib.sha256(c_h.encode()).hexdigest()
        m = hashlib.sha256(m.encode()).hexdigest()
        y = hashlib.sha256(y.encode()).hexdigest()
        cvv = hashlib.sha256(cvv.encode()).hexdigest()

        cur.execute("""--sql
        UPDATE users SET card_number = ? WHERE username = ?
        """, (c_n, user, ))
        con.commit()

        cur.execute("""--sql
        UPDATE users SET card_holder = ? WHERE username = ?
        """, (c_h, user, ))
        con.commit()

        cur.execute("""--sql
        UPDATE users SET exp_month = ? WHERE username = ?
        """, (m, user, ))
        con.commit()

        cur.execute("""--sql
        UPDATE users SET exp_year = ? WHERE username = ?
        """, (y, user, ))
        con.commit()

        cur.execute("""--sql
        UPDATE users SET cvv = ? WHERE username = ?
        """, (cvv, user, ))
        con.commit()

        cur.execute("""--sql
        UPDATE users SET status = ? WHERE username = ?
        """, ('premiumsub', user, ))
        con.commit()

        response = 0  # VALID DATA

    return response


def fct_all_titles2():
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

    choiced = random.choices(all_titles, k=20)
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

    choiced = random.choices(all_titles, k=20)
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

    ids = []

    for poster in posters:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""--sql
        SELECT id FROM movies WHERE poster = ?
        """, (poster, ))
        id = cur.fetchall()
        for t in id:
            for ides in t:
                ids.append(ides)
    return posters, ids


def fct_return_json_contect():
    JSON_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\static\api.json'
    with open(JSON_PATH, 'r') as file:
        data = json.load(file)
    return data[-1]


def fct_get_inf(id: int):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""--sql
    SELECT poster FROM movies WHERE id = ?
    """, (id, ))
    p1 = cur.fetchall()
    for t in p1:
        for poster in t:
            p1 = poster

    cur.execute("""--sql
    SELECT title FROM movies WHERE id = ?
    """, (id, ))
    title = cur.fetchall()
    for t in title:
        for poster in t:
            title = poster

    cur.execute("""--sql
    SELECT plot FROM movies WHERE id = ?
    """, (id, ))
    desp = cur.fetchall()
    for t in desp:
        for poster in t:
            desp = poster

    cur.execute("""--sql
    SELECT year FROM movies WHERE id = ?
    """, (id, ))
    year = cur.fetchall()
    for t in year:
        for poster in t:
            year = poster

    cur.execute("""--sql
    SELECT release FROM movies WHERE id = ?
    """, (id, ))
    release = cur.fetchall()
    for t in release:
        for poster in t:
            release = poster

    cur.execute("""--sql
    SELECT runtime FROM movies WHERE id = ?
    """, (id, ))
    runtime = cur.fetchall()
    for t in runtime:
        for poster in t:
            runtime = poster

    cur.execute("""--sql
    SELECT genres FROM movies WHERE id = ?
    """, (id, ))
    genres = cur.fetchall()
    for t in genres:
        for poster in t:
            genres = poster

    cur.execute("""--sql
    SELECT director FROM movies WHERE id = ?
    """, (id, ))
    director = cur.fetchall()
    for t in director:
        for poster in t:
            director = poster

    cur.execute("""--sql
    SELECT writers FROM movies WHERE id = ?
    """, (id, ))
    writers = cur.fetchall()
    for t in writers:
        for poster in t:
            writers = poster

    cur.execute("""--sql
    SELECT actors FROM movies WHERE id = ?
    """, (id, ))
    actors = cur.fetchall()
    for t in actors:
        for poster in t:
            actors = poster

    cur.execute("""--sql
    SELECT ratings FROM movies WHERE id = ?
    """, (id, ))
    ratings = cur.fetchall()
    for t in ratings:
        for poster in t:
            ratings = poster

    return p1, title, desp, year, release, runtime, genres, director, writers, actors, ratings


def fct_get_actors_posters(actors: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    actors = actors.split(',')
    posters = []
    for actor in actors:
        cur.execute("""--sql
        SELECT p_photo FROM actors WHERE name = ?
        """, (actor, ))
        actor = cur.fetchall()
        for t in actor:
            for ac in t:
                posters.append(ac)
    return posters


if __name__ == "__main__":
    act = 'Matt Damon, Tian Jing, Willem Dafoe'
    print('main')
    a = fct_retrive_movies('Aaron Paul', 'Drama', '')
    fct_get_matched_movies_info(a)
