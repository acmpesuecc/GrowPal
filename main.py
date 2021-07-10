# -------------------------------------------------------Import statements------------------------------------------------------- #
import sys
import os
# pip install PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QLineEdit, QWidget, QFileDialog, QLabel
from PyQt5.QtCore import QFile, QTextStream, QSize
from PyQt5.QtGui import QIcon, QPixmap
from validate_email import validate_email
# pip install validate_email
import mysql.connector
# pip install mysql-connector
# pip install pandas
from pandas.core.common import flatten
from imagekitio import ImageKit
# pip install imagekitio
from PIL import Image
# pip install pillow
import urllib
# -------------------------------------------------------Variables and Misc.------------------------------------------------------- #
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
givenFile = 'product_cake1.jpeg'
global db
db = mysql.connector.connect(host='sql6.freemysqlhosting.net', user = 'sql6424083', passwd = 'D2acFG7MzS', database = 'sql6424083')
if(db):
    print('sql connection successful')
else:
    print('sql messed up')


global curs
curs = db.cursor()

def getLoginDetails():
    global loginpage_details
    curs.execute('select username, password from login_details')
    loginpage_details = curs.fetchall()
    loginpage_details = list(flatten(loginpage_details))

getLoginDetails()

imagekit = ImageKit(
        private_key = 'private_UWuh0ACI8AKq5HVubqJ7K1gON6Q=',
        public_key='public_9lTcdw6jQBz3nQTYfU1MXlsC/ZU=',
        url_endpoint = 'https://ik.imagekit.io/bule8zjn18b'
)




# -------------------------------------------------------Class declaration for all pages------------------------------------------------------- #
# -------------------------------------------------------loginregisterpage------------------------------------------------------- #


class loginregisterpage(QMainWindow):
    def __init__(self):
        super(loginregisterpage, self).__init__()
        loadUi("loginRegisterPage.ui", self)
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
        loadUi("loginPage.ui", self)
        #logged_in_username = ""
        #logged_in_password = ""
        self.pushButton_back.clicked.connect(self.back_button_pressed)
        self.pushbutton_login.clicked.connect(self.login_button_pressed)
        self.password_view.clicked.connect(self.pass_view_clicked)
        global logged_in_username
        global logged_in_password
        logged_in_username = ''
        logged_in_password = ''
        self.iicon = QIcon('visiblity.svg')
        self.password_view.setIcon(self.iicon)
    def pass_view_clicked(self):
        if self.password_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)

            self.icon = QIcon('visiblity_off.svg')
            self.password_view.setIcon(self.icon)

        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            
            self.icon = QIcon('visiblity.svg')
            self.password_view.setIcon(self.icon)




    def back_button_pressed(self):
        widget.setCurrentIndex(0)

    def login_button_pressed(self):
        getLoginDetails()
        if self.lineEdit_username.text() == "" or self.lineEdit_password.text() == "":

            error_dialog = QtWidgets.QErrorMessage(self)
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
                    error_dialog.setWindowTitle('Welcome')
                    error_dialog.showMessage(
                        f"Welcome back {logged_in_username}!")
                    widget.setCurrentIndex(3)
                    buy_page.loadData()
                else:
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Password')
                    error_dialog.showMessage(
                        'Incorrect password, please try again')
                    self.lineEdit_password.setText("")
            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setWindowTitle('Account')
                error_dialog.showMessage('Please create an account')
                self.lineEdit_username.setText("")
                self.lineEdit_password.setText("")
                widget.setCurrentIndex(2)


# -------------------------------------------------------register_page------------------------------------------------------- #
class register_page(QMainWindow):
    def __init__(self):
        super(register_page, self).__init__()
        loadUi("registerPage.ui", self)
        self.pushButton_back.clicked.connect(self.back_button_clicked)
        self.pushbutton_register.clicked.connect(self.register_button_clicked)
        self.sp_view.clicked.connect(self.sp_view_clicked)
        self.cp_view.clicked.connect(self.cp_view_clicked)

        self.ispicon = QIcon('visiblity.svg')
        self.sp_view.setIcon(self.ispicon)
        self.icpicon = QIcon('visiblity.svg')
        self.cp_view.setIcon(self.icpicon)
    def sp_view_clicked(self):
        if self.sp_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
            self.iconsp = QIcon('visiblity_off.svg')
            self.sp_view.setIcon(self.iconsp)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            self.iconsp = QIcon('visiblity.svg')
            self.sp_view.setIcon(self.iconsp)

    def cp_view_clicked(self):
        if self.cp_view.isChecked():
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Normal)

            self.iconcp = QIcon('visiblity_off.svg')
            self.cp_view.setIcon(self.iconcp)
        else:
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Password)
            self.iconcp = QIcon('visiblity.svg')
            self.cp_view.setIcon(self.iconcp)

    def back_button_clicked(self):
        widget.setCurrentIndex(0)

    def register_button_clicked(self):

        if self.lineEdit_username.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_phnumber.text() == "" or self.lineEdit_password.text() == "" or self.lineEdit_repeatpassword.text() == "":
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Empty Fields')
            error_dialog.showMessage("Please fill all the fields")
        elif len(self.lineEdit_phnumber.text()) != 10:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Phone Number')
            error_dialog.showMessage('Please enter a valid phone number')
            self.lineEdit_phnumber.setText("")

        elif self.lineEdit_password.text() != self.lineEdit_repeatpassword.text():
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Password')
            error_dialog.showMessage('Your passwords do not match. Try again.')
            self.lineEdit_password.setText("")
            self.lineEdit_repeatpassword.setText("")

        elif self.lineEdit_password.text() == self.lineEdit_repeatpassword.text():
            if validate_email(self.lineEdit_email.text()):
                if self.lineEdit_username.text() not in loginpage_details:

                    curs.execute(f"insert into login_details values('{self.lineEdit_username.text()}', '{self.lineEdit_password.text()}', '{self.lineEdit_email.text()}', '{self.lineEdit_phnumber.text()}')")
                    db.commit()
                    getLoginDetails()
                    self.lineEdit_username.setText('')
                    self.lineEdit_email.setText('')
                    self.lineEdit_phnumber.setText('') 
                    self.lineEdit_password.setText("")
                    self.lineEdit_repeatpassword.setText("")
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Thanks!')
                    error_dialog.showMessage(
                        'Thanks for creating an account with us! Please login with the same credentials')
                    widget.setCurrentIndex(1)
                else:
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Account')
                    error_dialog.showMessage(
                        'You are already registered, please login.')
                    widget.setCurrentIndex(1)

            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setWindowTitle('Email')
                error_dialog.showMessage('Please enter a valid email ID')
                self.lineEdit_email.setText("")


# -------------------------------------------------------buy_page------------------------------------------------------- #
class buy_page(QMainWindow):

    def __init__(self) -> None:
        super(buy_page, self).__init__()
        loadUi("buy_page.ui", self)
        self.pushButton_logout.clicked.connect(self.logout)
        self.pushButton_sell.clicked.connect(self.gotoSellPage)
        global price
        global item
        self.pushButton_orders.clicked.connect(self.go_to_orders)
        self.pushButton_selling_items.clicked.connect(self.go_to_items)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 200)
        self.loadData()
        self.tableWidget.selectionModel().selectionChanged.connect(self.selection)
    def selection(self, selected):
        for ix in selected.indexes():
            global row 
            global column 
            row = ix.row()
            column = ix.column()
            global price 
            global item
            global picture 

            price = self.tableWidget.item(row, 2).text()
            item = self.tableWidget.item(row, 1).text()
            
            curs.execute(f"select product_image_address from listed_items where product_name = '{item}';")
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
        Items.loadData()




    def go_to_orders(self):
        widget.setCurrentIndex(10)
        orders.loadData()

    def logout(self):
        widget.setCurrentIndex(0)

    def gotoSellPage(self):

        # self.label_prod_img2.setPixmap(self.pixmap)
        widget.setCurrentIndex(4)
    



    def loadData(self):

        global logged_in_username 
        curs.execute(f"select product_name, product_price, product_description, product_image_address from listed_items;")
        listed_items = curs.fetchall()
    
        row = 0
        self.tableWidget.setRowCount(len(listed_items))
        for item in listed_items:
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item[0]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item[2]))



            self.image = QtWidgets.QLabel(self.centralwidget)
            self.image.setText('')
            self.image.setScaledContents(True)
            self.data = urllib.request.urlopen(item[3]).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.pixmap = self.pixmap.scaled(200, 250)
            self.image.setPixmap(self.pixmap)
            self.tableWidget.setCellWidget(row, 0, self.image)
            self.image.setHidden(True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(200)
            
            row = row + 1

# -------------------------------------------------------sellPage------------------------------------------------------- #
class sellPage(QMainWindow):
    def __init__(self) -> None:
        super(sellPage, self).__init__()
        loadUi("sellPage.ui", self)
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
        curs.execute("select product_name from listed_items")
        num = curs.fetchall()
        num = len(list(num))
        num = num  + 1 
        num = str(num)
        givenFile = Image.open(givenFile)
        givenFile.save(num + ".jpeg")
        upload = imagekit.upload(
                file= open(num+".jpeg", "rb"), 
                file_name= num+".jpeg", 
                options = {"use_unique_file_name" : False }
)       
        global imagekit_url
        imagekit_url = imagekit.url({
            "path": num + ".jpeg",
            "url_endpoint" : "https://ik.imagekit.io/bule8zjn18b/"
        }
)
        or.remove(num+".jpeg")
    def sell(self):
        if self.lineEdit_prod_name.text() == "" or self.lineEdit_price.text() == "" or self.lineEdit_description.text() == "" or self.lineEdit_name.text == "" or self.lineEdit_cont_num.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_address.text() == "" or self.lineEdit_upi_id == "":
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Empty Fields')
            error_dialog.showMessage("Please fill all the fields")
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
            global logged_in_username
            global imagekit_url
            curs.execute(f"insert into listed_items values('{sellPage.given_prod_name}', '{sellPage.given_price}', '{sellPage.given_description}', '{logged_in_username}', '{sellPage.given_name}', '{sellPage.given_cont_num}', '{sellPage.given_email}','{sellPage.given_address}', '{sellPage.given_upi_id}', '{str(imagekit_url)}');")      
            db.commit()
            error_dialog = QtWidgets.QErrorMessage(self)


            error_dialog.setWindowTitle('Sell')
            error_dialog.showMessage(
                f"Your product {sellPage.given_prod_name} is now listed for {sellPage.given_price} rupees")
            widget.setCurrentIndex(3)
            buy_page.loadData()



# -------------------------------------------------------Transaction Page------------------------------------------------------- #


class transactionPage(QMainWindow):
    def __init__(self) -> None:
        super(transactionPage, self).__init__()
        loadUi("transaction.ui", self)
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
        self.pixmap = QPixmap(picture)
        self.pixmap = self.pixmap.scaled(256, 171)
        self.label_picture.setPixmap(self.pixmap)
        self.label_ammount.setText(f'''Item: {item}
Ammount: {price}''')




# -------------------------------------------------------Transaction - Credit Card------------------------------------------------------- #

class creditCard(QMainWindow):
    def __init__(self) -> None:
        super(creditCard, self).__init__()
        loadUi("transaction_cc.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

    def pay(self):
        global price
        global item
        global logged_in_username
        curs.execute(f"insert into credit_card_transactions values('{logged_in_username}','{item}', '{price}', '{self.lineEdit_cnum.text()}', '{self.lineEdit_cvv.text()}', '{self.lineEdit_del_add.text()}')")
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')
        transactionPage.go_back()






# -------------------------------------------------------Transaction - Debit Card------------------------------------------------------- #

class debitCard(QMainWindow):
    def __init__(self) -> None:
        super(debitCard, self).__init__()
        loadUi("transaction_dc.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

    def pay(self):
        global price
        global item
        global logged_in_username
        curs.execute(f"insert into debit_card_transactions values('{logged_in_username}', '{item}', '{price}','{self.lineEdit_cnum.text()}', '{self.lineEdit_cvv.text()}', '{self.lineEdit_del_add.text()}')")
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()






# -------------------------------------------------------Transaction - UPI------------------------------------------------------- #

class upi(QMainWindow):
    def __init__(self) -> None:
        super(upi, self).__init__()
        loadUi("transaction_upi.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

    def pay(self):
        global price
        global item
        global logged_in_username
        curs.execute(f"insert into upi_transactions values('{logged_in_username}', '{item}', '{price}', '{self.lineEdit_upinum.text()}', '{self.lineEdit_del_add.text()}')")
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()

# -------------------------------------------------------Transaction - NetBanking------------------------------------------------------- #

class netBank(QMainWindow):
    def __init__(self) -> None:
        super(netBank, self).__init__()
        loadUi("transaction_netbank.ui", self)
        self.pushButton_cancel.clicked.connect(transactionPage.go_back)
        self.pushButton_pay.clicked.connect(self.pay)

    def pay(self):
        global price
        global item
        global logged_in_username
        curs.execute(f"insert into net_bank_transactions values('{logged_in_username}', '{item}', '{price}','{self.lineEdit_acnum.text()}', '{self.lineEdit_cifnum.text()}', '{self.lineEdit_branch_code.text()}', '{self.lineEdit_del_add.text()}')")
        db.commit()
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.setWindowTitle('Order')
        error_dialog.showMessage('Your order has been placed.')

        transactionPage.go_back()


# -------------------------------------------------------Orders------------------------------------------------------- #

class orders(QMainWindow):
    def __init__(self) -> None:
        super(orders, self).__init__()
        loadUi("orders.ui", self)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 332)
        self.loadData()
        self.pushButton_back.clicked.connect(self.go_back)

    def go_back(self):
        widget.setCurrentIndex(3)

    def loadData(self):
        global logged_in_username


        curs.execute(f"select item, price, flat_number from credit_card_transactions where username = '{logged_in_username}' union select item, price, flat_number from debit_card_transactions where username = '{logged_in_username}' union select item, price, flat_number from upi_transactions where username = '{logged_in_username}' union select item, price, flat_number from net_bank_transactions where username = '{logged_in_username}';")



        order_list = curs.fetchall()
        row = 0
        self.tableWidget.setRowCount(len(order_list))
        for order in order_list:
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(order[0]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(order[1]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(order[2]))
            row = row + 1

# -------------------------------------------------------Items------------------------------------------------------- #
class Items(QMainWindow):
    def __init__(self) -> None:
        super(Items, self).__init__()
        loadUi("sold_items.ui", self)
        self.loadData()
        self.pushButton_back.clicked.connect(orders.go_back)



    def loadData(self):
        global logged_in_username 
        curs.execute(f"select product_image_address, product_name, product_price, product_description from listed_items where seller_username = '{logged_in_username}';")
        listed_items = curs.fetchall()
    
        row = 0
        self.tableWidget.setRowCount(len(listed_items))
        for item in listed_items:
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item[3]))

            self.image = QtWidgets.QLabel(self.centralwidget)
            self.image.setText('')
            self.image.setScaledContents(True)

            self.data = urllib.request.urlopen(item[0]).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data)
            self.pixmap = self.pixmap.scaled(200, 250)
            self.image.setPixmap(self.pixmap)
            self.tableWidget.setCellWidget(row, 0, self.image)
            self.image.setHidden(True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(200)



            row = row + 1








 # End of class declaration
# -------------------------------------------------------Indexing for stacked widget------------------------------------------------------- #
app = QApplication(sys.argv)
file = QFile("amoled.qss")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app.setStyleSheet(stream.readAll())
widget = QtWidgets.QStackedWidget()


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
# End of indexing for stacked widgets


# Execution:
widget.show()


# Exit

try:
    sys.exit(app.exec_())

except:
    print("Exiting")
