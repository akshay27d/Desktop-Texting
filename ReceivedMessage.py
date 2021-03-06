#!/usr/bin/python
import sqlite3
import os
import sys  


conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def checkMsgs():
	path = './incoming/'
	count=0
	for filename in os.listdir(path):
		doIt=True
		if filename.endswith('.txt'):
			count+=1
			file = open(path+filename, 'r') #Read lines from .txt
			lines= file.readlines()
			file.close()
			
			numbr= lines[0].split('\n')[0]	#get rid of '\n'
			try:
				c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr+'"')
				rec=c.fetchone()
				sender = rec[0]
			except Exception as e:
					try:
						c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr[1:]+'"')
						rec=c.fetchone()
						sender = rec[0]
					except Exception as e:
						try:
							c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr[2:]+'"')
							rec=c.fetchone()
							sender = rec[0]
						except Exception as e:
							print "\nReceived message from number not in Contacts"
							doIt = False

			msg = lines[1]
			msg = msg.replace("'", "`");

			if doIt:
				c.execute('CREATE TABLE IF NOT EXISTS "'+sender+'" ("InOut" "TEXT", "Message" "TEXT", "TimeEntered" "TEXT" DEFAULT CURRENT_TIMESTAMP)')	#Create message log for this
				conn.commit()
				c.execute("INSERT INTO "+sender+" (InOut, Message) VALUES ('In', '"+msg+"')")				
				conn.commit()
				print "\nFrom: "+sender+"\nMessage: "+msg+"\n"

			os.remove(path+filename)
			
	if count==0:
		print "\nNo new Messages\n"

