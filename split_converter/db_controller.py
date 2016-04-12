import sqlite3
import datetime


class db_controller(object):
	def __init__(self):
		self.connection = sqlite3.connect('split_converter.db')
		self.cursor = self.connection.cursor()
		print('connected to db')

	def create_table(self):
		#self.cursor.execute('''DROP TABLE history''')
		sql = '''CREATE TABLE history (time DATETIME, results str);'''
		self.cursor.execute(sql)
		self.connection.commit()

	#accepts a list (queue) of dictionaries
	#postcondition: inserts n number of records into db for fetching
	#def save_results(self, history):
	def insert_record(self, history):
		for record in history:
			sql = '''INSERT INTO history (time, results) VALUES ('%s', "%s");''' % (record['timestamp'], record['results'])
			self.cursor.execute(sql)
			self.connection.commit()

	def fetch(self):
		sql = "SELECT * FROM history"
		self.cursor.execute(sql)
		print(self.cursor.fetchall())

	def query(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()