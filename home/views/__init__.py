from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
from .index import *
from .query1 import *
from .query2 import *
from .query3 import *
from .query4 import *
from .about import *
from .query5 import *

def populate_form(id, query):
	table = []
	with connection.cursor() as cursor:
			cursor.execute(query)
			table = dictfetchall(cursor)
			# print(table)
			table = [row[id] for row in table]

	return (table, "")


def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]
