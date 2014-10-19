import handle
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
	return render_template("index.html", post_link=None, post=None)

@app.route("/create.html")
def create():
	return render_template("create.html")

@app.route("/title/<post_title>")
def title(post_title):
	post = handle.get_post(post_title)
	comments = handle.get_comments(post_title)
	return render_template("title.html", title=post_title, post=post, comments=comments)


if __name__=="__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)