#!/usr/bin/python
import sqlite3

conn = sqlite3.connect('./log/database.db')
c = conn.cursor()

def send():
	print '\nRecipient?'
	recipient=raw_input()
	c.execute('SELECT "Num" FROM "Contacts" WHERE "Name"="'+recipient+'"')		#Get phone number of contact
	recipNum = c.fetchone()
	if(recipNum==None):			#If recipient is not a contact, do not continue
		print "Contact not found\n"
	else:
		print '\nMessage?'
		message=raw_input()
		print '\n'
		
		file = open('./log/OutCount.txt', 'r') #Read count from .txt
		oCount= file.read()
		file.close()
		file = open('./log/OutCount.txt', 'w') #increase count by 1
		file.write(str(int(oCount)+1))
		file.close()

		file = open('./outgoing/'+str(oCount)+'.txt', 'w')	#Put message in .txt to send
		file.write(recipNum[0] +'\n'+message)
		file.close()

		message = message.replace("'","")
		c.execute('CREATE TABLE IF NOT EXISTS "'+recipient+'" ("InOut" "TEXT", "Message" "TEXT", "TimeEntered" "TEXT" DEFAULT CURRENT_TIMESTAMP)')	#Create message log for this recipient
		conn.commit()
		c.execute("INSERT INTO "+recipient+" (InOut, Message) VALUES ('Out', '"+message+"')")	#Add message to recipient
		conn.commit()