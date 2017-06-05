#!/usr/bin/python
import sqlite3
import os
class DTUI:

	def refreshMessages():
		path = './incoming'
		if os.listdir(path)==[]:
			print "No new messages"
		else:
			



	#Create Connection ton Database
	conn = sqlite3.connect('./log/database.db')
	c = conn.cursor()

	#Create Contacts List
	c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY, {nf2} {ft2})'\
		.format(tn='Contacts', nf='Name', ft='TEXT', nf2='Num', ft2='TEXT'))
	conn.commit()


	#User Prompt
	print 'send, check new messages, new contact?'
	response = raw_input()

	#Send Message
	if(response== 'send'):
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
			c.execute("INSERT INTO '"+recipient+"' (InOut, Message) VALUES ('Out', '"+message+"')")	#Add message to recipient
			conn.commit()

	#Add a new Contact
	elif(response=='new contact'):				#New Contact is done
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
	 elif(response='check new messages'):



