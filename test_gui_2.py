# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_gui_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(542, 566)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 30, 521, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 10, 388, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 50, 521, 491))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.btn_bn = QtWidgets.QPushButton(self.tab)
        self.btn_bn.setGeometry(QtCore.QRect(280, 20, 104, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_bn.setFont(font)
        self.btn_bn.setObjectName("btn_bn")
        self.select_list = QtWidgets.QTreeWidget(self.tab)
        self.select_list.setGeometry(QtCore.QRect(10, 50, 211, 371))
        self.select_list.setObjectName("select_list")
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_0 = QtWidgets.QTreeWidgetItem(self.select_list)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        self.btn_close = QtWidgets.QPushButton(self.tab)
        self.btn_close.setGeometry(QtCore.QRect(420, 430, 75, 23))
        self.btn_close.setObjectName("btn_close")
        self.btn_move_to_right = QtWidgets.QPushButton(self.tab)
        self.btn_move_to_right.setGeometry(QtCore.QRect(230, 210, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_move_to_right.setFont(font)
        self.btn_move_to_right.setObjectName("btn_move_to_right")
        self.selected_list = QtWidgets.QTreeWidget(self.tab)
        self.selected_list.setGeometry(QtCore.QRect(280, 50, 221, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selected_list.sizePolicy().hasHeightForWidth())
        self.selected_list.setSizePolicy(sizePolicy)
        self.selected_list.setObjectName("selected_list")
        self.selected_list.headerItem().setText(0, "1")
        self.btn_run_test = QtWidgets.QPushButton(self.tab)
        self.btn_run_test.setGeometry(QtCore.QRect(340, 430, 75, 23))
        self.btn_run_test.setObjectName("btn_run_test")
        self.text_bn = QtWidgets.QTextEdit(self.tab)
        self.text_bn.setGeometry(QtCore.QRect(390, 20, 111, 21))
        self.text_bn.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.text_bn.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_bn.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_bn.setObjectName("text_bn")
        self.btn_planid = QtWidgets.QPushButton(self.tab)
        self.btn_planid.setGeometry(QtCore.QRect(10, 20, 95, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_planid.setFont(font)
        self.btn_planid.setObjectName("btn_planid")
        self.btn_deselect_all = QtWidgets.QPushButton(self.tab)
        self.btn_deselect_all.setGeometry(QtCore.QRect(230, 270, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_deselect_all.setFont(font)
        self.btn_deselect_all.setObjectName("btn_deselect_all")
        self.text_planid = QtWidgets.QTextEdit(self.tab)
        self.text_planid.setGeometry(QtCore.QRect(110, 20, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_planid.setFont(font)
        self.text_planid.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.text_planid.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_planid.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_planid.setObjectName("text_planid")
        self.btn_select_all = QtWidgets.QPushButton(self.tab)
        self.btn_select_all.setGeometry(QtCore.QRect(230, 180, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_select_all.setFont(font)
        self.btn_select_all.setObjectName("btn_select_all")
        self.btn_move_to_left = QtWidgets.QPushButton(self.tab)
        self.btn_move_to_left.setGeometry(QtCore.QRect(230, 240, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_move_to_left.setFont(font)
        self.btn_move_to_left.setObjectName("btn_move_to_left")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(30, 40, 54, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(330, 40, 18, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 84, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar.setGeometry(QtCore.QRect(20, 120, 481, 16))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(130, 70, 56, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(290, 70, 92, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(410, 70, 75, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(20, 100, 163, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(200, 100, 105, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 76, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(220, 70, 44, 15))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(150, 40, 18, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(440, 40, 18, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(230, 40, 18, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(10, 150, 491, 301))
        self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 542, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_14.setText(_translate("MainWindow", "INFINITT Tele-Radiology Test Automation"))
        self.btn_bn.setText(_translate("MainWindow", "Build Number"))
        self.select_list.headerItem().setText(0, _translate("MainWindow", "Test Suite"))
        __sortingEnabled = self.select_list.isSortingEnabled()
        self.select_list.setSortingEnabled(False)
        self.select_list.topLevelItem(0).setText(0, _translate("MainWindow", "Sign"))
        self.select_list.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "Sign In/Out"))
        self.select_list.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "Remember Me"))
        self.select_list.topLevelItem(1).setText(0, _translate("MainWindow", "Topbar"))
        self.select_list.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "Search Schedule List"))
        self.select_list.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "Upload Schedule List File"))
        self.select_list.topLevelItem(1).child(2).setText(0, _translate("MainWindow", "Download Register Form"))
        self.select_list.topLevelItem(1).child(3).setText(0, _translate("MainWindow", "Guide Download"))
        self.select_list.topLevelItem(2).setText(0, _translate("MainWindow", "Refer"))
        self.select_list.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "Hospital List"))
        self.select_list.topLevelItem(2).child(1).setText(0, _translate("MainWindow", "Reporter List"))
        self.select_list.topLevelItem(3).setText(0, _translate("MainWindow", "Search Filter"))
        self.select_list.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "Priority"))
        self.select_list.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "Job Status"))
        self.select_list.topLevelItem(3).child(2).setText(0, _translate("MainWindow", "Date"))
        self.select_list.topLevelItem(3).child(3).setText(0, _translate("MainWindow", "Patient Location"))
        self.select_list.topLevelItem(3).child(4).setText(0, _translate("MainWindow", "Patient ID"))
        self.select_list.topLevelItem(3).child(5).setText(0, _translate("MainWindow", "Patient Name"))
        self.select_list.topLevelItem(3).child(6).setText(0, _translate("MainWindow", "Age"))
        self.select_list.topLevelItem(3).child(7).setText(0, _translate("MainWindow", "Study Description"))
        self.select_list.topLevelItem(3).child(8).setText(0, _translate("MainWindow", "Modality"))
        self.select_list.topLevelItem(3).child(9).setText(0, _translate("MainWindow", "Bodypart"))
        self.select_list.topLevelItem(3).child(10).setText(0, _translate("MainWindow", "Department"))
        self.select_list.topLevelItem(3).child(11).setText(0, _translate("MainWindow", "Request Name"))
        self.select_list.topLevelItem(3).child(12).setText(0, _translate("MainWindow", "Search All"))
        self.select_list.topLevelItem(3).child(13).setText(0, _translate("MainWindow", "Real Time"))
        self.select_list.topLevelItem(3).child(14).setText(0, _translate("MainWindow", "Short cut"))
        self.select_list.topLevelItem(4).setText(0, _translate("MainWindow", "Worklist"))
        self.select_list.topLevelItem(4).child(0).setText(0, _translate("MainWindow", "All Assigned List"))
        self.select_list.topLevelItem(4).child(1).setText(0, _translate("MainWindow", "Not Assigned List"))
        self.select_list.topLevelItem(4).child(2).setText(0, _translate("MainWindow", "All List"))
        self.select_list.topLevelItem(4).child(3).setText(0, _translate("MainWindow", "Schedule"))
        self.select_list.topLevelItem(4).child(4).setText(0, _translate("MainWindow", "Priority"))
        self.select_list.topLevelItem(4).child(5).setText(0, _translate("MainWindow", "Canceled"))
        self.select_list.topLevelItem(4).child(6).setText(0, _translate("MainWindow", "Refer"))
        self.select_list.topLevelItem(4).child(7).setText(0, _translate("MainWindow", "Refer Cancel"))
        self.select_list.topLevelItem(4).child(8).setText(0, _translate("MainWindow", "Refer Cancel and Refer"))
        self.select_list.topLevelItem(4).child(9).setText(0, _translate("MainWindow", "Set Schedule"))
        self.select_list.topLevelItem(4).child(10).setText(0, _translate("MainWindow", "Schedule Cancel"))
        self.select_list.topLevelItem(4).child(11).setText(0, _translate("MainWindow", "Revised"))
        self.select_list.topLevelItem(4).child(12).setText(0, _translate("MainWindow", "Discard"))
        self.select_list.topLevelItem(4).child(13).setText(0, _translate("MainWindow", "Retry Request"))
        self.select_list.topLevelItem(4).child(14).setText(0, _translate("MainWindow", "Columns"))
        self.select_list.topLevelItem(4).child(15).setText(0, _translate("MainWindow", "Show entries"))
        self.select_list.topLevelItem(4).child(16).setText(0, _translate("MainWindow", "Sort by"))
        self.select_list.topLevelItem(4).child(17).setText(0, _translate("MainWindow", "Worklist"))
        self.select_list.topLevelItem(5).setText(0, _translate("MainWindow", "Statistics"))
        self.select_list.topLevelItem(5).child(0).setText(0, _translate("MainWindow", "Search Filter"))
        self.select_list.topLevelItem(5).child(0).child(0).setText(0, _translate("MainWindow", "Date"))
        self.select_list.topLevelItem(5).child(0).child(1).setText(0, _translate("MainWindow", "Hospital"))
        self.select_list.topLevelItem(5).child(0).child(2).setText(0, _translate("MainWindow", "Reporter"))
        self.select_list.topLevelItem(5).child(0).child(3).setText(0, _translate("MainWindow", "Modality"))
        self.select_list.topLevelItem(5).child(0).child(4).setText(0, _translate("MainWindow", "Export"))
        self.select_list.topLevelItem(5).child(1).setText(0, _translate("MainWindow", "Columns"))
        self.select_list.topLevelItem(5).child(2).setText(0, _translate("MainWindow", "Show entries"))
        self.select_list.topLevelItem(6).setText(0, _translate("MainWindow", "Configure"))
        self.select_list.topLevelItem(6).child(0).setText(0, _translate("MainWindow", "User Management"))
        self.select_list.topLevelItem(6).child(0).child(0).setText(0, _translate("MainWindow", "Search Filter"))
        self.select_list.topLevelItem(6).child(0).child(0).child(0).setText(0, _translate("MainWindow", "Class"))
        self.select_list.topLevelItem(6).child(0).child(0).child(1).setText(0, _translate("MainWindow", "Institution"))
        self.select_list.topLevelItem(6).child(0).child(0).child(2).setText(0, _translate("MainWindow", "User ID"))
        self.select_list.topLevelItem(6).child(0).child(0).child(3).setText(0, _translate("MainWindow", "User Name"))
        self.select_list.topLevelItem(6).child(0).child(0).child(4).setText(0, _translate("MainWindow", "Show with Mapping ID"))
        self.select_list.topLevelItem(6).child(0).child(1).setText(0, _translate("MainWindow", "User Registration"))
        self.select_list.topLevelItem(6).child(0).child(1).child(0).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(0).child(1).child(1).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(0).child(1).child(2).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(1).setText(0, _translate("MainWindow", "Specialty"))
        self.select_list.topLevelItem(6).child(1).child(0).setText(0, _translate("MainWindow", "Specialty List"))
        self.select_list.topLevelItem(6).child(1).child(0).child(0).setText(0, _translate("MainWindow", "Search"))
        self.select_list.topLevelItem(6).child(1).child(0).child(1).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(1).child(0).child(2).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(1).child(0).child(3).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(1).child(1).setText(0, _translate("MainWindow", "Institution List"))
        self.select_list.topLevelItem(6).child(1).child(1).child(0).setText(0, _translate("MainWindow", "Search"))
        self.select_list.topLevelItem(6).child(1).child(1).child(1).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(1).child(1).child(2).setText(0, _translate("MainWindow", "Add - Export"))
        self.select_list.topLevelItem(6).child(1).child(1).child(3).setText(0, _translate("MainWindow", "Add - Import"))
        self.select_list.topLevelItem(6).child(1).child(1).child(4).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(1).child(1).child(5).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(1).child(1).child(6).setText(0, _translate("MainWindow", "Modify - Export"))
        self.select_list.topLevelItem(6).child(1).child(1).child(7).setText(0, _translate("MainWindow", "Modify - Import"))
        self.select_list.topLevelItem(6).child(1).child(1).child(8).setText(0, _translate("MainWindow", "Modify - Search"))
        self.select_list.topLevelItem(6).child(2).setText(0, _translate("MainWindow", "Download Control"))
        self.select_list.topLevelItem(6).child(2).child(0).setText(0, _translate("MainWindow", "User"))
        self.select_list.topLevelItem(6).child(2).child(0).child(0).setText(0, _translate("MainWindow", "Search Filter - Class"))
        self.select_list.topLevelItem(6).child(2).child(0).child(1).setText(0, _translate("MainWindow", "Search Filter - Insitution"))
        self.select_list.topLevelItem(6).child(2).child(0).child(2).setText(0, _translate("MainWindow", "Search Filter - User ID"))
        self.select_list.topLevelItem(6).child(2).child(0).child(3).setText(0, _translate("MainWindow", "Search Filter - User Name"))
        self.select_list.topLevelItem(6).child(2).child(0).child(4).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(2).child(0).child(5).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(2).child(0).child(6).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(2).child(1).setText(0, _translate("MainWindow", "Institution"))
        self.select_list.topLevelItem(6).child(2).child(1).child(0).setText(0, _translate("MainWindow", "Search Filter - Class"))
        self.select_list.topLevelItem(6).child(2).child(1).child(1).setText(0, _translate("MainWindow", "Search Filter - Insitution"))
        self.select_list.topLevelItem(6).child(2).child(1).child(2).setText(0, _translate("MainWindow", "Search Filter - User ID"))
        self.select_list.topLevelItem(6).child(2).child(1).child(3).setText(0, _translate("MainWindow", "Search Filter - User Name"))
        self.select_list.topLevelItem(6).child(2).child(1).child(4).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(2).child(1).child(5).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(2).child(1).child(6).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(3).setText(0, _translate("MainWindow", "Institution"))
        self.select_list.topLevelItem(6).child(3).child(0).setText(0, _translate("MainWindow", "Search Filter"))
        self.select_list.topLevelItem(6).child(3).child(0).child(0).setText(0, _translate("MainWindow", "Institution Code"))
        self.select_list.topLevelItem(6).child(3).child(0).child(1).setText(0, _translate("MainWindow", "Institution Name"))
        self.select_list.topLevelItem(6).child(3).child(1).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(3).child(2).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(3).child(3).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(4).setText(0, _translate("MainWindow", "Standard Report"))
        self.select_list.topLevelItem(6).child(4).child(0).setText(0, _translate("MainWindow", "Expender Folder"))
        self.select_list.topLevelItem(6).child(4).child(1).setText(0, _translate("MainWindow", "Group Add"))
        self.select_list.topLevelItem(6).child(4).child(2).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(4).child(3).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(4).child(4).setText(0, _translate("MainWindow", "Group Modify"))
        self.select_list.topLevelItem(6).child(4).child(5).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(6).child(5).setText(0, _translate("MainWindow", "Multi Reading Center Rule"))
        self.select_list.topLevelItem(6).child(5).child(0).setText(0, _translate("MainWindow", "Search Filter"))
        self.select_list.topLevelItem(6).child(5).child(1).setText(0, _translate("MainWindow", "Add"))
        self.select_list.topLevelItem(6).child(5).child(2).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(6).child(5).child(3).setText(0, _translate("MainWindow", "Modify"))
        self.select_list.topLevelItem(7).setText(0, _translate("MainWindow", "Audit Log"))
        self.select_list.topLevelItem(7).child(0).setText(0, _translate("MainWindow", "Search"))
        self.select_list.topLevelItem(7).child(1).setText(0, _translate("MainWindow", "Export"))
        self.select_list.topLevelItem(7).child(2).setText(0, _translate("MainWindow", "Show entries"))
        self.select_list.topLevelItem(7).child(3).setText(0, _translate("MainWindow", "Sorting"))
        self.select_list.topLevelItem(7).child(4).setText(0, _translate("MainWindow", "Data"))
        self.select_list.topLevelItem(8).setText(0, _translate("MainWindow", "Notice"))
        self.select_list.topLevelItem(8).child(0).setText(0, _translate("MainWindow", "Notice List"))
        self.select_list.topLevelItem(8).child(0).child(0).setText(0, _translate("MainWindow", "Notice Edit Board"))
        self.select_list.topLevelItem(8).child(0).child(1).setText(0, _translate("MainWindow", "Edit"))
        self.select_list.topLevelItem(8).child(0).child(2).setText(0, _translate("MainWindow", "Delete"))
        self.select_list.topLevelItem(8).child(0).child(3).setText(0, _translate("MainWindow", "Display"))
        self.select_list.topLevelItem(9).setText(0, _translate("MainWindow", "Direct Message"))
        self.select_list.topLevelItem(9).child(0).setText(0, _translate("MainWindow", "Direct Message Box"))
        self.select_list.topLevelItem(9).child(0).child(0).setText(0, _translate("MainWindow", "Search"))
        self.select_list.topLevelItem(9).child(0).child(1).setText(0, _translate("MainWindow", "Show Entries"))
        self.select_list.topLevelItem(9).child(0).child(2).setText(0, _translate("MainWindow", "Sorting"))
        self.select_list.topLevelItem(9).child(0).child(3).setText(0, _translate("MainWindow", "Badge"))
        self.select_list.topLevelItem(9).child(0).child(4).setText(0, _translate("MainWindow", "Message"))
        self.select_list.topLevelItem(9).child(0).child(5).setText(0, _translate("MainWindow", "Institution - Search"))
        self.select_list.topLevelItem(9).child(0).child(6).setText(0, _translate("MainWindow", "Institution - Message"))
        self.select_list.topLevelItem(9).child(0).child(7).setText(0, _translate("MainWindow", "Center - Search"))
        self.select_list.topLevelItem(9).child(0).child(8).setText(0, _translate("MainWindow", "Center - Message"))
        self.select_list.topLevelItem(9).child(0).child(9).setText(0, _translate("MainWindow", "Reporter - Search"))
        self.select_list.topLevelItem(9).child(0).child(10).setText(0, _translate("MainWindow", "Reporter - Message"))
        self.select_list.topLevelItem(9).child(1).setText(0, _translate("MainWindow", "Direct Message Setting"))
        self.select_list.topLevelItem(9).child(1).child(0).setText(0, _translate("MainWindow", "Search"))
        self.select_list.topLevelItem(9).child(1).child(1).setText(0, _translate("MainWindow", "Authorize"))
        self.select_list.topLevelItem(9).child(1).child(2).setText(0, _translate("MainWindow", "Selection"))
        self.select_list.setSortingEnabled(__sortingEnabled)
        self.btn_close.setText(_translate("MainWindow", "Close"))
        self.btn_move_to_right.setText(_translate("MainWindow", ">"))
        self.btn_run_test.setText(_translate("MainWindow", "Run Test"))
        self.btn_planid.setText(_translate("MainWindow", "Test Plan ID"))
        self.btn_deselect_all.setText(_translate("MainWindow", "<<"))
        self.btn_select_all.setText(_translate("MainWindow", ">>"))
        self.btn_move_to_left.setText(_translate("MainWindow", "<"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Test Plan"))
        self.label_9.setText(_translate("MainWindow", "100"))
        self.label_12.setText(_translate("MainWindow", "4"))
        self.label.setText(_translate("MainWindow", "Summary"))
        self.label_3.setText(_translate("MainWindow", "Passed"))
        self.label_5.setText(_translate("MainWindow", "Not Excuted"))
        self.label_6.setText(_translate("MainWindow", "Exception"))
        self.label_7.setText(_translate("MainWindow", "Execution Progress -"))
        self.label_8.setText(_translate("MainWindow", "00% executed"))
        self.label_2.setText(_translate("MainWindow", "Test Case"))
        self.label_4.setText(_translate("MainWindow", "Failed"))
        self.label_11.setText(_translate("MainWindow", "5"))
        self.label_10.setText(_translate("MainWindow", "0"))
        self.label_13.setText(_translate("MainWindow", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Test Status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())