#!/usr/bin/python
import sqlite3

conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def enterNewContact():
	print 'Name?'
	name= raw_input()
	print 'Number?'
	num = raw_input()
	try:
		c.execute("INSERT INTO Contacts (Name, Num) VALUES ('"+name+"', '"+num+"')")
	except sqlite3.IntegrityError:
		 print(name+' already exists in your contacts, Update info? yes or no')
		 answr= raw_input()
		 if(answr=='yes'):
		 	c.execute('UPDATE Contacts SET "Num"=("'+num+'") WHERE "Name" = "'+name+'"')
		 	print "Contact Updated"
		 else:
		 	print "Contact not updated"
	conn.commit()