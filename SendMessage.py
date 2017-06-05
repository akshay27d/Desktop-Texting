#!/usr/bin/python
import sqlite3

conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def send():
	print 'Recipient?'
	recipient=raw_input()
	c.execute('SELECT "Num" FROM "Contacts" WHERE "Name"="'+recipient+'"')		#Get phone number of contact
	recipNum = c.fetchone()
	if(recipNum==None):			#If recipient is not a contact, do not continue
		print "Contact not found"
	else:
		print 'Message?'
		message=raw_input()
		file = open('./outgoing/'+recipNum[0]+'.txt', 'w')	#Put message in .txt to send
		file.write(message)
		file.close()

		c.execute('CREATE TABLE IF NOT EXISTS "'+recipient+'" ("InOut" "TEXT", "Message" "TEXT", "TimeEntered" "TEXT" DEFAULT CURRENT_TIMESTAMP)')	#Create message log for this recipient
		conn.commit()
		c.execute("INSERT INTO "+recipient+" (InOut, Message) VALUES ('Out', '"+message+"')")	#Add message to recipient
		conn.commit()