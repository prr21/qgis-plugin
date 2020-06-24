"""
/***************************************************************************
 NcfuPlugin
                                 A QGIS plugin
 Converting decimal coordinates to degrees
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
# Импорты QGIS компонентов
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Инициализировать ресурсы Qt из файла resources.py
from .resources import *

# Импорт код для диалогового окна
from .ncfu_plugin_dialog import NcfuPluginDialog

# Импорт классов
from .decimal_to_degree import DecimalToDegree
from .error_handler import ErrorHandler

# Прочие импорты
import os.path
import qgis.utils


class NcfuPlugin:
    """Главный класс плагина."""

    def __init__(self, iface):
        """Конструктор. """

        # Присвоить полученные значения
        self.iface = iface                          # Сохранить ссылку на интерфейс QGIS
        self.infoBar = self.iface.messageBar()      # Сохранить ссылку на окне уведомлений
        self.plugin_dir = os.path.dirname(__file__) # Сохранить путь папки плагина

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

        self.first_start = None # Проверка на первый запуск текущей сессии QGIS

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

        self.add_action(
            QIcon(os.path.join(os.path.dirname(__file__), "icon.png")),
            text=self.tr(u'Convert decimal coordinates to degrees'),
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
            self.first_start = False        # смена значения у первого запуска
            self.dlg = NcfuPluginDialog()   # установка диалогового окна
       
    #    Получить значения из диалогового окна
        cmBox = self.dlg.comboBox
        cmBox.clear()

        self.dlg.show() # показать диалоговое окно
        
        # Получить все слои QGIS
        allLayers = self.iface.mapCanvas().layers()
        activeLayers = []

        # Отобразить все слои в списке
        for l in allLayers:
            activeLayers.append(l.name())

        # Выполнить функционал после нажатия "ОК" в модальном окне
        cmBox.addItems(activeLayers)
        result = self.dlg.exec_()

        if result:
            """ Главный алгоритм действий """

            layer = allLayers[ cmBox.currentIndex() ]  # Присвоить выбранный слой

            # Если слой не подходит по условиям – отмена
            if not layer:
                self.infoBar.pushMessage("Слой не выбран", Qgis.Critical )
                return

            dp = layer.dataProvider()    # поставщик данных
            points = layer.getFeatures() # получить точки из слоя

            # Закончить если слой не прошел проверку
            gradErr = ErrorHandler(self.infoBar, dp, layer, self.dlg)
            if not gradErr.checkOnErrsGrad(): return

            # Создать экземпляр класса
            layGrads = DecimalToDegree(dp, self.dlg, points)

            # Создать атрибуты градусов
            layGrads.createField()
            self.infoBar.pushMessage("Данные обновлены", Qgis.Success )

            layGrads.fillAttr() # Заполнить атрибуты градусов
            layer.updateFields() # Обновить данные

            # Уведомить пользователя об успешном выполнении
            print('Операция выполнена успешна!')
            return
