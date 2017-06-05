#!/usr/bin/python
import sqlite3
import os
import SendMessage
import NewContact
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
		SendMessage.send()

	#Add a new Contact
	elif(response=='new contact'):				#New Contact is done
		NewContact.enterNewContact()