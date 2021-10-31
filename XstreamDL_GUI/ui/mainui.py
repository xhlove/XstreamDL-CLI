# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from XstreamDL_GUI.ui.widgets.qlineedit import (NameQLineEdit, URIQLineEdit)
from XstreamDL_GUI.ui.widgets.qtextedit import CommandQTextEdit
from  . import res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/ui/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget{\n"
"	background-color: rgb(225, 243, 254);\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 5, -1, 5)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(60, 0))
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_9)

        self.lineEdit_redl_code = QLineEdit(self.centralwidget)
        self.lineEdit_redl_code.setObjectName(u"lineEdit_redl_code")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_redl_code.sizePolicy().hasHeightForWidth())
        self.lineEdit_redl_code.setSizePolicy(sizePolicy)

        self.horizontalLayout_9.addWidget(self.lineEdit_redl_code)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 5, -1, 5)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(60, 0))
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_11)

        self.lineEdit_save_dir = QLineEdit(self.centralwidget)
        self.lineEdit_save_dir.setObjectName(u"lineEdit_save_dir")
        sizePolicy.setHeightForWidth(self.lineEdit_save_dir.sizePolicy().hasHeightForWidth())
        self.lineEdit_save_dir.setSizePolicy(sizePolicy)

        self.horizontalLayout_11.addWidget(self.lineEdit_save_dir)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 5, -1, 5)
        self.checkBox_use_proxy = QCheckBox(self.centralwidget)
        self.checkBox_use_proxy.setObjectName(u"checkBox_use_proxy")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBox_use_proxy.sizePolicy().hasHeightForWidth())
        self.checkBox_use_proxy.setSizePolicy(sizePolicy1)
        self.checkBox_use_proxy.setMinimumSize(QSize(60, 0))
        self.checkBox_use_proxy.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_5.addWidget(self.checkBox_use_proxy)

        self.lineEdit_proxy = QLineEdit(self.centralwidget)
        self.lineEdit_proxy.setObjectName(u"lineEdit_proxy")
        sizePolicy.setHeightForWidth(self.lineEdit_proxy.sizePolicy().hasHeightForWidth())
        self.lineEdit_proxy.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.lineEdit_proxy)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 5, -1, 5)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(60, 0))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_7)

        self.lineEdit_b64key = QLineEdit(self.centralwidget)
        self.lineEdit_b64key.setObjectName(u"lineEdit_b64key")
        sizePolicy.setHeightForWidth(self.lineEdit_b64key.sizePolicy().hasHeightForWidth())
        self.lineEdit_b64key.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.lineEdit_b64key)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 5, -1, 5)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(60, 0))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.lineEdit_hexiv = QLineEdit(self.centralwidget)
        self.lineEdit_hexiv.setObjectName(u"lineEdit_hexiv")
        sizePolicy.setHeightForWidth(self.lineEdit_hexiv.sizePolicy().hasHeightForWidth())
        self.lineEdit_hexiv.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.lineEdit_hexiv)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 5, -1, 5)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(60, 0))
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.label_10)

        self.lineEdit_url_patch = QLineEdit(self.centralwidget)
        self.lineEdit_url_patch.setObjectName(u"lineEdit_url_patch")
        sizePolicy.setHeightForWidth(self.lineEdit_url_patch.sizePolicy().hasHeightForWidth())
        self.lineEdit_url_patch.setSizePolicy(sizePolicy)

        self.horizontalLayout_10.addWidget(self.lineEdit_url_patch)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 5, -1, 5)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(60, 0))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_8)

        self.lineEdit_key = QLineEdit(self.centralwidget)
        self.lineEdit_key.setObjectName(u"lineEdit_key")
        sizePolicy.setHeightForWidth(self.lineEdit_key.sizePolicy().hasHeightForWidth())
        self.lineEdit_key.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.lineEdit_key)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_base_url = QLineEdit(self.centralwidget)
        self.lineEdit_base_url.setObjectName(u"lineEdit_base_url")
        sizePolicy.setHeightForWidth(self.lineEdit_base_url.sizePolicy().hasHeightForWidth())
        self.lineEdit_base_url.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lineEdit_base_url)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, 5)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(60, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_name = NameQLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lineEdit_name)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_16.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, -1, -1, -1)
        self.checkBox_index_name = QCheckBox(self.centralwidget)
        self.checkBox_index_name.setObjectName(u"checkBox_index_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkBox_index_name.sizePolicy().hasHeightForWidth())
        self.checkBox_index_name.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_index_name, 3, 1, 1, 1)

        self.checkBox_disable_force_close = QCheckBox(self.centralwidget)
        self.checkBox_disable_force_close.setObjectName(u"checkBox_disable_force_close")
        sizePolicy2.setHeightForWidth(self.checkBox_disable_force_close.sizePolicy().hasHeightForWidth())
        self.checkBox_disable_force_close.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_disable_force_close, 0, 2, 1, 1)

        self.checkBox_disable_auto_decrypt = QCheckBox(self.centralwidget)
        self.checkBox_disable_auto_decrypt.setObjectName(u"checkBox_disable_auto_decrypt")
        sizePolicy2.setHeightForWidth(self.checkBox_disable_auto_decrypt.sizePolicy().hasHeightForWidth())
        self.checkBox_disable_auto_decrypt.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_disable_auto_decrypt, 3, 2, 1, 1)

        self.checkBox_parse_only = QCheckBox(self.centralwidget)
        self.checkBox_parse_only.setObjectName(u"checkBox_parse_only")
        sizePolicy2.setHeightForWidth(self.checkBox_parse_only.sizePolicy().hasHeightForWidth())
        self.checkBox_parse_only.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_parse_only, 1, 1, 1, 1)

        self.checkBox_live = QCheckBox(self.centralwidget)
        self.checkBox_live.setObjectName(u"checkBox_live")
        sizePolicy2.setHeightForWidth(self.checkBox_live.sizePolicy().hasHeightForWidth())
        self.checkBox_live.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_live, 0, 0, 1, 1)

        self.checkBox_overwrite = QCheckBox(self.centralwidget)
        self.checkBox_overwrite.setObjectName(u"checkBox_overwrite")
        sizePolicy2.setHeightForWidth(self.checkBox_overwrite.sizePolicy().hasHeightForWidth())
        self.checkBox_overwrite.setSizePolicy(sizePolicy2)
        self.checkBox_overwrite.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_overwrite, 2, 0, 1, 1)

        self.checkBox_show_init = QCheckBox(self.centralwidget)
        self.checkBox_show_init.setObjectName(u"checkBox_show_init")
        sizePolicy2.setHeightForWidth(self.checkBox_show_init.sizePolicy().hasHeightForWidth())
        self.checkBox_show_init.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_show_init, 0, 1, 1, 1)

        self.checkBox_disable_auto_concat = QCheckBox(self.centralwidget)
        self.checkBox_disable_auto_concat.setObjectName(u"checkBox_disable_auto_concat")
        sizePolicy2.setHeightForWidth(self.checkBox_disable_auto_concat.sizePolicy().hasHeightForWidth())
        self.checkBox_disable_auto_concat.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_disable_auto_concat, 1, 2, 1, 1)

        self.checkBox_enable_auto_delete = QCheckBox(self.centralwidget)
        self.checkBox_enable_auto_delete.setObjectName(u"checkBox_enable_auto_delete")
        sizePolicy2.setHeightForWidth(self.checkBox_enable_auto_delete.sizePolicy().hasHeightForWidth())
        self.checkBox_enable_auto_delete.setSizePolicy(sizePolicy2)
        self.checkBox_enable_auto_delete.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_enable_auto_delete, 2, 2, 1, 1)

        self.checkBox_select = QCheckBox(self.centralwidget)
        self.checkBox_select.setObjectName(u"checkBox_select")
        sizePolicy2.setHeightForWidth(self.checkBox_select.sizePolicy().hasHeightForWidth())
        self.checkBox_select.setSizePolicy(sizePolicy2)
        self.checkBox_select.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_select, 1, 0, 1, 1)

        self.checkBox_raw_concat = QCheckBox(self.centralwidget)
        self.checkBox_raw_concat.setObjectName(u"checkBox_raw_concat")
        sizePolicy2.setHeightForWidth(self.checkBox_raw_concat.sizePolicy().hasHeightForWidth())
        self.checkBox_raw_concat.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.checkBox_raw_concat, 2, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy3)

        self.horizontalLayout_12.addWidget(self.label_12)

        self.spinBox_limit_per_host = QSpinBox(self.centralwidget)
        self.spinBox_limit_per_host.setObjectName(u"spinBox_limit_per_host")
        sizePolicy2.setHeightForWidth(self.spinBox_limit_per_host.sizePolicy().hasHeightForWidth())
        self.spinBox_limit_per_host.setSizePolicy(sizePolicy2)
        self.spinBox_limit_per_host.setMinimumSize(QSize(50, 0))
        self.spinBox_limit_per_host.setMaximumSize(QSize(16777215, 30))
        self.spinBox_limit_per_host.setMinimum(1)
        self.spinBox_limit_per_host.setMaximum(999)
        self.spinBox_limit_per_host.setValue(4)

        self.horizontalLayout_12.addWidget(self.spinBox_limit_per_host)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_12)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_14)

        self.spinBox_live_duration_hour = QSpinBox(self.centralwidget)
        self.spinBox_live_duration_hour.setObjectName(u"spinBox_live_duration_hour")
        sizePolicy2.setHeightForWidth(self.spinBox_live_duration_hour.sizePolicy().hasHeightForWidth())
        self.spinBox_live_duration_hour.setSizePolicy(sizePolicy2)
        self.spinBox_live_duration_hour.setMinimumSize(QSize(20, 0))
        self.spinBox_live_duration_hour.setMaximumSize(QSize(16777215, 30))
        self.spinBox_live_duration_hour.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout.addWidget(self.spinBox_live_duration_hour)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_live_duration_minute = QSpinBox(self.centralwidget)
        self.spinBox_live_duration_minute.setObjectName(u"spinBox_live_duration_minute")
        sizePolicy2.setHeightForWidth(self.spinBox_live_duration_minute.sizePolicy().hasHeightForWidth())
        self.spinBox_live_duration_minute.setSizePolicy(sizePolicy2)
        self.spinBox_live_duration_minute.setMinimumSize(QSize(20, 0))
        self.spinBox_live_duration_minute.setMaximumSize(QSize(16777215, 30))
        self.spinBox_live_duration_minute.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_live_duration_minute.setMaximum(59)

        self.horizontalLayout.addWidget(self.spinBox_live_duration_minute)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_13)

        self.spinBox_live_duration_second = QSpinBox(self.centralwidget)
        self.spinBox_live_duration_second.setObjectName(u"spinBox_live_duration_second")
        sizePolicy2.setHeightForWidth(self.spinBox_live_duration_second.sizePolicy().hasHeightForWidth())
        self.spinBox_live_duration_second.setSizePolicy(sizePolicy2)
        self.spinBox_live_duration_second.setMinimumSize(QSize(20, 0))
        self.spinBox_live_duration_second.setMaximumSize(QSize(16777215, 30))
        self.spinBox_live_duration_second.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_live_duration_second.setMaximum(59)

        self.horizontalLayout.addWidget(self.spinBox_live_duration_second)

        self.horizontalLayout.setStretch(0, 8)
        self.horizontalLayout.setStretch(1, 10)
        self.horizontalLayout.setStretch(2, 3)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 3)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 3)

        self.horizontalLayout_13.addLayout(self.horizontalLayout)

        self.pushButton_edit_headers = QPushButton(self.centralwidget)
        self.pushButton_edit_headers.setObjectName(u"pushButton_edit_headers")
        sizePolicy2.setHeightForWidth(self.pushButton_edit_headers.sizePolicy().hasHeightForWidth())
        self.pushButton_edit_headers.setSizePolicy(sizePolicy2)
        self.pushButton_edit_headers.setMinimumSize(QSize(100, 0))
        self.pushButton_edit_headers.setMaximumSize(QSize(100, 16777215))
        self.pushButton_edit_headers.setStyleSheet(u"QPushButton#pushButton_edit_headers {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dcdfe6;\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#pushButton_edit_headers:hover {\n"
"    background-color: #ecf5ff;\n"
"    color: #409eff;\n"
"}\n"
"\n"
"QPushButton#pushButton_edit_headers:pressed, QPushButton#pushButton_edit_headers:checked {\n"
"    border: 1px solid #3a8ee6;\n"
"    color: #409eff;\n"
"}")

        self.horizontalLayout_13.addWidget(self.pushButton_edit_headers)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)

        self.horizontalLayout_16.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 5, -1, 5)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(60, 0))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_URI = URIQLineEdit(self.centralwidget)
        self.lineEdit_URI.setObjectName(u"lineEdit_URI")
        sizePolicy.setHeightForWidth(self.lineEdit_URI.sizePolicy().hasHeightForWidth())
        self.lineEdit_URI.setSizePolicy(sizePolicy)
        self.lineEdit_URI.setStyleSheet(u"")
        self.lineEdit_URI.setDragEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEdit_URI)

        self.pushButton_do = QPushButton(self.centralwidget)
        self.pushButton_do.setObjectName(u"pushButton_do")
        sizePolicy2.setHeightForWidth(self.pushButton_do.sizePolicy().hasHeightForWidth())
        self.pushButton_do.setSizePolicy(sizePolicy2)
        self.pushButton_do.setMinimumSize(QSize(100, 0))
        self.pushButton_do.setStyleSheet(u"QPushButton#pushButton_do {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dcdfe6;\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#pushButton_do:hover {\n"
"    background-color: #ecf5ff;\n"
"    color: #409eff;\n"
"}\n"
"\n"
"QPushButton#pushButton_do:pressed, QPushButton#pushButton_do:checked {\n"
"    border: 1px solid #3a8ee6;\n"
"    color: #409eff;\n"
"}")

        self.horizontalLayout_4.addWidget(self.pushButton_do)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)
        self.label_15.setMinimumSize(QSize(60, 0))
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.label_15)

        self.textEdit_command = CommandQTextEdit(self.centralwidget)
        self.textEdit_command.setObjectName(u"textEdit_command")

        self.horizontalLayout_19.addWidget(self.textEdit_command)

        self.pushButton_copy_command = QPushButton(self.centralwidget)
        self.pushButton_copy_command.setObjectName(u"pushButton_copy_command")
        sizePolicy2.setHeightForWidth(self.pushButton_copy_command.sizePolicy().hasHeightForWidth())
        self.pushButton_copy_command.setSizePolicy(sizePolicy2)
        self.pushButton_copy_command.setMinimumSize(QSize(100, 0))
        self.pushButton_copy_command.setStyleSheet(u"QPushButton#pushButton_copy_command {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dcdfe6;\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#pushButton_copy_command:hover {\n"
"    background-color: #ecf5ff;\n"
"    color: #409eff;\n"
"}\n"
"\n"
"QPushButton#pushButton_copy_command:pressed, QPushButton#pushButton_copy_command:checked {\n"
"    border: 1px solid #3a8ee6;\n"
"    color: #409eff;\n"
"}")

        self.horizontalLayout_19.addWidget(self.pushButton_copy_command)


        self.verticalLayout_3.addLayout(self.horizontalLayout_19)

        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"XstreamDL-GUI", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"redl-code", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"save-dir", None))
        self.checkBox_use_proxy.setText(QCoreApplication.translate("MainWindow", u"proxy", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"b64key", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"hexiv", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"url-patch", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"key", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"base-url", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"name", None))
        self.checkBox_index_name.setText(QCoreApplication.translate("MainWindow", u"index-name", None))
        self.checkBox_disable_force_close.setText(QCoreApplication.translate("MainWindow", u"disable-force-close", None))
        self.checkBox_disable_auto_decrypt.setText(QCoreApplication.translate("MainWindow", u"disable-auto-decrypt", None))
        self.checkBox_parse_only.setText(QCoreApplication.translate("MainWindow", u"parse-only", None))
        self.checkBox_live.setText(QCoreApplication.translate("MainWindow", u"live", None))
        self.checkBox_overwrite.setText(QCoreApplication.translate("MainWindow", u"overwrite", None))
        self.checkBox_show_init.setText(QCoreApplication.translate("MainWindow", u"show-init", None))
        self.checkBox_disable_auto_concat.setText(QCoreApplication.translate("MainWindow", u"disable-auto-concat", None))
        self.checkBox_enable_auto_delete.setText(QCoreApplication.translate("MainWindow", u"enable-auto-delete", None))
        self.checkBox_select.setText(QCoreApplication.translate("MainWindow", u"select", None))
        self.checkBox_raw_concat.setText(QCoreApplication.translate("MainWindow", u"raw-concat", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"limit-per-host", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"live-duration", None))
        self.spinBox_live_duration_hour.setPrefix("")
        self.label.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.spinBox_live_duration_minute.setPrefix("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.spinBox_live_duration_second.setPrefix("")
        self.pushButton_edit_headers.setText(QCoreApplication.translate("MainWindow", u"edit headers", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"URI", None))
        self.pushButton_do.setText(QCoreApplication.translate("MainWindow", u"do", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"command", None))
        self.pushButton_copy_command.setText(QCoreApplication.translate("MainWindow", u"copy", None))
    # retranslateUi

