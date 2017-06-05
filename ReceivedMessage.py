#!/usr/bin/python
import sqlite3
conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "NewMessages" ("Contact" "TEXT", "Message" "TEXT")')
conn.commit()
import os
path = './incoming/'
if os.listdir(path)==[]:		#If no new messages
	print "No new messages"
else:
	for filename in os.listdir(path):
		if filename.endswith('.txt'):
			temp=filename.split('.')
			numToConvert=temp[0]			#Get contact name
			c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numToConvert+'"')
			rec=c.fetchone()

			file = open(path+filename, 'r') #Read message form .txt
			inMsg= file.read()
			file.close()

			c.execute("INSERT INTO NewMessages (Contact, Message) VALUES ('"+rec[0]+"', '"+inMsg+"')") #insert into NewMessages
			c.execute("INSERT INTO '"+rec[0]+"'(InOut, Message) VALUES ('In', '"+inMsg+"')") #Insert into Convo
			conn.commit()

