# Импорт QGIS компонента
from qgis.core import QgsField

from .error_handler import ErrorHandler # Импорт обработчика ошибок
from math import trunc                  # Импорт матемаческой функции

class DecimalToDegree:
    """Класс реализации перевода градусов """

    def __init__(self, dp, points, countMs):
        """Конструктор"""

        # Присвоить полученные значения
        self.dp      = dp
        self.points  = points
        self.countMs = countMs
        self.xgrds   = 'xcoord_grds'
        self.ygrds   = 'ycoord_grds'

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

        # Сократить число до указанного числа
        def toFixed(ss):
            dig = self.countMs
            return f"{ss:.{dig}f}"

        # Формула перевода в градусную систему координат
        dd = trunc(ddd)                   # Граудсы = TRUNC(DDD)    
        mm = trunc( (ddd - dd) * 60 )     # Минуты  = TRUNC((DDD − DD) * 60)
        ss = ( (ddd-dd) * 60 - mm ) * 60  # Секунды = ((DDD − DD) * 60 − MM) * 60

        # Скоректировать формат чисел
        dd = f"{dd:02d}"
        mm = f"{mm:02d}"

        ss = toFixed(ss)
        ss = str(ss).replace('.', '\" ')

        # Переобразовать в читаемый формат и вернуть
        grads = str(dd)+'° '+str(mm)+" \' "+ss
        return grads

    def fillAttr(self):
        """Заполнить атрибуты """
        
        # Деструктуризация
        points = self.points
        dp     = self.dp
        x      = self.xgrds
        y      = self.ygrds
        
        # Получить доступ к атрибутам
        xAttrInd = dp.fieldNameIndex( x )
        yAttrInd = dp.fieldNameIndex( y )

        # Цикл с точками
        for p in points:

            # Получить значения десятичных координат
            valX = p.attribute('xcoord')
            valY = p.attribute('ycoord')

            # Результат конвертации присвоить новым переменным
            gradsX = self.convertToGraduses( valX )
            gradsY = self.convertToGraduses( valY )

            # Присвоить градусы соответствующей точке
            newXAttr = {xAttrInd : gradsX }
            newYAttr = {yAttrInd : gradsY }

            # Изменить значения атрибутов
            dp.changeAttributeValues({ p.id(): newXAttr })
            dp.changeAttributeValues({ p.id(): newYAttr })