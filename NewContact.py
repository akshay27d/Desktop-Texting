#!/usr/bin/python
import sqlite3

conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def enterNewContact():
	print '\nName?'
	name= raw_input()
	print '\nNumber?'
	num = raw_input()
	print '\n'
	try:
		c.execute("INSERT INTO Contacts (Name, Num) VALUES ('"+name+"', '"+num+"')")	#insertnew contact
	except sqlite3.IntegrityError:	#contact already exists
		 print(name+' already exists in your contacts, Update info? yes or no')
		 answr= raw_input()
		 if(answr=='yes'):	#to update with new info or not
		 	c.execute('UPDATE Contacts SET "Num"=("'+num+'") WHERE "Name" = "'+name+'"')
		 	print "Contact Updated\n"
		 else:
		 	print "Contact not updated\n"
	conn.commit()
	conn.close()