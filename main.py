from flask import Flask
import sqlite3
from datetime import datetime
import pdb

app = Flask(__name__)
db = sqlite3.connect('test.db')

def convert_row(arr):
	s = "<tr>"
	for col in arr:
		s += "<td>"+str(col)+"</td>"
	s += "</tr>"
	return s

def get_header(name):
	header = db.cursor()
	header.execute("SELECT sql from sqlite_master where name=\""+name+"\"")
	create_sql = header.fetchall()[0][0]
	col_names = create_sql[create_sql.index("(")+1:create_sql.index(")")].split(",")
	return convert_row(col_names)
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def test():
		return "test"

@app.route("/tables")
def list_tables():
	cursor = db.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

	s = ""
	tbls = cursor.fetchall()
	for x in tbls:
		s += "<a href=\"/tables/"+x[0]+"\">"+x[0]+"<br />"
	return s

@app.route("/tables/<name>")
def retrieve_table(name):

	if not name:
		return list_tables()

	s = "<table>"+get_header(name)

	cursor = db.cursor()
	cursor.execute("SELECT * FROM "+name)
	rows = cursor.fetchall()
	pdb.set_trace()
	for row in rows:
		s += convert_row(row)

	return s

if __name__ == "__main__":
    app.run()