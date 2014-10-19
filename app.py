import handle
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
	return render_template("index.html")

@app.route("/create.html")
def create():
	return render_template("create.html")


if __name__=="__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)