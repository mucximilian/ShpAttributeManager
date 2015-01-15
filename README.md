# ShpAttributeManager

A python plugin for Quantum GIS (QGIS) providing tools for the management of attribute table values QGIS plugings are stored in the _.../python/plugins/_ directory of your QGIS directory, depending on your OS.

The main logic and the GUI of the tool are implemented, so it is already doing what it should do. With this tool it is possible to

* display all the unique attribute values of a attribute table field
* assign new attributes to features with a specific attribute
* delete all features with a specific attribute
* store the result in a new ESRI Shapefile

However, there is still quite a list of things that need to be fixed or improved:

* The layout
* Marking of features to delete in the table view
* Binding of the table cell with the edit dialog
* Enabling different data types for the new field (String, int, double)
* Checking the new field name for length and blanks
* Reset the dialogue when closed
* Displaying the faeture count somewhere...
* Adding a nice progress bar for processing
