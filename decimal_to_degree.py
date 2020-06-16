from qgis.core import *
from qgis.PyQt.QtCore import *
from .error_handler import ErrorHandler # Импорт обработчика ошибок
from math import trunc                  # Импорт матемаческой функции

class DecimalToDegree:
    """Класс реализации перевода градусов """

    def createField(dp,way):
        """Создать новое поле"""
        
        dp.addAttributes( [QgsField( way, QVariant.String )] )
        print('Создан новый атрибут \"' +way+'\"')

    def convertToGraduses(ddd, countMs):
        """Конвертировать в градусы"""

        # Сократить число до определенного числа
        def toFixed(numObj, digits=0):
            return f"{numObj:.{digits}f}"

        # Формула перевода в градусную систему координат
        dd = trunc(ddd)                   # Граудсы = TRUNC(DDD)    
        mm = trunc( (ddd - dd) * 60 )     # Минуты  = TRUNC((DDD − DD) * 60)
        ss = ( (ddd-dd) * 60 - mm ) * 60  # Секунды = ((DDD − DD) * 60 − MM) * 60

        dd = f"{dd:02d}"
        mm = f"{mm:02d}"

        ss = toFixed(ss,countMs)
        ss = str(ss).replace('.', '\" ')

        # Переобразовать в читаемый формат
        grads = str(dd)+'° '+str(mm)+" \' "+ss

        return grads    

    def fillAttr(features, dp, countMs):
        """Заполнить атрибуты """
        
        # Получить значение десятичных координат
        xAttrInd = dp.fieldNameIndex('xcoord_grds')
        yAttrInd = dp.fieldNameIndex('ycoord_grds')

        # Цикл с точками
        for feat in features:

            # Получить значения десятичных координат
            valX = feat.attribute('xcoord')
            valY = feat.attribute('ycoord')

            # Результат конвертации присвоить новым переменным
            gradsX = DecimalToDegree.convertToGraduses( valX, countMs )
            gradsY = DecimalToDegree.convertToGraduses( valY, countMs )

            # Объявление новых атрибутов
            newXAttr = {xAttrInd : gradsX }
            newYAttr = {yAttrInd : gradsY }

            # Изменить значения атрибутов
            dp.changeAttributeValues({ feat.id(): newXAttr })
            dp.changeAttributeValues({ feat.id(): newYAttr })    