#!/usr/bin/python
import sqlite3
import os
import SendMessage, NewContact, ReceivedMessage, ViewConversation

class DTUI:

	#Create Connection ton Database
	conn = sqlite3.connect('./log/database.db')
	c = conn.cursor()

	#Create Contacts List
	c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY, {nf2} {ft2})'\
		.format(tn='Contacts', nf='Name', ft='TEXT', nf2='Num', ft2='TEXT'))
	conn.commit() 


	while True:
		#User Prompt
		print '\n1.Send message\n2.Check for new messages\n3.Add new contact\n4.Open conversation?'
		response = raw_input()


		#Send Message
		if(response== '1'):
			SendMessage.send()

		#Check for new messages
		elif(response=='2'):
			ReceivedMessage.checkMsgs()

		#Add a new Contact
		elif(response=='3'):
			NewContact.enterNewContact()
		
		#Open a conversation
		elif(response=='4'):
			ViewConversation.openConvo()

		else:
			print 'Quit? (yes/no)'
			ans = raw_input();
			if ans=='yes':
				break;


	conn.close()