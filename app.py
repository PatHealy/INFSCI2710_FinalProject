from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack

from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "postgres"
POSTGRES_PW = "pw"
POSTGRES_DB = "final_project"

#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(DB_URL)
inspector = inspect(engine)

db = SQLAlchemy(app)

@app.route('/')
def home_page():
	example_contents = get_example()
	return render_template('home.html', example_contents=example_contents)

def get_example():
	returned = []

	with engine.connect() as con:
		statement = text("""SELECT * FROM example;""")
		rs = con.execute(statement)

		for row in rs:
			returned.append(row)

	return returned

# Models
# This is likely unnecessary for most of what we need to do,
# but a solid back-end app should probably contain models of the DB tables
class Example(db.Model):
	example_id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100)) # String is equivalent to VARCHAR