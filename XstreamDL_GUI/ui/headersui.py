# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'headers.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from XstreamDL_GUI.ui.widgets.qlineedit import HeaderFileQLineEdit
from XstreamDL_GUI.ui.widgets.qtextedit import HeadersQTextEdit

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 500)
        Form.setStyleSheet(u"QWidget#Form{\n"
"	background-color: rgb(225, 243, 254);\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_headers_path = HeaderFileQLineEdit(Form)
        self.lineEdit_headers_path.setObjectName(u"lineEdit_headers_path")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_headers_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_headers_path.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lineEdit_headers_path)

        self.pushButton_select = QPushButton(Form)
        self.pushButton_select.setObjectName(u"pushButton_select")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_select.sizePolicy().hasHeightForWidth())
        self.pushButton_select.setSizePolicy(sizePolicy1)
        self.pushButton_select.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_select)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textEdit_headers_content = HeadersQTextEdit(Form)
        self.textEdit_headers_content.setObjectName(u"textEdit_headers_content")

        self.horizontalLayout.addWidget(self.textEdit_headers_content)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_save = QPushButton(Form)
        self.pushButton_save.setObjectName(u"pushButton_save")
        sizePolicy1.setHeightForWidth(self.pushButton_save.sizePolicy().hasHeightForWidth())
        self.pushButton_save.setSizePolicy(sizePolicy1)
        self.pushButton_save.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.pushButton_save)

        self.pushButton_add = QPushButton(Form)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy1.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy1)
        self.pushButton_add.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.pushButton_add)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listWidget_headers_key = QListWidget(Form)
        self.listWidget_headers_key.setObjectName(u"listWidget_headers_key")

        self.horizontalLayout_3.addWidget(self.listWidget_headers_key)

        self.listWidget_headers_value = QListWidget(Form)
        self.listWidget_headers_value.setObjectName(u"listWidget_headers_value")

        self.horizontalLayout_3.addWidget(self.listWidget_headers_value)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 4)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.setStretch(2, 6)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"headers editor", None))
        self.lineEdit_headers_path.setPlaceholderText(QCoreApplication.translate("Form", u"headers.json", None))
#if QT_CONFIG(tooltip)
        self.pushButton_select.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>load headers.json file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select.setText(QCoreApplication.translate("Form", u"select", None))
#if QT_CONFIG(tooltip)
        self.pushButton_save.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>save to headers.json</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"save", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>add a group of header key-value</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add.setText(QCoreApplication.translate("Form", u"add", None))
    # retranslateUi

