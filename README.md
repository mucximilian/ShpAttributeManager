# ShpAttributeManager

A python plugin for Quantum GIS (QGIS) providing tools for the management of attribute table values.

## The tool

QGIS plugings are stored in the _.../python/plugins/_ directory of your QGIS directory, depending on your OS.

By now this is a first working prototype implementing the main logic and the GUI for the tool. It is more or less already doing what it should do. With this tool it is possible to:

* display all the unique attribute values of a attribute table field
* assign new attributes to features with a specific attribute
* delete all features with a specific attribute
* store the result in a new ESRI Shapefile

However, there is still quite a list of things that need to be fixed or improved...

## TO DOs

* The layout
* Marking of features to delete in the table view
* Better visual binding of the table cell with the edit dialog
* Enabling different data types for the new field (String, int, double)
* Checking the new field name for length and blanks
* Resetting the dialogue when closed
* Displaying the faeture count somewhere...
* Adding a progress bar for processing
* Adding new shapefile to the map after processing is finished

* * *

This software is released under the terms of the [MIT license](http://opensource.org/licenses/MIT).
