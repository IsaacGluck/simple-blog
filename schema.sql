CREATE TABLE posts (title TEXT UNIQUE, post TEXT, username TEXT);
CREATE TABLE comments (title TEXT UNIQUE, comment TEXT, username TEXT);
CREATE TABLE users (username TEXT UNIQUE, password TEXT);
