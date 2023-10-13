#!/usr/bin/python
#   ____                   ____       _
#  / ___|_ __ _____      _|  _ \ __ _| |
# | |  _| '__/ _ \ \ /\ / / |_) / _` | |
# | |_| | | | (_) \ V  V /|  __/ (_| | |
#  \____|_|  \___/ \_/\_/ |_|   \__,_|_|
#
#
#
# Please go through the README file before execution 
#
# -------------------------------------------------------Import statements------------------------------------------------------- #
from msilib.schema import Error
from email.mime.text import MIMEText
import sys
import os
import requests
# pip install PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QDialog, QApplication, QMainWindow, QLineEdit, QWidget, QFileDialog, QLabel,QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream, QSize
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import *
from dns.message import Message
from validate_email import validate_email
# pip install validate_email
import mysql.connector
# pip install mysql-connector
# pip install pandas
from pandas.core.common import flatten
from imagekitio import ImageKit
# pip install imagekitio
import urllib
#pip install qdarkstyle
import qdarkstyle
import smtplib
from email.mime.multipart import MIMEMultipart
import random
from dotenv import load_dotenv
import re
import html
import firebase_admin
from firebase_admin import credentials, storage
from google.cloud import storage as gcs

# Initialize Firebase with your project's credentials
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-bucket-name.appspot.com'
})

# Get a reference to the Firebase Storage bucket
bucket = storage.bucket()

# Get the file input from the user
file_input = input("Enter the path to the image file: ")

# Upload the selected image file
blob = bucket.blob("images/" + file_input.split("/")[-1])
blob.upload_from_filename(file_input)

# Get the download URL
url = blob.public_url

# Display the image
print(f'<img src="{url}">')

# -------------------------------------------------------Variables and Misc.------------------------------------------------------- #

print(r''' _        ___       _      ____    ___   _   _    ____             
| |      / _ \     / \    |  _ \  |_ _| | \ | |  / ___|            
| |     | | | |   / _ \   | | | |  | |  |  \| | | |  _             
| |___  | |_| |  / ___ \  | |_| |  | |  | |\  | | |_| |  _   _   _
|_____|  \___/  /_/   \_\ |____/  |___| |_| \_|  \____| (_) (_) (_)
''')
global loginpage_details
loginpage_details = []
global register_page_email
global register_page_password
global listedItems
global logged_in_username
logged_in_username = ''
global logged_in_password
logged_in_password = ''
listedItems = {}
global price
price = 0
global givenFile
givenFile = ''
global product_name_listed
product_name_listed = ''
global product_price_listed
product_price_listed = ''
global product_description_listed
product_description_listed = ''
global db
load_dotenv()

growpal_email = os.getenv("growpal_email")
imgkit_pub = os.getenv("imgkit_pub")
imgkit_priv = os.getenv("imgkit_priv")
sql = os.getenv("sql")

try:
    db = mysql.connector.connect(host='localhost', user = 'root', passwd = 'PUT YOUR PASSWORD HERE', database = 'growpal')
    print("Successfully Connected To Local SQL Server") 
except:
    try: 
        db = mysql.connector.connect(host= 'db4free.net', user = 'growpal', passwd = sql, database = 'growpal')
        print("Successfully Connected To Online Server") 

    except: print("Error Connecting to SQL Server")

try:
    global server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('system.growpal@gmail.com', growpal_email)
    print("Successfully Connected To SMTP Gmail Server")
except:
    print('Something went wrong with mail server')

global curs
curs = db.cursor()
def getLoginDetails():
    global loginpage_details
    curs.execute('select username, password from login_details')
    loginpage_details = curs.fetchall()
    loginpage_details = list(flatten(loginpage_details))

getLoginDetails()

imagekit = ImageKit(
        private_key = imgkit_priv,
        public_key= imgkit_pub,
        url_endpoint = 'https://ik.imagekit.io/bule8zjn18b'
)



# -------------------------------------------------------Class declaration for all pages------------------------------------------------------- #
# -------------------------------------------------------loginregisterpage------------------------------------------------------- #


class loginregisterpage(QMainWindow):
    def __init__(self):
        super(loginregisterpage, self).__init__()
        loadUi("assets/loginRegisterPage.ui", self)
        self.setWindowTitle("GrowPal")
        self.login_button.clicked.connect(self.gotologin_page)
        self.register_button.clicked.connect(self.gotoregister_page)

    def gotologin_page(self):
        widget.setCurrentIndex(1)

    def gotoregister_page(self):
        widget.setCurrentIndex(2)


# -------------------------------------------------------login_page------------------------------------------------------- #
class login_page(QMainWindow):
    def __init__(self):
        super(login_page, self).__init__()
        loadUi("assets/loginPage.ui", self)
        self.pushButton_back.clicked.connect(self.back_button_pressed)
        self.pushbutton_login.clicked.connect(self.login_button_pressed)
        self.password_view.clicked.connect(self.pass_view_clicked)
        self.shortcut_login = QShortcut(QKeySequence('return'), self)
        self.shortcut_login.activated.connect(self.login_button_pressed)
        self.pushButton_forgot.clicked.connect(self.go_to_forgot)
        global logged_in_username
        global logged_in_password
        logged_in_username = ''
        logged_in_password = ''
        self.icon = QIcon('assets/visiblity.svg')
        self.password_view.setIcon(self.icon)

    def go_to_forgot(self):
        widget.setCurrentIndex(13)
        self.lineEdit_password.setText('')
    def pass_view_clicked(self):
        if self.password_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)

            self.icon = QIcon('assets/visiblity_off.svg')
            self.password_view.setIcon(self.icon)

        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            
            self.icon = QIcon('assets/visiblity.svg')
            self.password_view.setIcon(self.icon)




    def back_button_pressed(self):
        widget.setCurrentIndex(0)
        self.lineEdit_password.setText('')


    def login_button_pressed(self):
        getLoginDetails()
        t=self.lineEdit_username.text();
        m=self.lineEdit_password.text() == ""
        if t == "" or m == "":

            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Empty Fields')
            error_dialog.showMessage("Please fill all the fields")
        else:
            if self.lineEdit_username.text() in loginpage_details:
                if self.lineEdit_password.text() == loginpage_details[loginpage_details.index(self.lineEdit_username.text()) + 1]:
                    global logged_in_username
                    global logged_in_password
                    logged_in_username = self.lineEdit_username.text()
                    loggin_in_password = self.lineEdit_password.text()
                    self.lineEdit_username.setText("")
                    self.lineEdit_password.setText("")
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                    error_dialog.setWindowTitle('Welcome')
                    error_dialog.showMessage(
                        f"Welcome back {logged_in_username}!")
                    widget.setCurrentIndex(3)
                    Items.loadData()
                    orders.loadData()
                    #buy_page.loadData()
                else:
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                    error_dialog.setWindowTitle('Password')
                    error_dialog.showMessage(
                        'Incorrect password, please try again')
                    self.lineEdit_password.setText("")
            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                error_dialog.setWindowTitle('Account')
                error_dialog.showMessage('Please create an account')
                self.lineEdit_username.setText("")
                self.lineEdit_password.setText("")
                widget.setCurrentIndex(2)






# -------------------------------------------------------Forgot Page------------------------------------------------------- #
class forgot(QMainWindow):
    def __init__(self):
        super(forgot, self).__init__()
        loadUi("assets/forgot.ui", self)
        self.pushButton_back.clicked.connect(self.back_button_pressed)
        self.pushbutton_send.clicked.connect(self.send_button_pressed)
        self.shortcut_send = QShortcut(QKeySequence('return'), self)
        self.shortcut_send.activated.connect(self.send_button_pressed)
        
        curs.execute("select email from login_details;")
        self.emails = curs.fetchall()
        self.emails = list(flatten(self.emails))
    def back_button_pressed(self):
        widget.setCurrentIndex(1)

    def send_button_pressed(self):

        if self.lineEdit_email.text() in self.emails:
            valid = validate_email(self.lineEdit_email.text())
            if valid:
                curs.execute(f"select username, password from login_details where email = '{self.lineEdit_email.text()}'")
            else: raise Exception("Invalid email")
            self.to_send = curs.fetchall()
            # If one email ID has multiple accounts.
            for entry in self.to_send:
                msg = "\r\n".join([
                "From: system.growpal@gmail.com",
                f"To: {self.lineEdit_email.text()}",
                "Subject: Forgot Credentials",
                "",
                f'''Hi! We heard you forgot your credentials. We are here to help. Here are your login details:
                Username: {entry[0]}
                Password: {entry[1]}
Regards
Team GrowPal'''
                ])
                
                server.sendmail('system.growpal@gmail.com', self.lineEdit_email.text(), msg)
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Mail')
            error_dialog.showMessage("We have sent your credentials to your email ID.")
            self.back_button_pressed()
        else:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Mail')
            error_dialog.showMessage("email ID does not exist in the database. Please check once again.")





# -------------------------------------------------------register_page------------------------------------------------------- #
class register_page(QMainWindow):
    def __init__(self):
        super(register_page, self).__init__()
        loadUi("assets/registerPage.ui", self)
        self.pushButton_back.clicked.connect(self.back_button_clicked)
        self.pushbutton_register.clicked.connect(self.register_button_clicked)
        self.sp_view.clicked.connect(self.sp_view_clicked)
        self.cp_view.clicked.connect(self.cp_view_clicked)
        self.shortcut_register = QShortcut(QKeySequence('return'), self)
        self.shortcut_register.activated.connect(self.register_button_clicked)
        self.pushButton_otp.clicked.connect(self.otp_button_clicked)

        self.ispicon = QIcon('assets/visiblity.svg')
        self.sp_view.setIcon(self.ispicon)
        self.icpicon = QIcon('assets/visiblity.svg')
        self.cp_view.setIcon(self.icpicon)




    def otp_button_clicked(self):

        

        self.otp = random.randint(100000, 999999)
      
        msg=MIMEMultipart('alternative')
        msg['Subject']="Verification [NO REPLY]"
        msg['From']="system.growpal@gmail.com"
        msg['To']=self.lineEdit_email.text()
#         h=f'''\
#             <html>
#     <head>
#         <style>
#             p{
#                 "background-color":#54BAB9;
#             }
#         </style>
#     </head>
#     <body>
#         <div >
#             <p>Your verification code is: {self.otp}. Please DO NOT share it with anybody. GrowPal never calls you for any reason</p>
            
#         </div>
#     </body>
# </html>'''
        h='''<!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
<!--[if !mso]><!-->
<link href="https://fonts.googleapis.com/css?family=Droid+Serif" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Fira+Sans" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Permanent+Marker" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Shrikhand" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Abril+Fatface" rel="stylesheet" type="text/css"/>
<!--<![endif]-->
<style>
		* {
			box-sizing: border-box;
		}

		body {
			margin: 0;
			padding: 0;
		}

		a[x-apple-data-detectors] {
			color: inherit !important;
			text-decoration: inherit !important;
		}

		#MessageViewBody a {
			color: inherit;
			text-decoration: none;
		}

		p {
			line-height: inherit
		}

		.desktop_hide,
		.desktop_hide table {
			mso-hide: all;
			display: none;
			max-height: 0px;
			overflow: hidden;
		}

		@media (max-width:700px) {

			.desktop_hide table.icons-inner,
			.social_block.desktop_hide .social-table {
				display: inline-block !important;
			}

			.icons-inner {
				text-align: center;
			}

			.icons-inner td {
				margin: 0 auto;
			}

			.fullMobileWidth,
			.image_block img.big,
			.row-content {
				width: 100% !important;
			}

			.mobile_hide {
				display: none;
			}

			.stack .column {
				width: 100%;
				display: block;
			}

			.mobile_hide {
				min-height: 0;
				max-height: 0;
				max-width: 0;
				overflow: hidden;
				font-size: 0px;
			}

			.desktop_hide,
			.desktop_hide table {
				display: table !important;
				max-height: none !important;
			}
		}
	</style>
</head>
<body style="background-color: #f3e2e2; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f3e2e2;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5b7b7a; background-position: center top;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
<tbody>
<tr>
<td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="vertical-align: middle; color: #000000; font-family: inherit; font-size: 14px; text-align: center; padding-top: 25px;">
<table align="center" cellpadding="0" cellspacing="0" class="alignment" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
<tr>

</tr>
</table>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="center" class="alignment" style="line-height:10px"></div>
</td>
</tr>
</table>
<table border="0" cellpadding="10" cellspacing="0" class="heading_block block-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad">
<h1 style="margin: 0; color: #ffffff; direction: ltr; font-family: 'Abril Fatface', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-size: 51px; font-weight: normal; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;">Your verification code is:  '''+str(self.otp)+'''<br> Please DO NOT share it with anybody. GrowPal never calls you for any reason</h1>
</td>
</tr>
</table>
<table border="0" cellpadding="10" cellspacing="0" class="text_block block-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 14px; mso-line-height-alt: 16.8px; color: #d6d6d6; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">

</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="button_block block-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:90px;padding-left:10px;padding-right:10px;padding-top:10px;text-align:center;">
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
<tbody>
<tr>
<td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:45px;line-height:45px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
<tbody>
<tr>
<td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="heading_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:5px;padding-left:10px;padding-right:10px;padding-top:10px;text-align:center;width:100%;">

</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="heading_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:10px;text-align:center;width:100%;">
<h1 style="margin: 0; color: #171719; direction: ltr; font-family: 'Abril Fatface', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-size: 40px; font-weight: normal; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;">Regards,thanks</h1>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:10px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 14px; mso-line-height-alt: 21px; color: #393d47; line-height: 1.5; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
<p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;">Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu</p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="center" class="alignment" style="line-height:10px"></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
<tbody>
<tr>
<td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:55px;line-height:55px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
<tbody>
<tr>
<td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="50%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:5px;padding-bottom:5px;">
<div align="center" class="alignment" style="line-height:10px"></div>
</td>
</tr>
</table>
</td>
<td class="column column-2" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="50%">
<table border="0" cellpadding="0" cellspacing="0" class="heading_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>



</body>
</html>'''
        m1=MIMEText(h,'html')
        msg.attach(m1)

        # msg = "\r\n".join([
        #     "From: system.growpal@gmail.com",
        #     f"To: {self.lineEdit_email.text()}",
        #     "Subject: Verification [NO REPLY]",
        #     "",m1
#             
# #            f'''Your verification code is: {self.otp}. Please DO NOT share it with anybody. GrowPal never calls you for any reason
            
# Regards
# Team GrowPal'''
     #       ])
        server.sendmail('system.growpal@gmail.com', self.lineEdit_email.text(), msg.as_string())
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('OTP')
        error_dialog.showMessage("Please check your mail inbox for the OTP")





    def sp_view_clicked(self):
        if self.sp_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
            self.iconsp = QIcon('assets/visiblity_off.svg')
            self.sp_view.setIcon(self.iconsp)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            self.iconsp = QIcon('assets/visiblity.svg')
            self.sp_view.setIcon(self.iconsp)

    def cp_view_clicked(self):
        if self.cp_view.isChecked():
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Normal)

            self.iconcp = QIcon('assets/visiblity_off.svg')
            self.cp_view.setIcon(self.iconcp)
        else:
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Password)
            self.iconcp = QIcon('assets/visiblity.svg')
            self.cp_view.setIcon(self.iconcp)

    def back_button_clicked(self):
        widget.setCurrentIndex(0)
        self.lineEdit_password.setText('')
        self.lineEdit_repeatpassword.setText('')


    def register_button_clicked(self):

        if self.lineEdit_username.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_phnumber.text() == "" or self.lineEdit_password.text() == "" or self.lineEdit_repeatpassword.text() == "":
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Empty Fields')
            error_dialog.showMessage("Please fill all the fields")
        elif len(self.lineEdit_phnumber.text()) != 10:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Phone Number')
            error_dialog.showMessage('Please enter a valid phone number')
            self.lineEdit_phnumber.setText("")

        elif self.lineEdit_password.text() != self.lineEdit_repeatpassword.text():
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Password')
            error_dialog.showMessage('Your passwords do not match. Try again.')
            self.lineEdit_password.setText("")
            self.lineEdit_repeatpassword.setText("")


        elif self.lineEdit_otp.text() == '':
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('OTP')
            error_dialog.showMessage('Please enter OTP')


        elif self.lineEdit_password.text() == self.lineEdit_repeatpassword.text():
            if validate_email(self.lineEdit_email.text()):
                if self.lineEdit_username.text() not in loginpage_details:
                    

                    if int(self.lineEdit_otp.text()) == self.otp: 




                        sep=[" ","-","."]  
                        if sep not in self.lineEdit_username.text().split():


                            curs.execute(f"insert into login_details values('{self.lineEdit_username.text()}', '{self.lineEdit_password.text()}', '{self.lineEdit_email.text()}', '{self.lineEdit_phnumber.text()}')")
                        else :
                            raise Exception ("sql injection");

                        db.commit()
                        getLoginDetails()
                        self.lineEdit_username.setText('')
                        self.lineEdit_email.setText('')
                        self.lineEdit_phnumber.setText('') 
                        self.lineEdit_password.setText("")
                        self.lineEdit_repeatpassword.setText("")
                        error_dialog = QtWidgets.QErrorMessage(self)
                        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                        error_dialog.setWindowTitle('Thanks!')
                        error_dialog.showMessage(
                            'Thanks for creating an account with us! Please login with the same credentials')
                        widget.setCurrentIndex(1)



                    else:
                        error_dialog = QtWidgets.QErrorMessage(self)
                        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                        error_dialog.setWindowTitle('OTP')
                        error_dialog.showMessage(
                        'OTP Incorrect')

                else:
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                    error_dialog.setWindowTitle('Account')
                    error_dialog.showMessage(
                        'Username already exists.')
                    widget.setCurrentIndex(1)

            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                error_dialog.setWindowTitle('Email')
                error_dialog.showMessage('Please enter a valid email ID')
                self.lineEdit_email.setText("")


# -------------------------------------------------------buy_page------------------------------------------------------- #
class buy_page(QMainWindow):

    def __init__(self) -> None:
        super(buy_page, self).__init__()
        loadUi("assets/buy_page.ui", self)
        self.pushButton_logout.clicked.connect(self.are_you_sure)
        self.pushButton_sell.clicked.connect(self.gotoSellPage)
        global price
        global item
        self.pushButton_orders.clicked.connect(self.go_to_orders)
        self.pushButton_selling_items.clicked.connect(self.go_to_items)
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 200)
        self.loadData()
        self.search_button.clicked.connect(self.loadFromSearch)
        self.search_bar.textChanged.connect(self.empty)
        self.shortcut_search = QShortcut(QKeySequence('return'), self)
        self.shortcut_search.activated.connect(self.loadFromSearch)
        self.tableWidget.selectionModel().selectionChanged.connect(self.selection)

        self.tableWidget.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    
    
    def selection(self, selected):
        for ix in selected.indexes():
            global row 
            global column 
            row = ix.row()
            column = ix.column()
            global price 
            global item
            global picture 
            global item_ID
            
            item_ID = self.tableWidget.item(row, 0).text()
            
            price = self.tableWidget.item(row, 3).text()
            item = self.tableWidget.item(row, 2).text()
            
            curs.execute(f"select product_image_address from listed_items where item_id = {item_ID};")
            picture = curs.fetchone()
            picture = list(picture)
            picture = str(picture[0])
            transactionPage.setPrice()
            self.go_to_transactions()

    def go_to_transactions(self):
        widget.setCurrentIndex(5)
        self.tableWidget.clearSelection()


    def go_to_items(self):
        widget.setCurrentIndex(11)




    def go_to_orders(self):
        widget.setCurrentIndex(10)


    def logout(self):
        widget.setCurrentIndex(0)

    def gotoSellPage(self):

        # self.label_prod_img2.setPixmap(self.pixmap)
        widget.setCurrentIndex(4)
    



    def loadData(self):

        global logged_in_username 
        curs.execute(f"select product_name, product_price, product_description, product_image_address, item_id from listed_items where deleted = 'False';")
        listed_items = curs.fetchall()
    
        row = 0
        self.tableWidget.setRowCount(len(listed_items))
        for item in listed_items:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[4])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item[0]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(item[2]))
            self.image = QtWidgets.QLabel(self.centralwidget)
            self.image.setText('')
            self.image.setScaledContents(True)
            self.data = urllib.request.urlopen(item[3]).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.pixmap = self.pixmap.scaled(250, 250)
            self.image.setPixmap(self.pixmap)
            self.tableWidget.setCellWidget(row, 1, self.image)
            self.image.setHidden(True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(250)
            row = row + 1
    


    def empty(self):
        if self.search_bar.text() == '':
            self.loadData()

    def loadFromSearch(self):
        self.search_criteria = self.search_bar.text()
        if self.search_criteria == '':
            self.loadData()

        else:

            curs.execute(f"select product_name, product_price, product_description, product_image_address, item_id from listed_items")
            listed_items = curs.fetchall()
            filtered = 0
            for i in listed_items:
                if self.search_criteria.lower() in i[0].lower():
                    filtered +=1

            if filtered == 0: 
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
                error_dialog.setWindowTitle('Search')
                error_dialog.showMessage("Oopsie, no results found :(")
                
            else:
                row = 0
                self.tableWidget.setRowCount(0)
                self.tableWidget.setRowCount(len(listed_items))
                for item in listed_items:
                    if self.search_criteria.lower() in item[0].lower():
                        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[4])))
                        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item[0]))
                        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item[1]))
                        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(item[2]))



                        self.image = QtWidgets.QLabel(self.centralwidget)
                        self.image.setText('')
                        self.image.setScaledContents(True)
                        self.data = urllib.request.urlopen(item[3]).read()
                        self.pixmap = QPixmap()
                        self.pixmap.loadFromData(self.data)
                        self.pixmap = self.pixmap.scaled(250, 250)
                        self.image.setPixmap(self.pixmap)
                        self.tableWidget.setCellWidget(row, 1, self.image)
                        self.image.setHidden(True)
                        self.tableWidget.verticalHeader().setDefaultSectionSize(250)
                        row = row + 1




    def are_you_sure(self):
        msg = QMessageBox()
        msg.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        msg.setWindowTitle("Logout")
        msg.setText("Are you sure?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()

    def popup_button(self, button):
        button_pressed = button.text()

        if button_pressed == '&Yes':
            self.logout()

        else:
            pass


# -------------------------------------------------------sellPage------------------------------------------------------- #
class sellPage(QMainWindow):
    def __init__(self) -> None:
        super(sellPage, self).__init__()
        loadUi("assets/sellPage.ui", self)
        self.pushButton_back.clicked.connect(self.getback)
        self.pushButton_UploadImages.clicked.connect(self.upload)
        self.pushButton_Sell.clicked.connect(self.sell)
        global logged_in_username


    def getback(self):
        widget.setCurrentIndex(3)

    def upload(self):
        sellPage.file = QFileDialog.getOpenFileName(self, 'Browse')
        self.label_browse.setText(sellPage.file[0])

        global givenFile
        givenFile = sellPage.file[0]
        if givenFile == '':
            givenFile = 'https://ik.imagekit.io/bule8zjn18b/ina.jpeg'

            self.data = urllib.request.urlopen(givenFile).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.label_picture.setScaledContents(True)
            self.pixmap = self.pixmap.scaled(190, 212)
            self.label_picture.setPixmap(self.pixmap)
        


        else:
            self.pixmap = QPixmap(givenFile)
            self.pixmap = self.pixmap.scaled(190, 212)
            self.label_picture.setScaledContents(True)
            self.label_picture.setPixmap(self.pixmap)

        
    def sell(self):
        if self.lineEdit_prod_name.text() == "" or self.lineEdit_price.text() == "" or self.lineEdit_description.text() == "" or self.lineEdit_name.text == "" or self.lineEdit_cont_num.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_address.text() == "" or self.lineEdit_upi_id == "":
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Empty Fields')
            error_dialog.showMessage("Please fill all the fields")

        elif(not validate_email(self.lineEdit_email.text())):
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Invalid Email')
            error_dialog.showMessage("Please enter a valid email ID.")

        elif(self.label_browse.text() == ''):
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Image')
            error_dialog.showMessage("Please upload an image of the product.")



        else:
            sellPage.given_prod_name = self.lineEdit_prod_name.text()
            sellPage.given_price = self.lineEdit_price.text()
            sellPage.given_description = self.lineEdit_description.text()
            sellPage.given_name = self.lineEdit_name.text()
            sellPage.given_cont_num = self.lineEdit_cont_num.text()
            sellPage.given_email = self.lineEdit_email.text()
            sellPage.given_address = self.lineEdit_address.text()
            sellPage.given_upi_id = self.lineEdit_upi_id.text()
            self.lineEdit_prod_name.setText('')
            self.lineEdit_price.setText('')
            self.lineEdit_description.setText('')
            self.lineEdit_name.setText('')
            self.lineEdit_cont_num.setText('')
            self.lineEdit_email.setText('')
            self.lineEdit_address.setText('')
            self.lineEdit_upi_id.setText('')
            self.label_browse.setText('')
            self.label_picture.clear()
            global logged_in_username
            global imagekit_url


            curs.execute("select product_name from listed_items")
            num = curs.fetchall()
            num = len(list(num))
            num = num  + 1 
            num = str(num)
            upload = imagekit.upload(
                file= open(givenFile, "rb"), 
                file_name= num+".jpeg", 
                options = {"use_unique_file_name" : False }
                )       
            global imagekit_url
            imagekit_url = imagekit.url({
                "path": num + ".jpeg",
                "url_endpoint" : "https://ik.imagekit.io/bule8zjn18b/"
                }
                )
            curs.execute("select item_id_num from numbers")
            item_id = int(curs.fetchone()[0])
            item_id += 1
            if f"insert into listed_items values('{sellPage.given_prod_name}', '{sellPage.given_price}', '{sellPage.given_description}', '{logged_in_username}', '{sellPage.given_name}', '{sellPage.given_cont_num}', '{sellPage.given_email}','{sellPage.given_address}', '{sellPage.given_upi_id}', '{str(imagekit_url)}', 'False', {item_id});
            curs.execute(f"update numbers set item_id_num = {item_id} where item_id_num = {item_id - 1}")
            db.commit()
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))


            error_dialog.setWindowTitle('Sell')
            error_dialog.showMessage(
                f"Your product {sellPage.given_prod_name} is now listed for {sellPage.given_price} rupees")
            widget.setCurrentIndex(3)
            buy_page.loadData()
            Items.loadData()



# -------------------------------------------------------Transaction Page------------------------------------------------------- #


class transactionPage(QMainWindow):
    def __init__(self) -> None:
        super(transactionPage, self).__init__()
        loadUi("assets/transaction.ui", self)
        global price
        global item
        self.pushButton_cc.clicked.connect(self.creditcard)
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_dc.clicked.connect(self.debitcard)

        self.pushButton_upi.clicked.connect(self.upi)


        self.pushButton_netbank.clicked.connect(self.netbank)


    def go_back(self):
        widget.setCurrentIndex(3)

    def creditcard(self):
        widget.setCurrentIndex(6)

    def debitcard(self):
        widget.setCurrentIndex(7)

    def upi(self):
        widget.setCurrentIndex(8)

    def netbank(self):
        widget.setCurrentIndex(9)

    def setPrice(self):
        global picture

        self.data = urllib.request.urlopen(picture).read()
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.data)
        self.pixmap = self.pixmap.scaled(256, 171)
        self.label_picture.setPixmap(self.pixmap)
        self.label_ammount.setText(f'''Item: {item}
Amount: {price}''')




# -------------------------------------------------------Transaction - Credit Card------------------------------------------------------- #

class creditCard(QMainWindow):
    def __init__(self) -> None:
        super(creditCard, self).__init__()
        loadUi("assets/transaction_cc.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

        

    def pay(self):
        global price
        global item
        global logged_in_username
        global picture
        curs.execute("select order_id_num from numbers")
        order_id = int(curs.fetchone()[0])
        order_id += 1
        curs.execute(f"insert into credit_card_transactions values('{logged_in_username}','{item}', '{price}', '{self.lineEdit_cnum.text()}', '{self.lineEdit_cvv.text()}', '{self.lineEdit_del_add.text()}', '{picture}', {order_id}, 'False')")
        curs.execute(f'''update numbers set order_id_num = {order_id} where order_id_num = {order_id - 1}''')
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')
        transactionPage.go_back()
        curs.execute(f"select email from login_details where username = '{logged_in_username}'")
        send_to_email = curs.fetchone()
        send_to_email = str(send_to_email[0])
        msg = "\r\n".join([
                "From: system.growpal@gmail.com",
                f"To: {send_to_email}",
                f"Subject: Order: {order_id} [NO REPLY]",
                "",
                f'''Dear Customer, 
Thank you for shopping with us. We have received your order for {item} with order ID: {order_id}.  We pledge to provide you with the best possible shopping experience. Thank you again for making it possible.

Regards
Team GrowPal  '''
                ])
        server.sendmail('system.growpal@gmail.com', send_to_email, msg)

        orders.loadData()






# -------------------------------------------------------Transaction - Debit Card------------------------------------------------------- #

class debitCard(QMainWindow):
    def __init__(self) -> None:
        super(debitCard, self).__init__()
        loadUi("assets/transaction_dc.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

        

    def pay(self):
        global price
        global item
        global logged_in_username
        global picture
        curs.execute("select order_id_num from numbers")
        order_id = int(curs.fetchone()[0])
        order_id += 1
        curs.execute(f"insert into debit_card_transactions values('{logged_in_username}', '{item}', '{price}','{self.lineEdit_dnum.text()}', '{self.lineEdit_cvv.text()}', '{self.lineEdit_del_add.text()}', '{picture}',{order_id}, 'False')")
        curs.execute(f'''update numbers set order_id_num = {order_id} where order_id_num = {order_id - 1}''')
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()

        curs.execute(f"select email from login_details where username = '{logged_in_username}'")
        send_to_email = curs.fetchone()
        send_to_email = str(send_to_email[0])
        msg = "\r\n".join([
                "From: system.growpal@gmail.com",
                f"To: {send_to_email}",
                f"Subject: Order: {order_id} [NO REPLY]",
                "",
                f'''Dear Customer, 
Thank you for shopping with us. We have received your order for {item} with order ID: {order_id}.
We pledge to provide you with the best possible shopping experience. Thank you again for making it possible.

Regards
Team GrowPal  '''
                ])
        server.sendmail('system.growpal@gmail.com', send_to_email, msg)
        orders.loadData()





# -------------------------------------------------------Transaction - UPI------------------------------------------------------- #

class upi(QMainWindow):
    def __init__(self) -> None:
        super(upi, self).__init__()
        loadUi("assets/transaction_upi.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)


    def pay(self):
        global price
        global item
        global logged_in_username
        global picture
        curs.execute("select order_id_num from numbers")
        order_id = int(curs.fetchone()[0])
        order_id += 1
        curs.execute(f"insert into upi_transactions values('{logged_in_username}', '{item}', '{price}', '{self.lineEdit_upinum.text()}', '{self.lineEdit_del_add.text()}', '{picture}',{order_id}, 'False')")
        curs.execute(f'''update numbers set order_id_num = {order_id} where order_id_num = {order_id - 1}''')
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()
        curs.execute(f"select email from login_details where username = '{logged_in_username}'")
        send_to_email = curs.fetchone()
        send_to_email = str(send_to_email[0])
        msg = "\r\n".join([
                "From: system.growpal@gmail.com",
                f"To: {send_to_email}",
                f"Subject: Order: {order_id} [NO REPLY]",
                "",
                f'''Dear Customer, 
Thank you for shopping with us. We have received your order for {item} with order ID: {order_id}.  We pledge to provide you with the best possible shopping experience. Thank you again for making it possible.

Regards
Team GrowPal  '''
                ])
        server.sendmail('system.growpal@gmail.com', send_to_email, msg)
        orders.loadData()
# -------------------------------------------------------Transaction - NetBanking------------------------------------------------------- #

class netBank(QMainWindow):
    def __init__(self) -> None:
        super(netBank, self).__init__()
        loadUi("assets/transaction_netbank.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)


    def pay(self):
        global price
        global item
        global logged_in_username
        global picture
        curs.execute("select order_id_num from numbers")
        order_id = int(curs.fetchone()[0])
        order_id += 1
        curs.execute(f"insert into net_bank_transactions values('{logged_in_username}', '{item}', '{price}','{self.lineEdit_acnum.text()}', '{self.lineEdit_cifnum.text()}', '{self.lineEdit_branch_code.text()}', '{self.lineEdit_del_add.text()}', '{picture}', {order_id},'False')")
        curs.execute(f'''update numbers set order_id_num = {order_id} where order_id_num = {order_id - 1}''')
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()
        curs.execute(f"select email from login_details where username = '{logged_in_username}'")
        send_to_email = curs.fetchone()
        send_to_email = str(send_to_email[0])
        msg = "\r\n".join([
                "From: system.growpal@gmail.com",
                f"To: {send_to_email}",
                f"Subject: Order: {order_id} [NO REPLY]",
                "",
                f'''Dear Customer, 
Thank you for shopping with us. We have received your order for {item} with order ID: {order_id}.  We pledge to provide you with the best possible shopping experience. Thank you again for making it possible.

Regards
Team GrowPal  '''
                ])
        server.sendmail('system.growpal@gmail.com', send_to_email, msg)
        orders.loadData()

# -------------------------------------------------------Orders------------------------------------------------------- #

class orders(QMainWindow):
    def __init__(self) -> None:
        super(orders, self).__init__()
        loadUi("assets/orders.ui", self)
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.loadData()
        self.pushButton_back.clicked.connect(self.go_back)
        self.tableWidget.selectionModel().selectionChanged.connect(self.selection)
        self.tableWidget.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 150)

    def go_back(self):
        widget.setCurrentIndex(3)

    def loadData(self):
        global logged_in_username


        curs.execute(f"select item, price, flat_number, image_url, order_id from credit_card_transactions where username = '{logged_in_username}' and deleted = 'False' union all select item, price, flat_number, image_url, order_id from debit_card_transactions where username = '{logged_in_username}' and deleted = 'False' union all select item, price, flat_number, image_url, order_id from upi_transactions where username = '{logged_in_username}' and deleted = 'False' union all select item, price, flat_number, image_url, order_id from net_bank_transactions where username = '{logged_in_username}' and deleted = 'False';")



        order_list = curs.fetchall()
        row = 0
        self.tableWidget.setRowCount(len(order_list))
        for order in order_list:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(order[4])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(order[0]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(order[1]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(order[2]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("   Cancel"))
            
            self.image = QtWidgets.QLabel(self.centralwidget)
            self.image.setText('')
            self.image.setScaledContents(True)
            self.data = urllib.request.urlopen(order[3]).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.pixmap = self.pixmap.scaled(200, 200)
            self.image.setPixmap(self.pixmap)
            self.tableWidget.setCellWidget(row, 2, self.image)
            self.image.setHidden(True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(200)






            row = row + 1



    def selection(self, selected):
        for ix in selected.indexes():
            msg = QMessageBox()
            msg.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            msg.setWindowTitle("Cancel")
            msg.setText("Are you sure you want to cancel this order?")
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            global item_name_selected 
            global logged_in_username
            self.row_listed = ix.row()
            self.column_listed = ix.column()
            msg.buttonClicked.connect(self.msgbutton)
            x = msg.exec_()



    def msgbutton(self, button):
        if button.text() == "&Yes":
    

            order_id_selected = int(self.tableWidget.item(self.row_listed, 0).text())
    
    
            curs.execute(f'''select order_id, "credit_card_transactions" from credit_card_transactions where order_id = {order_id_selected} union all select order_id, "debit_card_transactions" from debit_card_transactions where order_id = {order_id_selected} union all select order_id, "upi_transactions" from upi_transactions where order_id = {order_id_selected} union all select order_id, "net_bank_transactions"  from net_bank_transactions where order_id = {order_id_selected};''')
            search_list = curs.fetchall()
    

            for i in search_list:
                if order_id_selected == i[0]:
                    item_table = i[1]
                    break
    
            curs.execute(f'''update {item_table} set deleted = "True" where order_id = {order_id_selected};''')
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            error_dialog.setWindowTitle('Cancel')
            error_dialog.showMessage("Your order has been cancelled")
            self.tableWidget.clearSelection()
            self.loadData()
        else:
            self.tableWidget.clearSelection()



    

# -------------------------------------------------------Items------------------------------------------------------- #
class Items(QMainWindow):
    def __init__(self) -> None:
        super(Items, self).__init__()
        
        loadUi("assets/sold_items.ui", self)
        self.loadData()
        self.pushButton_back.clicked.connect(orders.go_back)
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.selectionModel().selectionChanged.connect(self.selection)
        self.tableWidget.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

        self.tableWidget.setColumnWidth(1, 100)



    def loadData(self):
        global logged_in_username 
        curs.execute(f"select product_image_address, product_name, product_price, product_description, item_id from listed_items where seller_username = '{logged_in_username}' and deleted = 'False';")
        listed_items = curs.fetchall()
    
        row = 0
        self.tableWidget.setRowCount(len(listed_items))
        for item in listed_items:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[4])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("   EDIT"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(item[2]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(item[3]))

            self.image = QtWidgets.QLabel(self.centralwidget)
            self.image.setText('')
            self.image.setScaledContents(True)

            self.data = urllib.request.urlopen(item[0]).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.pixmap = self.pixmap.scaled(200, 200)
            self.image.setPixmap(self.pixmap)
            self.tableWidget.setCellWidget(row, 2, self.image)
            self.image.setHidden(True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(200)



            row = row + 1

    def selection(self, selected):
        for ix in selected.indexes():
            global row_listed 
            global column_listed
            row_listed = ix.row()
            column_listed = ix.column()
            global product_name_listed
            global product_price_listed
            global product_description_listed
            global item_id_selected

            product_name_listed = self.tableWidget.item(row_listed, 3).text()
            product_price_listed = self.tableWidget.item(row_listed, 4).text()
            item_id_selected = int(self.tableWidget.item(row_listed, 0).text())
            curs.execute(f"select product_description from listed_items where item_id = {item_id_selected};")
            product_description_listed = curs.fetchone()
            product_description_listed = list(product_description_listed)
            product_description_listed = str(product_description_listed[0])
            Edit_Items.update_data()
            self.go_to_edit_page()



    def go_to_edit_page(self):
        self.tableWidget.clearSelection()
        widget.setCurrentIndex(12)



        




# -------------------------------------------------------Edit Items------------------------------------------------------- #
class Edit_Items(QDialog):
    def __init__(self) -> None:
        super(Edit_Items, self).__init__()
        loadUi("assets/editPage.ui", self)
        self.pushButton_delete.clicked.connect(self.are_you_sure)
        self.pushButton_done.clicked.connect(self.done)
        self.update_data()

    def delete(self): 
        global item_id_selected
        curs.execute(f"update listed_items set deleted = 'True' where item_id = {item_id_selected};")
        Items.loadData()
        buy_page.loadData()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Delete')
        error_dialog.showMessage("Your item has been deleted")
        widget.setCurrentIndex(11)
    def done(self):
        global item_id_selected
        self.item_name = self.lineEdit_name.text()
        self.item_price = self.lineEdit_price.text()
        self.item_description = self.lineEdit_description.text()


        curs.execute(f'''update listed_items set product_name = "{self.item_name}", product_price = "{self.item_price}", product_description = "{self.item_description}" where item_id = {item_id_selected};''')
        Items.loadData()
        buy_page.loadData()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        error_dialog.setWindowTitle('Update')
        error_dialog.showMessage("Your item has been updated")
        widget.setCurrentIndex(11)


    def are_you_sure(self):
        msg = QMessageBox()
        msg.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        msg.setWindowTitle("Delete")
        msg.setText("Are you sure you want to PERMANENTLY DELETE this item?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()

    def popup_button(self, button):
        button_pressed = button.text()

        if button_pressed == '&Yes':
            self.delete()

        else:
            pass

    def update_data(self):
        global product_name_listed
        global product_price_listed
        global product_description_listed
        self.lineEdit_name.setText(product_name_listed)
        self.lineEdit_price.setText(product_price_listed)
        self.lineEdit_description.setText(product_description_listed)




    















 # End of class declaration
# -------------------------------------------------------Indexing for stacked widget and Data------------------------------------------------------- #
app = QApplication(sys.argv)
#file = QFile("amoled.qss")
#file.open(QFile.ReadOnly | QFile.Text)
#stream = QTextStream(file)
#app.setStyleSheet(stream.readAll())
#app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
widget = QtWidgets.QStackedWidget()
widget.setMaximumHeight(600)
widget.setMaximumWidth(1000)
widget.setMinimumHeight(600)
widget.setMinimumWidth(1000)
login_register_page = loginregisterpage()
loginpage = login_page()
buy_page = buy_page()
registerpage = register_page()
sellpage = sellPage()
transactionPage = transactionPage()
creditCard = creditCard()
debitCard = debitCard()
upi = upi()
netBank = netBank()
orders = orders()
Items = Items()
Edit_Items = Edit_Items()
forgot = forgot()
buy_page.loadData()

# Indexing for all the stacked pages. indexes are appointed in the order they are added.
widget.addWidget(login_register_page)           # 0
widget.addWidget(loginpage)                     # 1
widget.addWidget(registerpage)                  # 2
widget.addWidget(buy_page)                      # 3
widget.addWidget(sellpage)                      # 4
widget.addWidget(transactionPage)               # 5
widget.addWidget(creditCard)                    # 6
widget.addWidget(debitCard)                     # 7
widget.addWidget(upi)                           # 8
widget.addWidget(netBank)                       # 9
widget.addWidget(orders)                        # 10
widget.addWidget(Items)                         # 11
widget.addWidget(Edit_Items)                    # 12
widget.addWidget(forgot)                        # 13
# End of indexing for stacked widgets


# Execution:
widget.show()


# Exit

try:
    sys.exit(app.exec_())

except:
    print("Exiting")
