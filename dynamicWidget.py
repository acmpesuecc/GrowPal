# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledFhFXFb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(902, 518)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-1, 9, 800, 401))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_picture = QLabel(self.frame)
        self.label_picture.setObjectName(u"label_picture")

        self.gridLayout.addWidget(self.label_picture, 0, 0, 2, 1)

        self.label_description = QLabel(self.frame)
        self.label_description.setObjectName(u"label_description")

        self.gridLayout.addWidget(self.label_description, 0, 1, 1, 1)

        self.pushButton_buy = QPushButton(self.frame)
        self.pushButton_buy.setObjectName(u"pushButton_buy")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_buy.setFont(font)

        self.gridLayout.addWidget(self.pushButton_buy, 1, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_picture.setText("")
        self.label_description.setText("")
        self.pushButton_buy.setText(QCoreApplication.translate("Form", u"Buy", None))
    # retranslateUi

