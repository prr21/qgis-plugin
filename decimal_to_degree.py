# Импорт QGIS компонента
from qgis.core import *
from qgis.PyQt.QtCore import *

from .error_handler import ErrorHandler # Импорт обработчика ошибок
from math import trunc                  # Импорт матемаческой функции

class DecimalToDegree:
    """Класс реализации перевода градусов """

    def __init__(self, dp, points, xcrd, ycrd, countMs):
        """Конструктор"""

        # Присвоить полученные значения
        self.dp      = dp
        self.points  = points
        self.countMs = countMs
        self.xcrd    = 'xcoord'
        self.ycrd    = 'ycoord'
        self.xgrds   = 'x_grads'
        self.ygrds   = 'y_grads'

    def createField(self):
        """Создать новое поле"""

        # Деструктуризация
        dp = self.dp
        x  = self.xgrds
        y  = self.ygrds

        # Если атрибуты не были созданы – создать
        if dp.fieldNameIndex( x ) == -1 or dp.fieldNameIndex( y ) == -1:
            
            # Через формулу API QGIS создать новые атрибуты
            dp.addAttributes( [QgsField( x, QVariant.String )] )
            dp.addAttributes( [QgsField( y, QVariant.String )] )

            # Уведомить
            print('Созданы новые атрибуты ' + x + ', ' + y)

        else:
            print('Атрибуты ' + x + ', ' + y + ' уже созданы')
        

    def convertToGraduses(self, ddd):
        """Конвертировать в градусы"""

        # Отформатировать секунды и милесекунды
        def formatSs(ssms):
            dig = self.countMs

            ss = trunc( ssms )
            ms = ssms - ss

            ss = f"{ss:02d}"
            ms = f"{ms:.{dig}f}"

            ssmsStr = str(ss) + str(ms)
            newSsms = ssmsStr.replace('0.', '\" ')

            return newSsms

        ddd = abs(ddd) # Преобразование отрицательного числа

        # Формула перевода в градусную систему координат
        dd = trunc(ddd)                     # Граудсы = TRUNC(DDD)    
        mm = trunc( (ddd - dd) * 60 )       # Минуты  = TRUNC((DDD − DD) * 60)
        ssms = ( (ddd-dd) * 60 - mm ) * 60  # Сек, мс = ((DDD − DD) * 60 − MM) * 60

        # Скоректировать формат чисел
        dd = f"{dd:02d}"
        mm = f"{mm:02d}"
        ss = formatSs(ssms)

        # Переобразовать в читаемый формат и вернуть
        grads = str(dd)+'° '+str(mm)+" \' "+ss
        return grads

    def fillAttr(self):
        """Заполнить атрибуты """
        
        # Деструктуризация
        points = self.points
        dp     = self.dp

        # Получить доступ к атрибутам
        xAttrInd = dp.fieldNameIndex( self.xgrds )
        yAttrInd = dp.fieldNameIndex( self.ygrds )

        # Цикл с точками
        for p in points:

            # Получить значения десятичных координат
            valX = p.attribute( self.xcrd )
            valY = p.attribute( self.ycrd )

            # Результат конвертации присвоить новым переменным
            gradsX = self.convertToGraduses( valX )
            gradsY = self.convertToGraduses( valY )

            # Присвоить градусы соответствующей точке
            newXAttr = {xAttrInd : gradsX }
            newYAttr = {yAttrInd : gradsY }

            # Изменить значения атрибутов
            dp.changeAttributeValues({ p.id(): newXAttr })
            dp.changeAttributeValues({ p.id(): newYAttr })