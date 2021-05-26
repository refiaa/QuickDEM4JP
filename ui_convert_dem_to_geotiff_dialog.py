# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\convert_dem_to_geotiff_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from qgsfilewidget import QgsFileWidget
from qgsprojectionselectionwidget import QgsProjectionSelectionWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConvertDEMtoGeoTiffDialogBase(object):
    def setupUi(self, ConvertDEMtoGeoTiffDialogBase):
        ConvertDEMtoGeoTiffDialogBase.setObjectName(
            "ConvertDEMtoGeoTiffDialogBase")
        ConvertDEMtoGeoTiffDialogBase.resize(400, 312)
        self.button_box = QtWidgets.QDialogButtonBox(
            ConvertDEMtoGeoTiffDialogBase)
        self.button_box.setGeometry(QtCore.QRect(40, 270, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.label_1 = QtWidgets.QLabel(ConvertDEMtoGeoTiffDialogBase)
        self.label_1.setGeometry(QtCore.QRect(10, 70, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(ConvertDEMtoGeoTiffDialogBase)
        self.label_2.setGeometry(QtCore.QRect(10, 190, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ConvertDEMtoGeoTiffDialogBase)
        self.label_3.setGeometry(QtCore.QRect(10, 250, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.mQgsProjectionSelectionWidget = QgsProjectionSelectionWidget(
            ConvertDEMtoGeoTiffDialogBase)
        self.mQgsProjectionSelectionWidget.setGeometry(
            QtCore.QRect(10, 270, 191, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mQgsProjectionSelectionWidget.setFont(font)
        self.mQgsProjectionSelectionWidget.setObjectName(
            "mQgsProjectionSelectionWidget")
        self.mQgsFileWidget_1 = QgsFileWidget(ConvertDEMtoGeoTiffDialogBase)
        self.mQgsFileWidget_1.setGeometry(QtCore.QRect(10, 90, 381, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mQgsFileWidget_1.setFont(font)
        self.mQgsFileWidget_1.setObjectName("mQgsFileWidget_1")
        self.mQgsFileWidget_2 = QgsFileWidget(ConvertDEMtoGeoTiffDialogBase)
        self.mQgsFileWidget_2.setGeometry(QtCore.QRect(10, 210, 381, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mQgsFileWidget_2.setFont(font)
        self.mQgsFileWidget_2.setObjectName("mQgsFileWidget_2")
        self.label_4 = QtWidgets.QLabel(ConvertDEMtoGeoTiffDialogBase)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(ConvertDEMtoGeoTiffDialogBase)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 161, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(ConvertDEMtoGeoTiffDialogBase)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 150, 161, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_5 = QtWidgets.QLabel(ConvertDEMtoGeoTiffDialogBase)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(ConvertDEMtoGeoTiffDialogBase)
        self.button_box.accepted.connect(ConvertDEMtoGeoTiffDialogBase.accept)
        self.button_box.rejected.connect(ConvertDEMtoGeoTiffDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ConvertDEMtoGeoTiffDialogBase)

    def retranslateUi(self, ConvertDEMtoGeoTiffDialogBase):
        _translate = QtCore.QCoreApplication.translate
        ConvertDEMtoGeoTiffDialogBase.setWindowTitle(_translate("ConvertDEMtoGeoTiffDialogBase", "Convert_DEM_to_GeoTiff"))
        self.label_1.setText(_translate("ConvertDEMtoGeoTiffDialogBase", "DEM格納先"))
        self.label_2.setText(_translate("ConvertDEMtoGeoTiffDialogBase", "GeoTiff出力フォルダ"))
        self.label_3.setText(_translate("ConvertDEMtoGeoTiffDialogBase", "参照先EPSGコード"))
        self.label_4.setText(_translate("ConvertDEMtoGeoTiffDialogBase", "DEM入力形式"))
        self.label_5.setText(_translate("ConvertDEMtoGeoTiffDialogBase", "出力形式"))
