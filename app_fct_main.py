import sqlite3
import random
import pprint

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
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    dict_all_movies = {}

    matched_movies = t[0]
    actors_movies = t[1]
    genre_movies = t[2]
    
    list_matched_movies = []
    for t in matched_movies:
        for content in t:
            list_matched_movies.append(content)
    
    list_actors_movies = []
    for t in actors_movies:
        for content in t:
            list_actors_movies.append(content)

    list_genre_movies = []
    for t in genre_movies:
        for content in t:
            list_genre_movies.append(content)
    
    movie_genre_sorted = random.choices(list_genre_movies, k = 10)


    dict_matched_movies = {}
    
    for t in matched_movies:
        if matched_movies:
            for movie in t:
                dict_details = {}
                dict_matched_movies[movie] = dict_details

                cur.execute('SELECT poster FROM movies WHERE title = ?', (movie,))
                poster = cur.fetchall()

                for t in poster:
                    for content in t:
                        dict_details['Poster'] = content

                cur.execute('SELECT ratings FROM movies WHERE title = ?', (movie,))
                ratings = cur.fetchall()

                for t in ratings:
                    for content in t:
                        dict_details['Ratings'] = content
                
                cur.execute('SELECT year FROM movies WHERE title = ?', (movie,))
                year = cur.fetchall()

                for t in year:
                    for content in t:
                        if '–' in content:
                            spit = content.split('–')
                            # print(spit)
                            dict_details['Year'] = spit[0]
                        else:    
                            dict_details['Year'] = content
    
    sorted_data = sorted(dict_matched_movies.items(), key=lambda x: (-int(x[1]['Ratings'][:-1])))
    sorted_dict = dict(sorted_data)
                
    dict_all_movies['Priority 1'] = sorted_dict



    for movie1 in list_matched_movies:
        for index, movie2 in enumerate(list_actors_movies):
            if movie1 == movie2:
                list_actors_movies.pop(index)

    dict_actor = {}

    list_actors_movies = set(list_actors_movies)

    for movie in list_actors_movies:
        dict_details2 = {}
        dict_actor[movie] = dict_details2


        cur.execute('SELECT poster FROM movies WHERE title = ?', (movie,))
        poster = cur.fetchall()

        for t in poster:
            for content in t:
                dict_details2['Poster'] = content

        cur.execute('SELECT ratings FROM movies WHERE title = ?', (movie,))
        ratings = cur.fetchall()

        for t in ratings:
            for content in t:
                dict_details2['Ratings'] = content


    sorted_data2 = sorted(dict_actor.items(), key=lambda x: (-int(x[1]['Ratings'][:-1])))
    sorted_dict2 = dict(sorted_data2)

    dict_all_movies['Priority 2'] = sorted_dict2


    dict_genre = {}

    for movie in movie_genre_sorted:
        dict_details3 = {}    
        dict_genre[movie] = dict_details3

        cur.execute('SELECT poster FROM movies WHERE title = ?', (movie,))
        poster = cur.fetchall()

        for t in poster:
            for content in t:
                dict_details3['Poster'] = content

        cur.execute('SELECT ratings FROM movies WHERE title = ?', (movie,))
        ratings = cur.fetchall()

        for t in ratings:
            for content in t:
                dict_details3['Ratings'] = content
    
    dict_all_movies['Priority 3'] = dict_genre

    # pprint.pprint(dict_all_movies)

    return dict_all_movies


if __name__ == "__main__":
    print('main')
    # con = sqlite3.connect(DB_PATH)
    # cur = con.cursor()
    # cur.execute("""--sql
    # SELECT actors FROM movies WHERE title = ?
    # """, ('Breaking Bad', ))
    # print(cur.fetchall())
    tup = fct_retrive_movies('aaron paul', 'drama', 'u')
    dict1 = fct_get_matched_movies_info(tup)
    # for key in dict1.keys():
    #     print(dict1[key])

    