# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Contents
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
import webbrowser

from qgis.core import QgsProject, QgsRasterLayer
from qgis.gui import QgsFileWidget
from PyQt5.QtWidgets import QMessageBox

from .quick_dem_for_jp_dialog import QuickDEMforJPDialog
from .convert_fgd_dem.src.convert_fgd_dem.converter import Converter

from .progress_dialog import ProgressDialog


class Contents:
    def __init__(self, iface):
        self.iface = iface
        self.dlg = QuickDEMforJPDialog()

        self.dlg.mQgsFileWidget_inputPath.setFilePath(QgsProject.instance().homePath())
        self.dlg.mQgsFileWidget_inputPath.setStorageMode(QgsFileWidget.GetMultipleFiles)
        self.dlg.mQgsFileWidget_inputPath.setFilter("*.xml;;*.zip")

        self.dlg.mQgsFileWidget_outputPath.setFilePath(QgsProject.instance().homePath())
        self.dlg.mQgsFileWidget_outputPath.setFilter("*.tiff")
        self.dlg.mQgsFileWidget_outputPath.setDialogTitle(
            "保存ファイルを選択してください"
        )
        self.dlg.mQgsFileWidget_outputPathTerrain.setFilePath(
            QgsProject.instance().homePath()
        )
        self.dlg.mQgsFileWidget_outputPathTerrain.setFilter("*.tiff")
        self.dlg.mQgsFileWidget_outputPathTerrain.setDialogTitle(
            "保存ファイルを選択してください"
        )

        # set terrain path if changed
        self.dlg.mQgsFileWidget_outputPath.fileChanged.connect(self.set_terrain_path)
        self.dlg.checkBox_outputTerrainRGB.stateChanged.connect(self.set_terrain_path)

        self.dlg.mQgsProjectionSelectionWidget_outputCrs.setCrs(
            QgsProject.instance().crs()
        )

        self.dlg.radioButton_xmlzipfile.toggled.connect(self.switch_input_type)
        self.dlg.radioButton_folder.toggled.connect(self.switch_input_type)

        self.dlg.button_box.accepted.connect(self.convert_DEM)
        self.dlg.button_box.rejected.connect(self.dlg_cancel)

        self.dlg.downloadButton.clicked.connect(self.on_download_page_clicked)

        self.process_interrupted = False

    def convert(self, output_path, filename, rgbify):
        progress_dialog = ProgressDialog(None)

        thread = Converter(
            import_path=self.import_path,
            output_path=output_path,
            output_epsg=self.output_epsg,
            file_name=filename,
            rgbify=rgbify,
            sea_at_zero=self.dlg.checkBox_sea_zero.isChecked(),
        )

        progress_dialog.abortButton.clicked.connect(
            lambda: [
                self.on_abort_clicked(thread, progress_dialog),
            ]
        )
        # progress dialog orchestation by process thread
        thread.setMaximum.connect(progress_dialog.set_maximum)
        thread.addProgress.connect(progress_dialog.add_progress)
        thread.postMessage.connect(progress_dialog.set_message)
        thread.setAbortable.connect(progress_dialog.set_abortable)
        thread.processFinished.connect(progress_dialog.close)

        thread.start()
        progress_dialog.exec_()

    def add_layer(self, output_path, tiff_name, layer_name):
        layer = QgsRasterLayer(os.path.join(output_path, tiff_name), layer_name)
        QgsProject.instance().addMapLayer(layer)

    def convert_DEM(self):
        do_GeoTiff = self.dlg.checkBox_outputGeoTiff.isChecked()
        do_TerrainRGB = self.dlg.checkBox_outputTerrainRGB.isChecked()

        if not do_GeoTiff and not do_TerrainRGB:
            QMessageBox.information(
                None, "エラー", "出力形式にチェックを入れてください"
            )
            return

        self.import_path = self.dlg.mQgsFileWidget_inputPath.filePath()
        if not self.import_path:
            QMessageBox.information(None, "エラー", "DEMの入力先パスを入力してください")
            return

        self.output_path = self.dlg.mQgsFileWidget_outputPath.filePath()
        if do_GeoTiff and not self.output_path:
            QMessageBox.information(
                None, "エラー", "GeoTIFFの出力先パスを入力してください"
            )
            return

        self.output_path_terrain = self.dlg.mQgsFileWidget_outputPathTerrain.filePath()
        if do_TerrainRGB and not self.output_path_terrain:
            QMessageBox.information(
                None, "エラー", "Terrain RGBの出力先パスを入力してください"
            )
            return

        self.output_epsg = (
            self.dlg.mQgsProjectionSelectionWidget_outputCrs.crs().authid()
        )
        if not self.output_epsg:
            QMessageBox.information(None, "エラー", "DEMの出力CRSを入力してください")
            return

        do_add_layer = self.dlg.checkBox_openLayers.isChecked()

        try:
            if do_GeoTiff and not self.process_interrupted:
                # check if directory exists
                directory = os.path.dirname(self.output_path)
                if not os.path.isdir(directory):
                    QMessageBox.information(
                        None, "エラー", f"Cannot find output folder.\n{directory}"
                    )
                    return
                filename = os.path.basename(self.output_path)
                # Add .tiff to output path if missing
                if not filename.lower().endswith(".tiff"):
                    filename += ".tiff"

                self.convert(
                    output_path=os.path.dirname(self.output_path),
                    filename=filename,
                    rgbify=False,
                )
                if do_add_layer and not self.process_interrupted:
                    self.add_layer(
                        os.path.dirname(self.output_path),
                        tiff_name=filename,
                        layer_name=os.path.splitext(filename)[0],
                    )
            if do_TerrainRGB and not self.process_interrupted:
                # check if directory exists
                directory = os.path.dirname(self.output_path_terrain)
                if not os.path.isdir(directory):
                    QMessageBox.information(
                        None, "エラー", f"Cannot find output folder.\n{directory}"
                    )
                    return
                filename = os.path.basename(self.output_path_terrain)
                # Add .tiff to output path if missing
                if not filename.lower().endswith(".tiff"):
                    filename += ".tiff"

                self.convert(
                    os.path.dirname(self.output_path_terrain),
                    filename=filename,
                    rgbify=True,
                )
                if do_add_layer and not self.process_interrupted:
                    self.add_layer(
                        os.path.dirname(self.output_path_terrain),
                        tiff_name=filename,
                        layer_name=os.path.splitext(filename)[0],
                    )
        except Exception as e:
            QMessageBox.information(None, "エラー", f"{e}")
            return

        if not self.process_interrupted:
            QMessageBox.information(None, "完了", "処理が完了しました")

        self.dlg.hide()

        return True

    def dlg_cancel(self):
        self.dlg.hide()

    def switch_input_type(self):
        if self.dlg.radioButton_xmlzipfile.isChecked():
            self.dlg.mQgsFileWidget_inputPath.setStorageMode(
                QgsFileWidget.GetMultipleFiles
            )
        else:
            self.dlg.mQgsFileWidget_inputPath.setStorageMode(QgsFileWidget.GetDirectory)

    def set_terrain_path(self):
        # set Terrain file path automatically if path is not defined and Geotiff path is defined
        geotiff_path = self.dlg.mQgsFileWidget_outputPath.filePath()
        if (
            self.dlg.checkBox_outputTerrainRGB.isChecked()
            and os.path.splitext(geotiff_path)[1] == ".tiff"
            and not self.dlg.mQgsFileWidget_outputPathTerrain.filePath()
            .lower()
            .endswith(".tiff")
        ):
            terrain_path = (
                os.path.splitext(geotiff_path)[0]
                + f"_Terrain-RGB{os.path.splitext(os.path.basename(geotiff_path))[1]}"
            )
            self.dlg.mQgsFileWidget_outputPathTerrain.setFilePath(terrain_path)

    def on_download_page_clicked(self):
        webbrowser.open("https://fgd.gsi.go.jp/download/")
        return

    def on_abort_clicked(self, thread, progress_dialog: ProgressDialog) -> None:
        if QMessageBox.Yes == QMessageBox.question(
            None,
            "Aborting",
            "Are you sure to cancel process?",
            QMessageBox.Yes,
            QMessageBox.No,
        ):
            self.set_interrupted()
            thread.process_interrupted = True
            self.abort_process(thread, progress_dialog)

    def abort_process(self, thread, progress_dialog: ProgressDialog) -> None:
        if self.process_interrupted:
            thread.exit()
            progress_dialog.abort_dialog()
            self.dlg_cancel()
            return

    def set_interrupted(self):
        self.process_interrupted = True
