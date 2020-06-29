# Импорты QGIS компонентов
from qgis.core import QgsField
from qgis.PyQt.QtCore import *

from .convert_to_graduses import convertToGraduses # Импорт класса конвертации

class DecimalToDegree:
    """Класс реализации перевода градусов """

    def __init__(self, dp, data, points):
        """Конструктор"""

        # Присвоить полученные значения
        self.dp      = dp
        self.points  = points
        self.xcrd    = data.x_coord.text()
        self.ycrd    = data.y_coord.text()
        self.toMs    = data.spinBox.value()
        self.checked = data.checkBox.checkState()

    def createField(self):
        """Создать новое поле"""

        # Деструктуризация
        dp = self.dp
        
        # Если атрибуты не были созданы – создать
        if dp.fieldNameIndex( 'xgrads' ) == -1 or dp.fieldNameIndex( 'ygrads' ) == -1:
            
            # Через формулу API QGIS создать новые атрибуты
            dp.addAttributes( [QgsField( 'xgrads', QVariant.String )] )
            dp.addAttributes( [QgsField( 'ygrads', QVariant.String )] )

            # Уведомить в консоле
            print('Созданы новые атрибуты xgrads ygrads')
        else:
            print('Атрибуты xgrads, ygrads уже созданы')

    def fillAttr(self):
        """Заполнить атрибуты """

        # Получить доступ к атрибутам
        xAttrInd = self.dp.fieldNameIndex( 'xgrads' )
        yAttrInd = self.dp.fieldNameIndex( 'ygrads' )

        for p in self.points:

            # Получить значения десятичных координат
            valX = p.attribute( self.xcrd )
            valY = p.attribute( self.ycrd )

            # Экзамплер класс с градусами
            grads = convertToGraduses( valX, valY, self.toMs, self.checked )
            gradsArr = grads.getGrads()

            # Присвоить градусы соответствующей точке
            newXAttr = {xAttrInd : gradsArr[1] }
            newYAttr = {yAttrInd : gradsArr[0] }

            # Изменить значения атрибутов
            self.dp.changeAttributeValues({ p.id(): newXAttr })
            self.dp.changeAttributeValues({ p.id(): newYAttr })