from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
import json
import csv


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


def export_csv_file(request, data):
	
	# data = [{'NAME': 'Ohio', 'DATA_VALUE': '21%'},
    #      {'NAME': 'Ohio', 'DATA_VALUE': '21%'}, {'NAME': 'Ohio', 'DATA_VALUE': '21%'}, {'NAME': 'Ohio', 'DATA_VALUE': '21%'}]

	response = HttpResponse()
	response['Content-Disposition'] = 'attactment; filename="data.csv"'

	writer = csv.writer(response)
	writer.writerow([key for key in data[0]])

	for row in data:
		writer.writerow([row[i] for i in row])

	return response


def list_to_query(list):
	temp=[]
	for i in list:
		temp.append("'"+i+"'")

	return ', '.join(temp)

