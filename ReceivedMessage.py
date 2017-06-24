#!/usr/bin/python
import sqlite3
import os


conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def checkMsgs():
	path = './incoming/'
	count=0
	for filename in os.listdir(path):
		if filename.endswith('.txt'):
			count+=1
			file = open(path+filename, 'r') #Read lines from .txt
			lines= file.readlines()
			file.close()
			
			numbr= lines[0].split('\n')[0]	#get rid of '\n'

			try:
				c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr+'"')
				rec=c.fetchone()
				test = rec[0]
			except Exception as e:
					try:
						c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr[1:]+'"')
						rec=c.fetchone()
						test = rec[0]
					except Exception as e:
						try:
							c.execute('SELECT "Name" FROM "Contacts" WHERE "Num"="'+numbr[2:]+'"')
							rec=c.fetchone()
							test = rec[0]
						except Exception as e:
							print "Did not work"


			c.execute('CREATE TABLE IF NOT EXISTS "'+rec[0]+'" ("InOut" "TEXT", "Message" "TEXT", "TimeEntered" "TEXT" DEFAULT CURRENT_TIMESTAMP)')	#Create message log for this
			conn.commit()
			c.execute("INSERT INTO '"+rec[0]+"'(InOut, Message) VALUES ('In', '"+lines[1].split('\n')[0]+"')") #Insert into Convo
			conn.commit()

			os.remove(path+filename)
			print "\nFrom: "+rec[0]+"\nMessage: "+lines[1]+"\n"
	if count==0:
		print "\nNo new Messages\n"

