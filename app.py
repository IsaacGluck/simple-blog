import sqlite3
from flask import Flask, render_template, request, redirect, g

app = Flask(__name__)

##### \/DATABASE\/ #####
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
	conn = get_db()
	cur = conn.cursor()
	insert = "INSERT INTO posts VALUES (" + "\'" + title + "\'" + ", " + "\'" + post + "\'" + ")"
	cur.execute(insert)
	conn.commit()
	conn.close()

def new_comment(title, comment):
	conn = get_db()
	cur = conn.cursor()
	insert = "INSERT INTO comments VALUES (" + "\'" + title + "\'" + ", " + "\'" + comment + "\'" + ")"
	cur.execute(insert)
	conn.commit()
	conn.close()

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
##### /\DATABASE/\ #####

# URL spaces workaround
def make_url(title):
	return title.replace(" ", "_")
def make_title(url):
	return url.replace("_", " ")

# The current RowID
current_row = None


@app.route("/", methods=["GET","POST"])
@app.route("/index.html", methods=["GET","POST"])
def index():
	if request.method == "GET": # If the form is not being used, just display the page
		titles = get_titles()
		links = [ [ str("/title/" + make_url(i[0])), i[0] ] for i in titles]
		return render_template("index.html", post_list=links)

	else: # Take the title and post from the form and make a new post
		title = request.form["new_title"]
		post = request.form["new_post"]

		new_post(title, post) # put the new post into the database
		titles = get_titles()
		links = [ [str("/title/" + make_url(i[0])), i[0]] for i in titles]
		return render_template("index.html", post_list=links)






@app.route("/title/<post_title>", methods=["GET","POST"])
def title(post_title):
	if request.method == "GET":
		title = make_title(post_title)
		post = get_post(title)
		comments = [str(i[0]) for i in get_comments(title)]
		return render_template("title.html", title=title, post=post, comments=comments)

	else:
		title = make_title(post_title)
		comment = request.form["comment"]
		new_comment(title, comment)

		post = get_post(title)
		comments = [str(i[0]) for i in get_comments(title)]
		return render_template("title.html", title=title, post=post, comments=comments)


if __name__=="__main__":
	#app.run(host='0.0.0.0', port=8080, debug=True)
	app.run(debug=True)