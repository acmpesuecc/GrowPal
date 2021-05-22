# -------------------------------------------------------Import statements------------------------------------------------------- #
import sys  
#pip install PyQt5
from PyQt5.uic import loadUi 
from PyQt5 import QtWidgets
from PyQt5 import QtGui  
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QLineEdit
from validate_email import validate_email
#pip install validate_email

# -------------------------------------------------------Variables------------------------------------------------------- #
global loginpage_details
loginpage_details = {'admin': 'admin@password'}
global register_page_email
global register_page_password
global listedItems
listedItems = {}
#global logged_in_username
#logged_in_username = "" 
#global logged_in_password
#logged_in_password = ""



# -------------------------------------------------------Class declaration for all pages------------------------------------------------------- #
# -------------------------------------------------------loginregisterpage------------------------------------------------------- #
class loginregisterpage(QMainWindow):
    def __init__(self):
        super(loginregisterpage, self).__init__()
        loadUi("loginRegisterPage.ui",self) 
        self.setWindowTitle("GrowPal")
        self.login_button.clicked.connect(self.gotologin_page) 
        self.register_button.clicked.connect(self.gotoregister_page) 
        #self.iconName = "logo.jpg"
    def gotologin_page(self):
        widget.setCurrentIndex(1) 
    def gotoregister_page(self):
        widget.setCurrentIndex(2)



# -------------------------------------------------------login_page------------------------------------------------------- #
class login_page(QMainWindow):
    def __init__(self):
        super(login_page,self).__init__() 
        loadUi("loginPage.ui",self) 
        #global logged_in_username
        logged_in_username = "" 
        #global logged_in_password
        logged_in_password = ""
        self.pushButton_back.clicked.connect(self.back_button_pressed)
        self.pushbutton_login.clicked.connect(self.login_button_pressed) 
        self.password_view.clicked.connect(self.pass_view_clicked)

    def pass_view_clicked(self):
        if self.password_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)

    def back_button_pressed(self):
        widget.setCurrentIndex(0)


    def login_button_pressed(self):
        if self.lineEdit_username.text() == "" or self.lineEdit_password.text() == "": 
            print("empty")
        else:
            if self.lineEdit_username.text() in loginpage_details.keys():                           
                if self.lineEdit_password.text() == loginpage_details[self.lineEdit_username.text()]:
                    login_page.logged_in_username = self.lineEdit_username.text()           
                    login_page.logged_in_password = self.lineEdit_password.text()
                    self.lineEdit_username.setText("")
                    self.lineEdit_password.setText("")
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Welcome')
                    error_dialog.showMessage(f"Welcome back {login_page.logged_in_username}!")
                    # print(login_page.logged_in_username)
                    # print(login_page.logged_in_password)
                    widget.setCurrentIndex(3)
                else: 
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Password')
                    error_dialog.showMessage('Incorrect password, please try again')
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
       
        



    def sp_view_clicked(self):
        if self.sp_view.isChecked():
            self.lineEdit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.Password)



    def cp_view_clicked(self):
        if self.cp_view.isChecked():
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_repeatpassword.setEchoMode(QLineEdit.Password)


    def back_button_clicked(self):
        widget.setCurrentIndex(0)


    def register_button_clicked(self):
       

        if self.lineEdit_username.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_phnumber.text() == "" or self.lineEdit_password.text() == "" or self.lineEdit_repeatpassword.text() == "":
            print("empty")  

        elif len(self.lineEdit_phnumber.text()) != 10:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Phone Number')
            error_dialog.showMessage('Please enter a valid phone number')
            self.lineEdit_phnumber.setText("")

        elif self.lineEdit_password.text() == self.lineEdit_repeatpassword.text(): 
            if validate_email(self.lineEdit_email.text()):
                if self.lineEdit_username.text() not in loginpage_details.keys():
                    register_page_username = self.lineEdit_username.text()
                    register_page_password = self.lineEdit_password.text()
                    loginpage_details.update({register_page_username:register_page_password})
                    self.lineEdit_password.setText("")
                    self.lineEdit_repeatpassword.setText("")
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Thanks!')
                    error_dialog.showMessage('Thanks for creating an account with us! Please login with the same credentials')
                    widget.setCurrentIndex(1)
                else:
                    error_dialog = QtWidgets.QErrorMessage(self)
                    error_dialog.setWindowTitle('Account')
                    error_dialog.showMessage('You are already registered, please login.')
                    widget.setCurrentIndex(1)
                    
            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setWindowTitle('Email')
                error_dialog.showMessage('Please enter a valid email ID')
                self.lineEdit_email.setText("")



        elif self.lineEdit_password.text() != self.lineEdit_repeatpassword.text(): 
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Password') 
            error_dialog.showMessage('Your passwords do not match. Try again.') 
            self.lineEdit_password.setText("")
            self.lineEdit_repeatpassword.setText("")



# -------------------------------------------------------buy_page------------------------------------------------------- #
class buy_page(QMainWindow):
    def __init__(self) -> None:
        super(buy_page, self).__init__()
        loadUi("buy_page.ui", self)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.pushButton_logout.clicked.connect(self.logout)
        self.pushButton_sell.clicked.connect(self.gotoSellPage)
    def logout(self):
        widget.setCurrentIndex(0)
        # print(login_page.logged_in_username)
        # print(login_page.logged_in_password)
    def gotoSellPage(self):
        widget.setCurrentIndex(4)

# -------------------------------------------------------sellPage------------------------------------------------------- #
class sellPage(QMainWindow):
    def __init__(self) -> None:
        super(sellPage, self).__init__()
        loadUi("sellPage.ui",self)
        self.pushButton_back.clicked.connect(self.getback)
        self.pushButton_UploadImages.clicked.connect(self.upload)
        self.pushButton_Sell.clicked.connect(self.sell)
        
    def getback(self):
        widget.setCurrentIndex(3)
    def upload(self):
        pass
    def sell(self):
        if self.lineEdit_prod_name.text() == "" or self.lineEdit_price.text() == "" or self.lineEdit_description.text() == "" or self.lineEdit_name.text == "" or self.lineEdit_cont_num.text() == "" or self.lineEdit_email.text() == "" or self.lineEdit_address.text() == "" or self.lineEdit_upi_id == "":
            print("empty")
            
        else: 
            sellPage.given_prod_name = self.lineEdit_prod_name.text()
            sellPage.given_price = self.lineEdit_price.text()
            sellPage.given_description = self.lineEdit_description.text()
            sellPage.given_name = self.lineEdit_name.text()
            sellPage.given_cont_num = self.lineEdit_cont_num.text()
            sellPage.given_email = self.lineEdit_email.text()
            sellPage.given_address = self.lineEdit_address.text()
            sellPage.given_upi_id = self.lineEdit_upi_id.text()
            error_dialog = QtWidgets.QErrorMessage(self)
            listedItems.update({sellPage.given_prod_name:sellPage.given_price})
            # print(listedItems)
            error_dialog.setWindowTitle('Sell') 
            error_dialog.showMessage(f"Your product {sellPage.given_prod_name} is now listed for {sellPage.given_price} rupees")
            widget.setCurrentIndex(3)
        
        
        
        
        
        
        
        
        
    # End of class declaration


# -------------------------------------------------------Indexing for stacked widget------------------------------------------------------- #
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() 


login_register_page = loginregisterpage() 
loginpage = login_page() 
buypage = buy_page()
registerpage = register_page()
sellpage = sellPage()
# Indexing for all the stacked pages. indexes are appointed in the order they are added.
widget.addWidget(login_register_page) # 0
widget.addWidget(loginpage)   # 1
widget.addWidget(registerpage) # 2
widget.addWidget(buypage)     # 3
widget.addWidget(sellpage)      #4
# End of indexing for stacked widgets


# Execution:
widget.show()


# Exit 

try:
    sys.exit(app.exec_())

except:
    print("Exiting")
    


