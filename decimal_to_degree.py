# Импорты QGIS компонентов
from qgis.core import QgsField
from qgis.PyQt.QtCore import *

# Импорт собственных классов
from .convert_to_graduses import convertToGraduses    
from .error_handler import ErrorHandler

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
        
        dp = self.dp
        x  = 'xgrads'
        y  = 'ygrads'

        # Если атрибуты не были созданы – создать
        if dp.fieldNameIndex( x ) == -1 or dp.fieldNameIndex( y ) == -1:
            
            # Через формулу API QGIS создать новые атрибуты
            dp.addAttributes( [QgsField( x, QVariant.String )] )
            dp.addAttributes( [QgsField( y, QVariant.String )] )

            # Уведомить в консоле
            print('Созданы новые атрибуты ' + x + ', ' + y)
            
        else:
            print('Атрибуты ' + x + ', ' + y + ' уже созданы')

    def fillAttr(self):
        """Заполнить атрибуты """
        
        # Деструктуризация
        points = self.points
        dp     = self.dp

        # Получить доступ к атрибутам
        xAttrInd = dp.fieldNameIndex( 'xgrads' )
        yAttrInd = dp.fieldNameIndex( 'ygrads' )

        # Цикл с точками
        for p in points:

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
            dp.changeAttributeValues({ p.id(): newXAttr })
            dp.changeAttributeValues({ p.id(): newYAttr })