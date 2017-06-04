#!/usr/bin/python
import sqlite3
class DTUI:

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
		print 'Message?'
		message=raw_input()
		file = open('./outgoing/'+recipient+'.txt', 'w')
		file.write(message)
		file.close()
		c.execute('CREATE TABLE IF NOT EXISTS "'+recipient+'" ("SeRe" "TEXT", "Message" "TEXT", "Timestamp" "TEXT" DEFAULT CURRENT_TIMESTAMP)')
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


