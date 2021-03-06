# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NcfuPlugin
                                 A QGIS plugin
 Plugin with the many options
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-05-14
        copyright            : (C) 2020 by Kurban M.K.
        email                : mr.gustav009@gmail.com
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
    """Load NcfuPlugin class from file NcfuPlugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .ncfu_plugin import NcfuPlugin

    return NcfuPlugin(iface)
