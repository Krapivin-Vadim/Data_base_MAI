# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fam_dialog_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(333, 142)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 331, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 80, 301, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.update_button = QtWidgets.QPushButton(self.layoutWidget)
        self.update_button.setObjectName("update_button")
        self.horizontalLayout_2.addWidget(self.update_button)
        self.delete_button = QtWidgets.QPushButton(self.layoutWidget)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.insert_button = QtWidgets.QPushButton(self.layoutWidget)
        self.insert_button.setObjectName("insert_button")
        self.horizontalLayout_2.addWidget(self.insert_button)
        self.splitter_3 = QtWidgets.QSplitter(self.frame)
        self.splitter_3.setGeometry(QtCore.QRect(20, 10, 281, 51))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.where_label = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.where_label.setFont(font)
        self.where_label.setAcceptDrops(False)
        self.where_label.setAutoFillBackground(False)
        self.where_label.setAlignment(QtCore.Qt.AlignCenter)
        self.where_label.setObjectName("where_label")
        self.where_comboBox = QtWidgets.QComboBox(self.splitter)
        self.where_comboBox.setObjectName("where_comboBox")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.new_value_label = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.new_value_label.setFont(font)
        self.new_value_label.setAcceptDrops(False)
        self.new_value_label.setAutoFillBackground(False)
        self.new_value_label.setAlignment(QtCore.Qt.AlignCenter)
        self.new_value_label.setObjectName("new_value_label")
        self.new_value_lineEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.new_value_lineEdit.setObjectName("new_value_lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.update_button.setText(_translate("Dialog", "UPDATE"))
        self.delete_button.setText(_translate("Dialog", "DELETE"))
        self.insert_button.setText(_translate("Dialog", "INSERT"))
        self.where_label.setText(_translate("Dialog", "WHERE"))
        self.new_value_label.setText(_translate("Dialog", "New value"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())