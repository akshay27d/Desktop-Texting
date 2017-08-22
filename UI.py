#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, 
	QMessageBox, QDesktopWidget, QMainWindow, qApp, QAction, QLineEdit, 
	QPlainTextEdit, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QTableWidget, 
	QTableWidgetItem, QTextEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication

import sqlite3
import os
import SendMessage3, ReceivedMessage3

class DTexting(QMainWindow):
	def __init__(self):
		super().__init__()

		conn = sqlite3.connect('./log/database.db')
		c = conn.cursor()

		#Create Contacts List
		c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY, {nf2} {ft2})'\
			.format(tn='Contacts', nf='Name', ft='TEXT', nf2='Num', ft2='TEXT'))
		conn.commit() 

		self.initUI()
        
	def initUI(self):	
		self.resize(500, 300)
		self.center()


		extractAction = QAction('&Send', self)
		extractAction.setShortcut('Ctrl+e')
		extractAction.triggered.connect(self.gotoSendTab)

		extractAction1 = QAction('&Check', self)
		extractAction1.setShortcut('Ctrl+r')
		extractAction1.triggered.connect(self.gotoCheckMessages)

		extractAction2 = QAction('&Log', self)
		extractAction2.setShortcut('Ctrl+t')
		extractAction2.triggered.connect(self.gotoSendTab)
		
		self.toolBar = self.addToolBar('Top')
		self.toolBar.addAction(extractAction)
		self.toolBar.addAction(extractAction1)
		self.toolBar.addAction(extractAction2)
		self.show()
	
	def gotoSendTab(self):
		self.sendtab= SendTab(self)
		self.setWindowTitle("Send Message")
		self.setCentralWidget(self.sendtab)
		self.sendtab.btnSend.clicked.connect(self.newtab) 
		self.show()

	def gotoCheckMessages(self):
		self.checktab= CheckTab(self)
		self.setWindowTitle("Check Messages")
		self.setCentralWidget(self.checktab)
		self.show()

	def newtab(self):
		self.Window = newclass(self)
		self.setWindowTitle("UIWindow")
		self.setCentralWidget(self.Window)
		self.show()

	def center(self):       #center in screen 
		qr= self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

		
class SendTab(QWidget):
	def __init__(self,parent=None):
		super().__init__()
		QToolTip.setFont(QFont('SansSerif', 10))  #Set tooltip font
		
		self.setWindowTitle('Desktop Texting')   #Window title



		self.initUI()

	
	def initUI(self):
		print("Here")
		# btn = QPushButton('Quit', self)
		# btn.setToolTip('This will end the program')     #popup words on hover
		# btn.clicked.connect(QCoreApplication.instance().quit) #make button close app
		# btn.resize(btn.sizeHint())
		# btn.move(50,50)

		self.recip = QLineEdit(self,placeholderText='Recipient')
		self.recip.setObjectName("RecipientEnter")
		self.recip.setGeometry(50,50,200,20)

		self.msg = QPlainTextEdit(self, placeholderText='Message')
		self.msg.setObjectName("MessageEnter")
		self.msg.setGeometry(50, 100, 400, 100)

		self.btnSend = QPushButton('Enter', self)
		self.btnSend.clicked.connect(self.send)
		self.btnSend.move(50,200)


		self.show()

	def send(self):
		rec = self.recip.text()
		message = self.msg.toPlainText()
		SendMessage3.send(rec, message)

class newclass(QWidget):
	def __init__(self,parent=None):
		super().__init__()
		self.initUI()
        
	def initUI(self):	
		None

class CheckTab(QWidget):
	def __init__(self,parent=None):
		super().__init__()
		self.initUI()

	def initUI(self):
		letemknow= QLabel('New Messages')
		letemknow.setAlignment(QtCore.Qt.AlignCenter)
		
		data = ReceivedMessage3.checkMsgs()

		results = QTextEdit()
		results.setReadOnly(True)
		
		msgs=""
		for msg in data:
			msgs+=(msg[0]+':\n'+msg[1]+'\n\n')
		
		if data == []:
			results.setText('No messages')
			results.setAlignment(QtCore.Qt.AlignCenter)
		else:
			results.setText(msgs)

		hbox1 = QHBoxLayout()
		hbox1.addWidget(letemknow)
		hbox2 = QHBoxLayout()
		# if i==0:
		# 	hbox2.addWidget(QLabel('No New Messages'))
		# else:
		# 	hbox2.addWidget(msgTable)

		hbox2.addWidget(results)
		vbox = QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)		

		
		self.setLayout(vbox)

class NewContact(QWidget):
	def __init__(self,parent=None):
		super().__init__()
		self.initUI()

	def initUI(self):
		None





if __name__=='__main__':

	app = QApplication(sys.argv)  #new app w sys args
	ex = DTexting()      #new class ^
	sys.exit(app.exec_())   #start app and ensure clean close
