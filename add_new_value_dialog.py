# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShpTableManagerDialog
                                 A QGIS plugin
 QGIS Plugin for managing the attribute table data of a shapefile
                             -------------------
        begin                : 2014-12-18
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

import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'add_new_value.ui'))

class AddNewValueDialog(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(AddNewValueDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.values_new = []
        self.values_matching = []

        self.curr_row=0
        self.curr_column=0    
        
        self.tblAttrCurr = None;
        
        self.buttonBox.accepted.connect(self.updateCellValue)
        self.cbxSelNewValue.activated.connect(self.setToNewValue)
        self.cbxSelOriValue.activated.connect(self.setToOriginalValue)
    
    ############################################################################
    # Updates the table cell with the new attribute value as well as the
    # matching list
    def updateCellValue(self):
        print ("Setting data in cell "
            + str(self.curr_row) + ","
            + str(self.curr_column))
        
        # Update new value list and check for existing value
        value_text = self.txtNewValue.text()
        if (value_text == ""):            
            print "No text entered..."
        else:        
            item_unique_new = QtGui.QTableWidgetItem(value_text)
            self.tblAttrCurr.setItem(
                self.curr_row, self.curr_column, item_unique_new)
            self.addToValueList(value_text)            
            self.updateMatchingList(
                self.curr_row, self.values_new.index(value_text))
            
    ############################################################################
    # Assigns the new attribute value to the original attribute value in the 
    # matching list
    def updateMatchingList(self, row, value_new_index):
        self.values_matching[row][1] = value_new_index
        print self.values_matching[row]
        
    ############################################################################
    # Sets the new value to a value from the new value combobox
    def setToNewValue(self):
        new_value_text = self.cbxSelNewValue.itemText(
            self.cbxSelNewValue.currentIndex())
        self.txtNewValue.setText(new_value_text)
    
    ############################################################################
    # Sets the new value to a value from the original value combobox
    def setToOriginalValue(self):
        new_value_text = self.cbxSelOriValue.itemText(
            self.cbxSelOriValue.currentIndex())
        self.txtNewValue.setText(new_value_text)

    ############################################################################
    # Adds a new attribute value to the list of new values if not already in it
    def addToValueList(self, new_value):
        if new_value in self.values_new:
            print "value is already in list"
        else:
            self.values_new.append(new_value)
    
    ############################################################################
    # Updating the variables on cell click when dialog is shown
    def updateDialogData(
        self, tblAttrCurr, values_unique, values_matching, row, column):
        self.txtNewValue.clear()
        self.cbxSelNewValue.clear()
        self.cbxSelNewValue.addItems(self.values_new)
        self.cbxSelOriValue.addItems(values_unique)
        self.tblAttrCurr = tblAttrCurr
        self.values_matching = values_matching
        self.curr_row = row
        self.curr_column = column
    
    ############################################################################
    # Getting the new values list 
    def getValuesNew(self):
        return self.values_new

    ############################################################################
    # Getting the matching list
    def getValuesMatching(self):
        return self.values_matching