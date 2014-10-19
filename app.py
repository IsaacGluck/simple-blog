import sqlite3
from flask import Flask, render_template, request, redirect, g

app = Flask(__name__)

##### DATABASE #####
DATABASE = "blog.db"

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

def new_post(title, post):
	cur = get_db().cursor()
	insert = "INSERT INTO posts (title, post) VALUES (" + title + ", " + post + ")"
	cur.execute(insert)
	conn.commit()

def new_comment(title, comment):
	cur = get_db().cursor()
	insert = "INSERT INTO comments (title, comments) VALUES (" + title + ", " + comment + ")"
	cur.execute(insert)
	conn.commit()

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
##### DATABASE #####
def make_url(title):
	return title.replace(" ", "_")
def make_title(url):
	return url.replace("_", " ")


@app.route("/")
@app.route("/index.html")
def index():
	titles = get_titles()
	links = [ [str("/title/" + make_url(i[0])), i[0]] for i in titles]
	return render_template("index.html", post_list=links)

@app.route("/title/<post_title>")
def title(post_title):
	title = make_title(post_title)
	post = get_post(title)
	comments = [str(i[0]) for i in get_comments(title)]
	print title, post, comments
	return render_template("title.html", title=title, post=post, comments=comments)

if __name__=="__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)