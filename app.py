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
	return render_template('home.html')

@app.route('/browse')
def browse_home():
	return render_template('browse.html', type='none', keys=None, contents=None, order_by=None, order=None)

@app.route('/browse/<type>')
def browse_stuff(type):
	keys, contents = get_all(type)
	return render_template('browse.html', type=type, keys=keys, contents=contents, order_by=None, order=None)

@app.route('/browse/<type>/<order_by>/<order>')
def browse_stuff_order_by(type,order_by, order):
	keys, contents = get_all(type, order_by, order)
	return render_template('browse.html', type=type, keys=keys, contents=contents, order_by=order_by, order=order)

@app.route('/create')
def create_home():
	return render_template('create.html')

def get_all(type, order_by='_na', order='_na'):
	print("Order by " + order_by + ", " + order)
	if order == 'DESC':
		#call query with DESC
		pass
	else:
		#call query without DESC
		pass
	return get_example()

def get_example():
	keys = ['name', 'a', 'b']

	contents = []
	contents.append(['Example Item 1', 'example a', 'example b'])

	#with engine.connect() as con:
	#	statement = text("""SELECT * FROM example;""")
	#	rs = con.execute(statement)

	#	for row in rs:
	#		returned.append(row)

	return keys, contents

# Models
# This is likely unnecessary for most of what we need to do,
# but a solid back-end app should probably contain models of the DB tables
class Example(db.Model):
	example_id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100)) # String is equivalent to VARCHAR