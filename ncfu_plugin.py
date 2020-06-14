# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NcfuPlugin
                                 A QGIS plugin
 Plugin with the many options
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-14
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Kurban M.K.
        email                : mr.gustav009@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Инициализировать ресурсы Qt из файла resources.py
from .resources import *
# Импорт код для диалогового окна
from .ncfu_plugin_dialog import NcfuPluginDialog
import os.path


class NcfuPlugin:
    """Реализация плагина QGIS."""

    def __init__(self, iface):
        """Конструктор. """
        # Сохранить ссылку на интерфейс QGIS
        self.iface = iface
        # инициализировать катол плагина
        self.plugin_dir = os.path.dirname(__file__)
        # инициализировать locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NcfuPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Объявить атрибуты экземпляра
        self.actions = []
        self.menu = self.tr(u'&NCFU KGI-161')

        # Проверить, был ли плагин запущен в первый раз в текущей сессии QGIS
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        return QCoreApplication.translate('NcfuPlugin', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Добавить значок панели инструментов на панель инструментов. """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Добавить значок плагина на панель инструментов плагинов
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Создать пункты меню и значки панели инструментов внутри графического интерфейса QGIS."""

        icon_path = ':/plugins/ncfu_plugin/icon.png' # путь до значка плагина
        self.add_action(
            icon_path,
            text=self.tr(u'Work with data'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # будет установлено False при run()
        self.first_start = True


    def unload(self):
        """Удаляет пункт меню и значок плагина из QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&NCFU KGI-161'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Главный запуск """

        if self.first_start == True:
            self.first_start = False  # смена значения у первого запуска
            self.dlg = NcfuPluginDialog() # установка диалогового окна

        # показать диалоговое окно
        self.dlg.show()

        # Запустить цикл событий диалога
        result = self.dlg.exec_()

        # Выполнить функционал после нажатия "ОК" в модальном окне
        if result:
            # Главный алгоритм действий
            print("Проверка работоспособности.")
