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
def browse_query():
	# table: simple string representing table
	# where: list of tuples (column, operator, value)
	# order: tuple (order by, order)
	table, where, order = clean_queries(request.args.get('table'), request.args.get('where'), request.args.get('order'))

	# run the query based on the specifications in the query string
	# keys contains column names, contents is rows
	keys, contents = get_query(table, where, order)
	# dictionary containing data types
	cols = get_columns(table)
	col_types = None
	if cols != None:
		col_types = cols.values()
	types, string_types, datetime_types, date_types, num_types = get_types(cols)
	pks = get_pks(table)
	fks = get_fks(table)
	references = get_references(table)
	joins = get_joins(table)
	editable = not (table=="orders")

	flash(get_flash_string(table, where, order))

	return render_template('browse.html', table=table, where=where, order=order, keys=keys, contents=contents, types=types, num_types=num_types, string_items=string_types, datetime_types=datetime_types, date_types=date_types, pks=pks, fks=fks, col_types=col_types, references=references, joins=joins, double_join=False, editable=editable)

@app.route('/browse/double-join')
def browse_double_join():
	table1pkName = request.args.get('table1pkName')
	table1pk = request.args.get('table1pk')
	table2 = request.args.get('table2')
	table3 = request.args.get('table3')
	join23 = request.args.get('join23')
	message = request.args.get('message')
	keys, contents = get_double_join(table1pkName, table1pk, table2, table3, join23)

	flash(message)
	return render_template('browse.html', keys=keys, contents=contents, table=None, where=None, order=None, types=None, num_types=None, string_items=None, datetime_items=None, date_items=None, pks=None, fks=None, col_types=None, references=None, joins=None, double_join=True, editable=False)

@app.route('/create/<type>')
def create(type):
	types = get_columns(type)
	return render_template('create.html', table=type, types=types)

@app.route('/create', methods=['POST'])
def create_new_entry():
	entry = request.json;
	table_name = entry['table']
	del entry['table']

	cols = get_columns(table_name)

	statement_text = """INSERT INTO  """ + table_name + """ ("""

	for k in entry.keys():
		statement_text = statement_text + k + """, """

	statement_text = statement_text[:-2] + """) VALUES ("""

	for k,v in entry.items():
		if 'string' in cols[k]:
			statement_text = statement_text + """'""" + v + """', """
		else:
			statement_text = statement_text + v + """, """

	statement_text = statement_text[:-2] + """);"""

	#print(statement_text)

	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

	return "Created"

@app.route('/edit/<type>/<pk>')
def edit(type, pk):
	content = get_row(type, pk)
	types = get_columns(type)
	return render_template('edit.html', table=type, primary_key=pk, content=content, types=types)

@app.route('/view/<type>/<pk>')
def view(type, pk):
	content = get_row(type, pk)
	return render_template('view.html', table=type, primary_key=pk, content=content)

@app.route('/update', methods=['POST'])
def update():
	entry = request.json;
	table_name = entry['table']
	del entry['table']

	pks = get_pks(table_name)
	cols = get_columns(table_name)

	pk_pairs = {}
	for k in pks:
		pk_pairs[k] = entry[k]
		del entry[k]

	statement_text = """UPDATE """ + table_name + """ SET """

	for k,v in entry.items():
		if 'string' in cols[k]:
			statement_text = statement_text + k + """ = '""" + v + """', """
		elif 'datetime' in cols[k]:
			statement_text = statement_text + k + """ = '""" + v.replace("T", " ") + """', """
		elif 'date' in cols[k]:
			statement_text = statement_text + k + """ = '""" + v + """', """
		else:
			statement_text = statement_text + k + """ = """ + v + """, """

	statement_text = statement_text[:-2] + """ WHERE """ 

	for k,v in pk_pairs.items():
		if 'string' in cols[k]:
			statement_text = statement_text + k + """ = '""" + v + """', """
		else:
			statement_text = statement_text + k + """ = """ + v + """, """

	statement_text = statement_text[:-2] + """;"""

	#print(statement_text)

	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

	return "Updated"

@app.route('/remove', methods=['POST'])
def remove():
	entry = request.json;
	table_name = entry['table']
	del entry['table']

	pks = get_pks(table_name)
	cols = get_columns(table_name)

	pk_pairs = {}
	for k in pks:
		pk_pairs[k] = entry[k]
		del entry[k]

	statement_text = """DELETE FROM """ + table_name + """ WHERE """

	for k,v in pk_pairs.items():
		if 'string' in cols[k]:
			statement_text = statement_text + str(k) + """ = '""" + str(v) + """', """
		else:
			statement_text = statement_text + str(k) + """ = """ + str(v) + """, """

	statement_text = statement_text[:-2] + """;"""

	#print(statement_text)

	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

	return "Deleted"

@app.route('/update/<table>/<update_type>')
def update_redirect(table, update_type):
	if update_type == "update":
		flash("Updated " + table + " entry!")
	elif update_type == "new":
		flash("Create new " + table + " entry!")
	elif update_type == "remove":
		flash("Removed entry from " + table + "!")
	return redirect("/browse?table=" + table)

@app.route('/aggregation')
def aggregation():
	queries = [
		"""SELECT products.p_name, count(*) FROM cases, products WHERE cases.product_id=products.product_id GROUP BY products.product_id ORDER BY count(*) DESC;""",
		"""SELECT employees.e_first, employees.e_last, count(*) from cases, employees WHERE cases.employee_id=employees.employee_id AND cases.c_status='Closed' GROUP BY employees.employee_id ORDER BY count(*) DESC;""",
		"""SELECT customers.c_first, customers.c_last, count(*) from cases, customers WHERE cases.customer_id=customers.customer_id GROUP BY customers.customer_id ORDER BY count(*) DESC;""",
		"""SELECT customers.c_company, count(*) FROM customers, cases WHERE customers.customer_id=cases.customer_id GROUP BY customers.c_company ORDER BY count(*) DESC;"""
	]

	rows_returned = []
	with engine.connect() as con:
		for statement_text in queries:
			rows = []
			statement = text(statement_text)
			rs = con.execute(statement)

			for row in rs:
				rows.append(row)
			rows_returned.append(rows)

	return render_template('aggregation.html', rows=rows_returned)

def processT1(t1):
	t1 = t1.replace("&gt;", ">")
	t1 = t1.replace("&lt;", "<")
	return t1

def get_query(table, where, order):
	if table == None:
		return None, None

	statement_text = "SELECT * FROM " + table

	if where != None and len(where) > 0:
		statement_text = statement_text + " WHERE "
		for t in where:
			search_string = t[2]
			operator = t[1]
			if t[1] == "contains":
				operator = " LIKE "
				search_string = " '%" + t[2] + "%'"
			else:
				t[1] = processT1(t[1])
				operator = t[1]

			statement_text = statement_text + t[0] + operator + search_string + " AND "
		statement_text = statement_text[:-5]

	if order != None and len(order) > 0:
		statement_text = statement_text + " ORDER BY " + order[0] + " " + order[1]

	statement_text = statement_text + ";"

	rows = []
	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

		for row in rs:
			rows.append(row)

	header = [x['name'] for x in inspector.get_columns(table)]

	return header, rows

def get_double_join(table1pkName, table1pk, table2, table3, join23):
	table3_col_headers = [x['name'] for x in inspector.get_columns(table3)]
	statement_text = "SELECT "

	for h in table3_col_headers:
		statement_text = statement_text + table3 + "." + h + ", "
	statement_text = statement_text[:-2] + " FROM " + table2 + ", " + table3 + " WHERE " + table2 + "." + table1pkName + "=" + table1pk + " AND " + table2 + "." + join23 + "=" + table3 + "." + join23 + ";"
	rows = []
	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

		for row in rs:
			rows.append(row)

	return table3_col_headers, rows

def get_columns(type):
	"Returns a dictionary containing (column name, data type)"
	#Data type can be number, string, or boolean. Also may include the word static, if they should not be editable (such as in primary keys)
	if type == None:
		return None
	returned = {}
	cols = inspector.get_columns(type)
	for c in cols:
		t = 'string'
		if 'NUMERIC' in str(c['type']) or 'INTEGER' in str(c['type']):
			t = 'number'
		elif 'TIMESTAMP' in str(c['type']):
			t = 'datetime'
		elif 'DATE' in str(c['type']):
			t = 'date'

		if c['name'] in get_pks(type):
			t = t + " static"

		returned[c['name']] = t
		#for k, v in c.items():
		#	print(k + ": " + str(v))
		#print()

	return returned

def get_pks(table):
	"Returns a list of primary keys of the given table"
	if table == None:
		return None
	return inspector.get_pk_constraint(table)['constrained_columns']

def get_fks(table):
	"Returns a dictionary of column_name:other_table, representing the FK relationships"
	if table == None:
		return None
	fks = {}
	for full in inspector.get_foreign_keys(table):
		fks[full['constrained_columns'][0]] = full['referred_table']
	return fks

def get_row(type, pk):
	"Returns a dictionary of a whole row in the form (columnName,value)"
	pk_name = get_pks(type)[0]
	header = [x['name'] for x in inspector.get_columns(type)]
	types = get_columns(type)

	# TODO -- Handle multi-col primary keys
	statement_text = """SELECT * FROM """ + type + """ WHERE """ + pk_name + """=""" +pk + """;"""

	rows = []
	with engine.connect() as con:
		statement = text(statement_text)
		rs = con.execute(statement)

		for row in rs:
			rows.append(row)

	returned = {}
	for i in range(len(header)):
		returned[header[i]] = rows[0][i]

	for k,v in types.items():
		if 'datetime' in v:
			returned[k] = str(returned[k]).replace(" ", "T")

	return returned

def get_types(cols):
	if cols == None:
		return None, None, None, None, None
	types = []
	string_types = []
	datetime_types = []
	date_types = []
	for k,v in cols.items():
		if 'string' in v:
			string_types.append(k)
			types.append(True)
		else:
			types.append(False)
		if 'datetime' in v:
			datetime_types.append(True)
		else:
			datetime_types.append(False)
		if 'date' in v:
			date_types.append(True)
		else:
			date_types.append(False)

	return types, string_types, datetime_types, date_types, len(types)

def get_flash_string(table, where, order):
	if table == None:
		return ""
	temp = "Browsing " + table.upper() + " items"

	if where != None and len(where) > 0:
		temp = temp + " where " 
		for t in where:
			temp = temp + t[0].upper() + " " + t[1] + " " + t[2] + " and "
		temp = temp[:-4]

	if order != None and len(order) > 0:
		if order[1] == 'DESC':
			temp = temp + " in DESCENDING order by " + order[0]
		else:
			temp = temp + " in ASCENDING order by " + order[0]

	return temp + "."

def clean_queries(table,where,order):
	if table == "null":
		table = None
	if where == "null":
		where = None
	elif where != None:
		where = json.loads(where)
	if order == "null":
		order = None
	elif order != None:
		order = json.loads(order)

	return table, where, order

def get_references(table):
	"Returns a dictionary representing what other tables reference this one"
	if table == None:
		return None
	return { 
		'employees':[['salesperson title for this employee', 'salespersons'], ['cases assigned to this employee', 'cases']],
		'products': [['cases involving this product', 'cases'], ['orders including this product', 'orders']],
		'resolutions': [['cases using this resolution', 'cases']],
		'customers': [['orders by this customer', 'orders'], ['cases involving this customer', 'cases']],
		'cases': [['comments on this case', 'comments']],
		'salespersons': None,
		'orders': None,
		'comments':None
	}[table]

def get_joins(table):
	if table == None:
		return None
	joins = {
		'customers': [['products purchased by this customer', 'orders', 'products', 'product_id']],
		'products': [['customers who purchased this product', 'orders', 'customers', 'customer_id'], ['common resolutions involving this product', 'cases', 'resolutions', 'resolution_id']]
	}
	if table not in joins.keys():
		return None
	return joins[table]