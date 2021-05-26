# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ConvertDEMtoGeoTiff content
                                 A QGIS plugin
 The plugin to convert DEM to GeoTiff and Terrain RGB (Tiff).
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-05-31
        git sha              : $Format:%H$
        copyright            : (C) 2021 by MIERUNE Inc.
        email                : info@mierune.co.jp
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

from .convert_dem_to_geotiff_dialog import ConvertDEMtoGeoTiffDialog
from .convert_fgd_dem.converter import Converter


class ConvertDEMtoGeotiffContents:
    def __init__(self, iface):
        self.iface = iface
        self.dlg = ConvertDEMtoGeoTiffDialog()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.dlg.mQgsFileWidget_1.setFilePath(self.current_dir)
        self.dlg.mQgsFileWidget_2.setFilePath(self.current_dir)
        self.dlg.mQgsFileWidget_2.setStorageMode(QgsFileWidget.GetDirectory)
        self.dlg.mQgsProjectionSelectionWidget.setCrs(QgsProject.instance().crs())

        input_type = {
            'zip or xml': 1,
            'folder': 2,
        }
        for key in input_type:
            self.dlg.comboBox.addItem(key, input_type[key])
        self.dlg.comboBox.activated.connect(self.switch_input_type)

        output_type = {
            'only GeoTiff': 1,
            'GeoTiff & Terrain RGB': 2,
        }
        for key in output_type:
            self.dlg.comboBox_2.addItem(key, output_type[key])

        self.dlg.button_box.accepted.connect(self.convert_DEM)
        self.dlg.button_box.rejected.connect(self.dlg_cancel)

    def convert_DEM(self):
        self.import_path = self.dlg.mQgsFileWidget_1.filePath()
        self.geotiff_output_path = self.dlg.mQgsFileWidget_2.filePath()
        self.output_epsg = self.dlg.mQgsProjectionSelectionWidget.crs().authid()
        self.rgbify = self.dlg.comboBox_2.currentIndex()

        converter = Converter(
            import_path=self.import_path,
            output_path=self.geotiff_output_path,
            output_epsg=self.output_epsg,
            rgbify=self.rgbify
        )
        converter.dem_to_geotiff()

        output_layer = QgsRasterLayer(os.path.join(self.geotiff_output_path, 'output.tif'), 'output')
        QgsProject.instance().addMapLayer(output_layer)

        if self.rgbify:
            rgbify_layer = QgsRasterLayer(os.path.join(self.geotiff_output_path, 'rgbify.tif'), 'rgbify')
            QgsProject.instance().addMapLayer(rgbify_layer)

        return True

    def dlg_cancel(self):
        self.dlg.hide()

    def switch_input_type(self):
        if self.dlg.comboBox.currentData() == 1:
            self.dlg.mQgsFileWidget_1.setStorageMode(QgsFileWidget.GetMultipleFiles)
        else:
            self.dlg.mQgsFileWidget_1.setStorageMode(QgsFileWidget.GetDirectory)

