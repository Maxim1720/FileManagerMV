# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\py_projects\temp\form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import subprocess
import os
import threading
import psutil
import pickle
import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 520)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.logButtonFrame = QtWidgets.QFrame(Form)
        self.logButtonFrame.setMinimumSize(QtCore.QSize(0, 40))
        self.logButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logButtonFrame.setObjectName("logButtonFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.logButtonFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.logButtonFrame)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.killButton = QtWidgets.QPushButton(self.logButtonFrame)
        self.killButton.setMinimumSize(QtCore.QSize(150, 0))
        self.killButton.setObjectName("killButton")
        self.horizontalLayout.addWidget(self.killButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.logButtonFrame, 2, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setMinimumSize(QtCore.QSize(432, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        item = QtWidgets.QTableWidgetItem()
        item.setText("PID")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Created on")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)        
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.logfileLineEdit = QtWidgets.QLineEdit(Form)
        self.logfileLineEdit.setObjectName("logfileLineEdit")
        self.gridLayout.addWidget(self.logfileLineEdit, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OS FileManager Processes"))
        self.pushButton.setText(_translate("Form", "Save to log file"))
        self.killButton.setText(_translate("Form", "Kill Process"))        
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Name"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "File Path"))


class ProcWindow(Ui_Form):
    def __init__(self, Form, memcache=None) -> None:
        super().__init__()
        self.setupUi(Form)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.memcache = memcache
        self.logfileLineEdit.setText('log/log_processes.txt')
        self.processes_memory = list()
        self.processes_data = list()
        self.tableWidget.clearContents()            
        self.pushButton.clicked.connect(self.save_button_onclick)
        self.killButton.clicked.connect(self.kill_button_onclick)

        if memcache:
            self.memory_thread = threading.Thread(target=self.access_memory)
            self.memory_thread.setDaemon(True)
            self.memory_thread.start()

    def access_memory(self):
        while True:
            if os.path.getsize(self.memcache) > 0:           
                with open(self.memcache, 'rb') as input:
                    self.processes_data = pickle.load(input)
            
            i = len(self.processes_memory)
            j = len(self.processes_data) 
            if i < j:
                for elem in self.processes_data[i:]:
                    self.processes_memory.append(elem)
                    try:
                        self.rp = self.tableWidget.rowCount()
                    except:
                        self.rp += 1
                    self.input_elem_to_table(elem, self.rp)
            time.sleep(1)

    def input_elem_to_table(self, elem, rowPosition):
        self.tableWidget.insertRow(rowPosition)
        e1, e2, e3, e4 = elem

        self.tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(f'{e1}'))
        self.tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(f'{e2}'))
        self.tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(f'{e3}'))
        self.tableWidget.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(f'{e4}'))

    def save_button_onclick(self):
        with open(os.getcwd() + '/' + self.logfileLineEdit.text(), 'w') as f:
            for e in self.processes_memory:
                print(*e, sep=', ', file=f)

    def kill_button_onclick(self):
        item = self.tableWidget.selectedItems()
        pid = item[0].text()
        # subprocess.Popen(["sudo", "kill", "-9", f"{pid}"], shell=False)
        try:
            p = psutil.Process(int(pid))
            p.terminate()
        except:
            pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ProcWindow(Form)
    Form.show()
    sys.exit(app.exec_())
