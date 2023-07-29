from app_fct_login import *
from app_fct_main import *
from flask import (Flask, abort, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from google_auth_oauthlib import flow

app = Flask(__name__)
app.secret_key=fct_hash_str()

fct_creare_DB()
GOOGLE_CLIENT_ID = '532617767739-j8vtdh7u78v2arb7od889s3nfu505bjo.apps.googleusercontent.com'



def login_is_required(funtion):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)
        else:
            return function()
    return wrapper


@app.route("/")
def home():
    posters = fct_all_titles()
    
    return render_template('index.html', choiced = posters)



@app.route("/loginpage")
def loginpage():
    return render_template('login.html')



@app.route("/signuppage")
def signuppage():
    return render_template('signup.html')



@app.route("/login", methods = ["POST"]) 
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    resp = fct_test(username, password)
    if resp == 1:
        flash('Username not found', 'error')
        return render_template('login.html')
    elif resp == 2:
        flash('Incorrect password', 'error')
        return render_template('login.html')
    elif resp == 3:
        return render_template('admin.html')
    elif resp == 7:
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
    elif resp == 8:
        return render_template('premium_sub.html')

@login_is_required
@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    if 'username' in session:
        username = session['username']
        movies = fct_all_titles()
        ids = [1123123, 2123123, 3, 4, 5, 6, 7]
        return render_template('main.html', movies = movies, ids = ids)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return 'You have been logged out.'


@app.route("/register", methods = ["POST"])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    resp = fct_test(username, email, password)
    if resp == 4:
        flash('Invalid username', 'error')
        return render_template('signup.html')
    elif resp == 5:
        flash('Email already in use', 'error')
        return render_template('signup.html')
    elif resp == 6:
        return render_template('success_signup.html')
    elif resp == 9:
        flash('Invalid email', 'error')
        return render_template('signup.html')
    elif resp == 10:
        flash('Invalid password', 'error')
        return render_template('signup.html')
    


@app.route("/forgetpass")
def forgetpass():   
    return render_template('forget_pass.html')



@app.route("/replacepass", methods = ['POST'])
def generatate_token():
    email = request.form.get('email')
    resp = fct_reset_password(email=email)
    if resp != -1:
        return render_template('succes_replace.html')
    elif resp == -1:
        flash('Invalid Email', 'error')
        return render_template('forget_pass.html')
    


@app.route("/replacepassdb", methods = ['POST'])
def replacepass():
    user_token = request.form.get('token')
    possw_user = request.form.get('password')
    repossw_user = request.form.get('repassword')
    if possw_user != repossw_user:
        flash('Passwords are difrent', 'error')
        return render_template('succes_replace.html')
    resp = fct_ver_token_change_pass(user_token, possw_user)
    if resp == 1:
        return render_template('swaped_pass.html')
    elif resp == -1:
        flash('Invalid token', 'error')
        return render_template('succes_replace.html')
    elif resp == 2:
        flash('Invalid password', 'error')
        return render_template('succes_replace.html')

@app.route("/verificare", methods = ['POST'])
def verifivare():
    actor = request.form.get('actor')
    selected_genre = request.form.get('genreSelect')
    selected_genre = selected_genre.title()

    username = session['username']
    print(username)
    print(actor)
    print(selected_genre)
    tuple = fct_retrive_movies(actor=actor, genre=selected_genre, user=username)
    l_img = fct_get_matched_movies_info(tuple)

    return render_template('rezultate_cautare_filme.html', l_img = l_img)

@app.route("/movie_details")
def movie_details():
    return render_template('movie_detail.html')

if __name__ == '__main__':
    app.run(debug=True)
