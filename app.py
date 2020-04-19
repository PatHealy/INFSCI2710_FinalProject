from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack

from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #this is just for development purposes -- not a real secret key!

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
	flash("Viewing " + type.upper())
	return render_template('browse.html', type=type, keys=keys, contents=contents, order_by=None, order=None)

@app.route('/browse/<type>/<order_by>/<order>')
def browse_stuff_order_by(type,order_by, order):
	keys, contents = get_all(type, order_by, order)
	flash("Viewing " + type.upper() + " ordered by " + order_by.upper() + " in " + order.upper() + " order")
	return render_template('browse.html', type=type, keys=keys, contents=contents, order_by=order_by, order=order)

@app.route('/create/<type>')
def create(type):
	types = get_columns(type)
	return render_template('create.html', table=type, types=types)

@app.route('/create', methods=['POST'])
def create_new_entry():
	entry = request.json;
	print(entry)
	table_name = entry['table']
	del entry['table']
	#TODO -- actually do the insert
	return "Created"

@app.route('/edit/<type>/<pk>')
def edit(type, pk):
	content = get_row(type, pk)
	types = get_columns(type)
	return render_template('edit.html', table=type, primary_key=pk, content=content, types=types)

@app.route('/update', methods=['POST'])
def update():
	entry = request.json;
	table_name = entry['table']
	del entry['table']
	#TODO -- actually do the update
	return "Updated"

@app.route('/update/<table>/<update_type>')
def update_redirect(table, update_type):
	if update_type == "update":
		flash("Updated " + table + " entry!")
	elif update_type == "new":
		flash("Create new " + table + " entry!")
	return redirect("/browse/" + table)

def get_all(type, order_by='_na', order='_na'):
	# TODO: actually interact with the database here
	statement_text = """SELECT * FROM """ + type

	if not order_by == '_na':
		statement_text = statement_text + " ORDER BY " + order_by

	if order == 'DESC':
		#call query with DESC
		statement_text = statement_text + " DESC";
	elif order == 'ASC':
		#call query without DESC
		statement_text = statement_text + " ASC";

	statement_text = statement_text  + """;"""

	rows = []
	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

		for row in rs:
			rows.append(row)

	header = [x['name'] for x in inspector.get_columns(type)]

	return header, rows

def get_columns(type):
	"Returns a dictionary containing (column name, data type)"
	#TODO
	#Data type can be number, string, or boolean. Also may include the word static, if they should not be editable (such as in primary keys)
	return {'Example 1': 'number static', 'Example 2': 'string', 'Example 3': 'boolean static', 'Example 4': 'string static'}

def get_row(type, pk):
	"Returns a dictionary of a whole row in the form (columnName,value)"\
	#TODO
	#Placeholder
	return {'Example 1': 5, 'Example 2': 'This is an example text area.', 'Example 3': True, 'Example 4': 'This text area cannot be edited'}

def get_example():
	#This method is just a placeholder until we actually interface with the DB
	keys = ['id', 'name', 'a', 'b']

	contents = []
	contents.append(['1','Example Item 1', 'example a', 'example b'])

	#This commented out bit shows how to interact with the DB
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