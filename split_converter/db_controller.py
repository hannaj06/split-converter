import sqlite3
import datetime


class db_controller(object):
	def __init__(self):
		self.connection = sqlite3.connect('split_converter.db')
		self.cursor = self.connection.cursor()
		print('connected to db')

	#postcondition: history table cleared in split_converter.db
	def clear_db(self):
		self.cursor.execute('''DROP TABLE history''')
		sql = '''CREATE TABLE history (time DATETIME primary key, results str);'''
		self.cursor.execute(sql)
		self.connection.commit()
		print('history table cleared')

	#accepts a list (queue) of dictionaries
	#postcondition: inserts n number of records into db for fetching
	#def save_results(self, history):
	def insert_record(self, history):
		for record in history:
			try:
				sql = '''INSERT INTO history (time, results) VALUES ('%s', "%s");''' % (record['timestamp'], record['results'])
				self.cursor.execute(sql)
				self.connection.commit()
			except sqlite3.IntegrityError as e:
				print('skip duplicate entry into db' + str(record))
				print(str(e))

	#postondition: returns all records from hisory table
	def fetch(self):
		sql = "SELECT * FROM history"
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	#precondition: accepts valid sql statment
	#postcondition: commits sql statement to db, doesn not return any records
	def query(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()

	def close(self):
		self.cursor.close()
		self.connection.close()
		print('db cursor and connection closed')