import sqlite3
import datetime


class db_controller(object):
	def __init__(self):
		self.connection = sqlite3.connect('split_converter.db')
		self.cursor = self.connection.cursor()
		print('connected to db')

	def create_table(self):
		#self.cursor.execute('''DROP TABLE history''')
		sql = '''CREATE TABLE history (time str, results str);'''
		self.cursor.execute(sql)
		self.connection.commit()

	#accepts a list (queue) of dictionaries
	#postcondition: inserts n number of records into db for fetching
	#def save_results(self, history):
	def query(self):
		#print(datetime.datetime.now())
		sql = '''INSERT INTO history (time, results) VALUES ('%s', 'this is a test');''' % str(datetime.datetime.now())
		print(sql)
		self.cursor.execute(sql)
		self.connection.commit()
		sql = "SELECT * FROM history"
		self.cursor.execute(sql)
		print(self.cursor.fetchall())
db = db_controller()
#db.create_table()
db.query()

