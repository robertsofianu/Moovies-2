from email.message import EmailMessage
from threading import Thread
from cryptography.fernet import Fernet
import smtplib
import sqlite3
import hashlib
import random
import ssl
import re



DB_PATH = r'C:\Users\rober\OneDrive\Desktop\Programming\_movies_unboxing\database\users.db'
RE = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+$'
regex = re.compile(RE)


def fct_creare_DB(db = DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """--sql
        CREATE TABLE if not exists users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL,
            status TEXT,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            token_reset_pass VARCHAR(255) NOT NULL,
            fav_artist VARCHAR(255) NOT NULL,
            movies_genre VARCHAR(255) NOT NULL
        )
        """
    )
    con.commit()

def fct_sent_mail(rec_email: str, token: str, user: str):
    email_sender = 'listofmovie.robert@gmail.com'
    email_password = 'ynmzzzoavfmwpdmr'
    email_receiver = rec_email
    subject = 'Your Recovery Token'
    body = f"""
    Dear user, {user}

    We heared that you lost your password, here it is the recovery token, use it wisely:

    \t{token}
    """
    body = body.strip()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def fct_hash_str(p = 'ana are mere'):
    p = hashlib.sha256(p.encode()).hexdigest()
    return p

def fct_test(*kargs):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    #FOR LOG IN if len kargs == 2 we verify if the users exists and if passwords matches
    if len(kargs) == 2:
        username1 = kargs[0]
        username1 = username1.strip()
        username1 = username1.lower()
        password1 = fct_hash_str(kargs[1])

        cur.execute(
        """--sql
        SELECT * FROM users WHERE username = ?
        """, (username1,))
        con.commit()
        exist_user = cur.fetchone()

        cur.execute("""--sql
        SELECT password FROM users WHERE username = ?
        """, (username1, ))
        con.commit()
        exist_pass = cur.fetchone()

        cur.execute("""--sql
        SELECT status FROM users WHERE username = ?
        """, (username1, ))
        status = cur.fetchone()
        con.commit()


        if not exist_user:
            return 1 # user not found
        elif exist_pass[0] != password1:
            return 2 # password dont match
        if status[0] == 'admin':
            return 3 # loads admin page
        elif status[0] == 'freesub':
            return 7 # loads freesub page
        elif status[0] == 'premiumsub':
            return 8 # loads premium sub   
    
    #FOR SIGN UP if len kargs == 3, we verify if user already exists and if not we insert them in db 
    elif len(kargs) == 3:
        username = kargs[0]
        username = username.strip()
        username = username.lower()
        email = kargs[1]
        passw = kargs[2]


        resp_username = fct_username_validator(username)
        if resp_username:
            return 4

        resp_passw = fct_ver_pass(passw)
        if not resp_passw:
            return 10

        password = fct_hash_str(passw)

        result = regex.match(email)
        if not result:
            return 9 # invalid email

        cur.execute(
        """--sql
        SELECT * FROM users WHERE username = ?
        """, (username, ))
        existing_username = cur.fetchone()
        if existing_username:
            return 4 # invalid username
        


        cur.execute(
        """--sql
        SELECT * FROM users WHERE email = ?
        """, (email, ))
        exist_email = cur.fetchone()
        if exist_email:
            return 5 # email already in use

        cur.execute(
        """--sql
        INSERT INTO users (username, email, password, token_reset_pass, fav_artist, movies_genre, profile_picture) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, email, password, '', '', '', '../static/imgs/poster_unknown/unknown_poster.png'))
        con.commit()
        if email == 'robertsofianu@gmail.com':
            cur.execute("""--sql
            UPDATE users SET status = ? WHERE email = ?
            """, ('admin', 'robertsofianu@gmail.com'))
            con.commit()
        else:
            cur.execute("""--sql
            UPDATE users SET status = ? WHERE email = ?
            """, ('freesub', email, ))
            con.commit()

        return 6 # insert username, email and password

def fct_reset_password(email: str, db= DB_PATH):
    result = regex.match(email)

    con = sqlite3.connect(db)
    cur = con.cursor()

    create_token = lambda a, b: fct_hash_str(a + b)
    n1 = str(random.choice(range(10000)))
    n2 = random.choice(range(256))  
    n2 = chr(n2)
    token = create_token(n1, n2) # this token will be sent on email to reset the password

    cur.execute(
    """--sql
    SELECT * FROM users WHERE email = ?
    """, (email, ))
    exist_mail = cur.fetchone()
    if email == '' or not result:
        return -1
    elif exist_mail:
        id = exist_mail[0]
        username = exist_mail[1]
        emai2 = exist_mail[3]
        cur.execute("""--sql
        UPDATE users SET token_reset_pass = ? WHERE id = ?
        """, (token, id, ))
        con.commit()

        cur.execute("""--sql
        SELECT token_reset_pass FROM users WHERE id = ?
        """, (id, ))
        token = cur.fetchone()[0]
        # thread runs the sent email funtion in the backgorund for time eficiency
        t = Thread(target=fct_sent_mail, args=(emai2, token, username))
        t.start()

        return exist_mail # 1 means that the recovery email has been semt
    return -1 # -1 means that the email was not found it the db 



def fct_ver_token_change_pass(token_user: str, passwd: str, db = DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()
    passw = passwd

    resp_pass = fct_ver_pass(passw)

    if not resp_pass:
        return 2

    password = fct_hash_str(passw)
    cur.execute("""--sql
    SELECT username FROM users WHERE token_reset_pass = ?
    """, (token_user, ))
    con.commit()
    user_token = cur.fetchone()
    print(user_token)
    if token_user == '':
        return -1 # invalid token error
    if user_token:
        user_token = user_token[0]
        cur.execute("""--sql
        UPDATE users SET password = ? WHERE username = ?
        """, (password, user_token, ))
        con.commit()
        return 1 # sucess 
    return -1 # fail


def fct_ver_pass(password: str):
    specialchar = '1234567890[](){}";:/?.,<>!@#$%^&*'
    upper_case = 'QWERTYUIOPASDFGHJKLZXCVBNM'

    has_len = False
    has_sp_char = False
    has_one_upper_case = False

    if len(password) >= 8:
        has_len = True
    for spchr in specialchar:
        if spchr in password:
            has_sp_char = True
    
    for upper in upper_case:
        if upper in password:
            has_one_upper_case = True
    
    if has_len and has_sp_char and has_one_upper_case:
        return True
    else:
        return False

def fct_username_validator(username: str):
    bad_words = ['duck', 'dog']
    status = False
    for bad_word in bad_words:
        if bad_word in username:
            status = True
    return status

def fct_crypting_str(str1: str):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    enMessage = fernet.encrypt(str1.encode())
    return enMessage, fernet

def fct_decript_str(enMes_key: tuple):
    enMes = enMes_key[0]
    key = enMes_key[1]
    decMes = key.decrypt(enMes).decode()
    return decMes    


if __name__ == '__main__':
    from threading import Thread
    import time
    from cryptography.fernet import Fernet

    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+$'
    regex = re.compile(email_pattern)

    email1 = 'robert@gmail.org'
    

    email2 = 'a@a.a'
    result = regex.match(email1)

    message = 'this is a nonencripted mesage'

    key = Fernet.generate_key()
    fernet = Fernet(key)

    enMessage = fernet.encrypt(message.encode())

    # print('original string: ', message)
    # print('encripted string: ', enMessage)

    decMess = fernet.decrypt(enMessage).decode()

    # print('decripted string: ', decMess)

    def enc(mes: str):
        message = mes
        key = Fernet.generate_key()
        fernet = Fernet(key)

        enMessage = fernet.encrypt(message.encode())
        return enMessage, fernet
    
    def dec(mes_key: tuple):
        enMes = mes_key[0]
        key = mes_key[1]
        decMes = key.decrypt(enMes).decode()
        
        return decMes

    encmes = enc('ana are mere')
    print(dec(encmes))    
    passw = 'ana are mere     '
    passw2 = passw.strip()
    print(len(passw), len(passw2))
