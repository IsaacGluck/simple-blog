import sqlite3
from flask import Flask, render_template, request, redirect, g, session, escape, url_for

app = Flask(__name__)

##### \/DATABASE\/ #####

DATABASE = "blog.db"

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_blog', None)
    if db is None:
        db = g._database = sqlite3.connect("blog.db")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def new_post(title, post, username):
        conn = get_db()
        cur = conn.cursor()
        insert = "INSERT INTO posts VALUES (" + "\'" + title + "\'" + ", " + "\'" + post + "\'" + "," + "\'" + username + "\'" + ")"
        cur.execute(insert)
        conn.commit()
        conn.close()

def new_comment(title, comment, username):
        conn = get_db()
        cur = conn.cursor()
        insert = "INSERT INTO comments VALUES (" + "\'" + title + "\'" + ", " + "\'" + comment + "\'" + "," + "\'" + username + "\'" + ")"
        cur.execute(insert)
        conn.commit()
        conn.close()

def new_user(username,password):
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT username FROM users WHERE username = \'" + username + "\'"
    cur.execute(query)
    post = cur.fetchall()
    if len(post) != 0:
        return False
    else:
        insert = "INSERT INTO users VALUES (" + "\'" + username + "\'" + ", " + "\'" + password + "\'" + ")"
        cur.execute(insert)
        conn.commit()
        conn.close()
        return True

def get_titles():
        cur = get_db().cursor()
        query = "SELECT title FROM posts"
        cur.execute(query)
        titles = cur.fetchall()
        return titles

def get_comments(title):
        cur = get_db().cursor()
        query = "SELECT comment from comments WHERE title = \'" + title + "\'"
        cur.execute(query)
        comments = cur.fetchall()
        return comments

def get_post(title):
        cur = get_db().cursor()
        query = "SELECT post FROM posts WHERE title = \'" + title + "\'"
        cur.execute(query)
        post = cur.fetchall()
        return post[0][0]

def check_user(username, password):
        cur = get_db().cursor()
        query = "SELECT username FROM users WHERE password = \'" + password + "\'" + "AND username = \'" + username + "\'"
        cur.execute(query)
        post = cur.fetchall()
        if len(post) >= 1:
            return True
        else:
            return False
##### /\DATABASE/\ #####    

# URL spaces workaround                                                                                                                                                                                                                                                      \
\                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                             \

def make_url(title):
        return title.replace(" ", "_")
def make_title(url):
        return url.replace("_", " ")

# Page routes                                                                                                                                                                                                                                                                \
                                                                                                                                                                                                                                                                              

@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username,password):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success = new_user(username,password)
        print success
        if success:
            return redirect(url_for('register_successful'))
        else:
            return redirect(url_for('register_fail'))
    return render_template("register.html")

@app.route("/register_successful")
def register_successful():
    return render_template("register_1.html")
@app.route("/register_fail")
def register_fail():
    return render_template("register_0.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/index", methods=["GET","POST"])
def index():
    if request.method == "GET":
        # If the form is not being used, just display the page                                                                                                                                                                                                               \
\                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                             \

        titles = get_titles()
        links = [ [ str("/title/" + make_url(i[0])), i[0] ] for i in titles]
        return render_template("index.html", post_list=links)
    elif 'username' in session:
        title = request.form["new_title"]
        post = request.form["new_post"]
        new_post(title, post, escape(session['username'])) # put the new post into the database                                                                                                                                                                              \
\                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                             \

        titles = get_titles()
        links = [ [str("/title/" + make_url(i[0])), i[0]] for i in titles]
        return render_template("index.html", post_list=links)
    else:
        return 'You are not logged in'



@app.route("/title/<post_title>", methods=["GET","POST"])
def title(post_title):
        if request.method == "GET":
                title = make_title(post_title)
                post = get_post(title)
                comments = [str(i[0]) for i in get_comments(title)]
                return render_template("title.html", title=title, post=post, comments=comments)
        elif 'username' in session:
            title = make_title(post_title)
            comment = request.form["comment"]
            new_comment(title, comment, escape(session['username']))
            post = get_post(title)
            comments = [str(i[0]) for i in get_comments(title)]
            return render_template("title.html", title=title, post=post, comments=comments)
        else:
            return 'You are not logged in'


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RRR'

if __name__=="__main__":
        #app.run(host='0.0.0.0', port=8080, debug=True)                                                                                                                                                                                                                      \
\                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                             \

        app.run(debug=True)
