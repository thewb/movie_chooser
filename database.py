#!/usr/bin/python3
import sqlite3
import os

class DB:
	cnx = None

	def connect(self):
		self.conn = sqlite3.connect("/var/cache/minidlna/files.db")
	def query(self, sql):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			
		except:
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql)
			return cursor

	def commit(self):
			self.cnx.commit()

def finder():
	db = DB()
	sql = "select path from details where path like '%/Movies/%' order by RANDOM() limit 1;"
	c = db.query(sql)
	movie_path = c.fetchone()[0]
	print(movie_path)
	if os.path.isfile(movie_path) and '.mp4' in movie_path:
		return movie_path
	else:
		return finder()