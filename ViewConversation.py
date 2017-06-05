#!/usr/bin/python
import sqlite3, os

conn = sqlite3.connect('./log/database.db')
c = conn.cursor()
conn.text_factory = str

def openConvo():
	print "\nSelect contact to see messages"
	chatname= raw_input()
	print '\n'
	path = './incoming/'
	try:
		c.execute('SELECT * FROM "'+chatname+'" ORDER BY TimeEntered DESC Limit 10') #Grabs last 10 msgs
		ansr= c.fetchall()

		for index in range(len(ansr)-1,-1, -1):
			print ansr[index]
		print '\n'
	except sqlite3.OperationalError:
		print "Contact not found\n"




