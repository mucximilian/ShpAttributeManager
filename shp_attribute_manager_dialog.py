# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShpAttributeManagerDialog
                                 A QGIS plugin
 QGIS Plugin for managing the attribute table data of a shapfile
                             -------------------
        begin                : 2014-12-28
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Max Hartl
        email                : m@xhartl.de
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

import qgis.utils
from qgis.core import *
from qgis.gui import *
import os
from PyQt4 import QtGui, QtCore, uic
from add_new_value_dialog import AddNewValueDialog
import datetime

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'shp_attribute_manager_dialog_base.ui'))

canvas = qgis.utils.iface.mapCanvas()

field_list = []

class ShpAttributeManagerDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ShpAttributeManagerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.addNewValueDialog = AddNewValueDialog()
        
        self.out_file_name = None
        
        self.btnCancel.clicked.connect(self.close)
        self.btnCancel.clicked.connect(self.addNewValueDialog.close)
        #self.btnUpdate.clicked.connect(self.getLayers)
        self.mMapLayerComboBox.activated.connect(self.getAttributes)
        self.cbxSelCol.activated.connect(self.getUniqueValues)
        self.tblAttrCurr.cellClicked.connect(self.editTableCell)
        self.btnExecute.clicked.connect(self.btnExecuteClicked)
        self.btnSelectFileLocation.clicked.connect(self.showSaveDialog)        
        self.btnExecute.setDisabled(True)
        self.txtFileLocation.setReadOnly(True)
        
        self.values_unique = []
        self.values_new = []
        self.values_matching = []
        
        self.selected_layer = None
        self.selected_field_idx = 0        
    
    def printBla(self):
        print "click"
        print self.mMapLayerComboBox.currentIndex()
    
    '''
    def getLayers(self):
        layer_list = []    
    
        self.mMapLayerComboBox.clear()        
        del layer_list[:]
        allLayers = canvas.layers()
        
        print "+++++++++++"
        
        layer_list.append("--- select layer ---")
        for layer in allLayers:            
            layer_list.append(layer.name())
            print layer.name()
    
        print str(len(layer_list) -1) + " layers available"        
        print "+++++++++++"
    
        self.mMapLayerComboBox.addItems(layer_list)
        self.cbxSelCol.clear()
    '''
        
    #####################################################################################################
    # retrievieng the attribute field names from the selected layer 
    def getAttributes(self):
        
        self.selected_layer = self.mMapLayerComboBox.currentLayer()
        
        try:                
            field_list = self.selected_layer.pendingAllAttributesList()        
            new_field_list = []        
            
            new_field_list.append("--- select column ---")
            for i in range(0, len(field_list)):
                #print layer.attributeDisplayName(i)
                new_field_list.append(self.selected_layer.attributeDisplayName(i))
                
            self.cbxSelCol.clear()
            self.cbxSelCol.addItems(new_field_list)
            
            self.txtOutput.append("Features in this layer: " + str(self.selected_layer.featureCount()))
            
        except AttributeError:
            self.txtOutput.append("No attribute data available...")
        
    #####################################################################################################
    # fill the QTable with unique values
    def getUniqueValues(self):
                      
        self.selected_field_idx = self.cbxSelCol.currentIndex()-1 # skipping the first combobox item
        print "selected attribute column = " + str(self.selected_field_idx)
        
        if self.cbxSelCol.currentIndex() == 0:
            print "Gnah..."
            self.txtOutput.append("No column selected")
        else:     
            # reset arrays
            self.values_new = []
            self.values_matching = []
              
            self.values_unique = self.selected_layer.dataProvider().uniqueValues(self.selected_field_idx)
            value_unique_count = len(self.values_unique)
            self.txtOutput.append("Unique values in this layer: " + str(value_unique_count))
            
            for unique_value in self.values_unique:
                self.values_matching.append([self.values_unique.index(unique_value), None])
            
            self.tblAttrCurr.setRowCount(value_unique_count)
            self.tblAttrCurr.setColumnCount(3)
            
            self.tblAttrCurr.setColumnWidth(0,  30)
            self.tblAttrCurr.setColumnWidth(1,  236)
            self.tblAttrCurr.setColumnWidth(2,  236)
            
            self.tblAttrCurr.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Delete?'))
            self.tblAttrCurr.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Unique Attribute values'))
            self.tblAttrCurr.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem('NEW Attribute values'))
        
            # filling table with unique values
            for i, value_unique in enumerate(self.values_unique):
                
                checkbox_item = QtGui.QTableWidgetItem()
                
                try:
                    item_unique = QtGui.QTableWidgetItem(value_unique)
                except TypeError:
                    self.txtOutput.append("Null type in attribute column...")
                    item_unique = QtGui.QTableWidgetItem("NULL")
                    
                item_unique_new = QtGui.QTableWidgetItem("")
                
                # make first column checkable
                checkbox_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                checkbox_item.setCheckState(QtCore.Qt.Unchecked)    
                
                # disable cell editing
                item_unique.setFlags(QtCore.Qt.ItemIsEnabled)
                item_unique_new.setFlags(QtCore.Qt.ItemIsEnabled)

                self.tblAttrCurr.setItem(i, 0, checkbox_item)
                self.tblAttrCurr.setItem(i, 1, item_unique)
                self.tblAttrCurr.setItem(i, 2, item_unique_new)
                
            self.btnExecute.setDisabled(False)
              
    #####################################################################################################
    # edit a table cell value             
    def editTableCell(self, row, column):
        
        print "editing cell " + str(row) + "," + str(column)
        
        item = self.tblAttrCurr.item(row, column)
        
        # mark fields with an attribute value for removal
        if item.column() == 0:
            if item.checkState() == QtCore.Qt.Checked:
                print str(row) + "," + str(column) + " checked"
                self.values_matching[row][1] = -1
            else:
                print str(row) + "," + str(column) + " unchecked" 
                self.values_matching[row][1] = None
        
            # print self.values_matching
                
        # open the dialog to add a new value in the table
        elif item.column() == 2:
            
            # make only cells selectable that are not marked for deletion
            if self.tblAttrCurr.item(row, 0).checkState() == QtCore.Qt.Checked:
                self.txtOutput.append("cannot edit this field")
            else:
                self.addNewValueDialog.updateTableAndUniqueValues(self.tblAttrCurr, self.values_unique, self.values_matching, row, column)
                self.addNewValueDialog.show()
      
    #####################################################################################################
    # open the dialog to save the edits in a new shapefile              
    def showSaveDialog(self):

        print self.selected_layer.name()        
        
        out_file_name = str(QtGui.QFileDialog.getSaveFileName(
            self, "Select output directory:", self.selected_layer.name() + "_edit.shp", "*.shp"))
        print out_file_name
            
        self.txtFileLocation.clear()
        self.txtFileLocation.setText(out_file_name)
        
    #####################################################################################################
    # open the dialog to save the edits in a new shapefile    
    def btnExecuteClicked(self):
        
        self.values_new = self.addNewValueDialog.getValuesNew()
        self.values_matching = self.addNewValueDialog.getValuesMatching()                
            
        print self.values_unique
        print self.values_new
        print self.values_matching        
        
        # check for correct inputs
        name_set = False
        location_set = False
        
        if self.txtNewFieldName.text() == "":
            self.txtOutput.append("please select a name for the new field")
        else:
            name_set = True
            
        if self.txtFileLocation.text() == "":            
            self.txtOutput.append("please select a location to store your new shapefile")    
        else:
            location_set = True
        
        if name_set & location_set:
            print str(datetime.datetime.now()) + " - processing"
            
            fields = self.selected_layer.pendingFields()
            
            field_is_unique = True
            
            new_field_name = self.txtNewFieldName.text()
            
            # check provided field name for uniqueness and length
            for field in fields:
                if field.name() == new_field_name:
                    self.txtOutput.append("provided name for new field is not unique...")
                    print "provided name for new field is not unique..."
                    field_is_unique = False 

            if field_is_unique:
                fields.append(QgsField(new_field_name, QtCore.QVariant.String))                
                
                # getting parameters of input shapefile                    
                wkb_type = self.selected_layer.wkbType()
                crs = self.selected_layer.crs()
                feature_count = self.selected_layer.featureCount()
                
                print wkb_type
                print crs.toWkt()
                print feature_count                
                
                print "creating shapefile " + self.txtFileLocation.text()
                
                writer = QgsVectorFileWriter(self.txtFileLocation.text(), "UTF-8", fields, wkb_type, crs, "ESRI Shapefile")
                
                if writer.hasError() != QgsVectorFileWriter.NoError:
                    print "error when creating shapefile: ", writer.hasError()
                    self.txtOutput.append("error when creating shapefile: ", writer.hasError())    
                    
                iter = self.selected_layer.getFeatures()
                
                for feature in iter:
                    print "===================================================="                         
                    print "feature ID %d: " % feature.id()
                                      
                    print str(feature.attributes())
                    
                    attributes = feature.attributes()
                    
                    # get the new attribute for this feature attribute
                    old_attribute = attributes[self.selected_field_idx]
                    new_attribute = self.getNewAttribute(old_attribute)                    
                    
                    print str(new_attribute)
                    
                    # only add the feature if it is not marked for deletion                                                            
                    if new_attribute is not None:                        
                        attributes.append(new_attribute)                            
                        
                        feature.setFields(fields, False)
                        feature.initAttributes(fields.count())                     
                        feature.setAttributes(attributes)
                            
                        print str(feature.attributes())
        
                        writer.addFeature(feature)
                    else:
                        print "deleting feature"                            
                
                # delete the writer to flush features to disk 
                del writer
                
                # resetting fields variable
                fields = None
                print str(datetime.datetime.now()) + " - processing done"
                self.txtOutput.append("processing done")
             
    # returns the new value of an original unique value 
    def getNewAttribute(self, old_attribute):
        idx_old_attribute = self.values_unique.index(old_attribute)
        idx_new_attribute = self.values_matching[idx_old_attribute][1]
                
        if idx_new_attribute is None or idx_new_attribute >= 0:
            try:
                new_value = self.values_new[idx_new_attribute]
            except TypeError:
                new_value = old_attribute
                print "no new value..."     
            return new_value
        else:
            return None