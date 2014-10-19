import sqlite3

conn = sqlite3.connect("blog.db")
c = conn.cursor()

def new_post(title, post):
	insert = "INSERT INTO posts VALUES (" + title + ", " + post + ")"
	c.execute(insert)
	conn.commit()

def new_comment(title, comment):
	insert = "INSERT INTO comments VALUES (" + title + ", " + comment + ")"
	c.execute(insert)
	conn.commit()

def get_titles():
	query = "SELECT title FROM posts"
	c.execute(query)
	titles = c.fetchall()
	return titles

def get_comments(title):
	query = "SELECT comment from comments WHERE title = " + title
	c.execute(query)
	comments = c.fetchall()
	return comments

def get_post(title):
	query = "SELECT post FROM posts WHERE title = " + title
	c.execute(query)
	post = c.fetchall()
	return post
