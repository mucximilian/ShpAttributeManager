# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShpAttributeManager
                                 A QGIS plugin
 QGIS Plugin for managing the attribute table data of a shapfile
                             -------------------
        begin                : 2014-12-28
        copyright            : (C) 2014 by Max Hartl
        email                : m@xhartl.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ShpAttributeManager class from file ShpAttributeManager.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .shp_attribute_manager import ShpAttributeManager
    return ShpAttributeManager(iface)
