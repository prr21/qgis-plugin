# Импорт матемаческой функции
from math import trunc

class convertToGraduses:
    """Класс выполняющий конвертацию """

    def __init__(self, valX, valY, toMs, withWays):
        """Конструктор"""

        # Присвоить полученные значения
        self.withWays = withWays
        self.toMs = toMs
        self.x = valX
        self.y = valY

    def getGrads(self):
        """Получить градусы"""

        xWay = '' 
        yWay = ''

        if ( self.withWays ):
            xWay = self.getWay( self.x, 'x' )
            yWay = self.getWay( self.y, 'y' )

        xGrad = self.countByFormule( self.x, xWay )
        yGrad = self.countByFormule( self.y, yWay )

        return [xGrad, yGrad]

    def getWay(self, num, axis):
        """Получить сторону света """

        if ( num < 0 ):
            way = 'W' if axis == 'x' else 'S'
        else:
            way = 'E' if axis == 'x' else 'N'
        return way

    def countByFormule(self, ddd, way = ''):
        """Посчитать по формуле """

        ddd = abs(ddd) # Избваление отрицательного числа

        # Формула перевода в градусную систему координат
        dd = trunc(ddd)                     # Граудсы = TRUNC(DDD)    
        mm = trunc( (ddd - dd) * 60 )       # Минуты  = TRUNC((DDD − DD) * 60)
        ssms = ( (ddd-dd) * 60 - mm ) * 60  # Сек, мс = ((DDD − DD) * 60 − MM) * 60

        # Скоректировать формат чисел
        dd = f"{dd:02d}"
        mm = f"{mm:02d}"
        ss = self.formatSs(ssms)

        # Переобразовать в читаемый формат и вернуть
        grads = str(dd)+'°'+str(mm)+"\'"+ss + way
            #   59°30'58.9"N
        return grads    

    def formatSs(self, ssms):
        """Отформатировать секунды и милесекунды """
        dig = self.toMs 

        ss = trunc( ssms )      # Секунда
        ms = ssms - ss          # Милесекунды

        ss = f"{ss:02d}"        # 0 в начало если нужно
        ms = f"{ms:.{dig}f}"    # Сокращение милесекунд

        ssmsStr = str(ss) + str(ms) + '\"'
        newSsms = ssmsStr.replace('0.', '.')

        return newSsms