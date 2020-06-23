# Импорт QGIS компонента
from qgis.core import Qgis

class ErrorHandler:

    def __init__(self, infoBar, dp, layer, data):
        """Конструктор"""

        # Присвоить полученные значения
        self.infoBar = infoBar
        self.layer = layer
        self.dp = dp
        self.x = data.x_coord.text()
        self.y = data.y_coord.text()

    def checkOnErrsGrad(self):
        """Проверка всех условий """

        # Деструктуризация
        dp = self.dp
        layer = self.layer
        infoBar = self.infoBar

        # Если с точками не выбран
        if layer.geometryType() != 0:
            infoBar.pushMessage("Выберите слой с точками!", Qgis.Warning )
            return False

        # Проверка наличия необходимых атрибутов
        elif dp.fieldNameIndex( self.x ) == -1:
            self.lostAttr( self.x )
            return False

        elif dp.fieldNameIndex( self.y ) == -1:
            self.lostAttr( self.y )
            return False

        else: return True

    def lostAttr(self, attr):
        """Указать какой атрибут отсутствует """

        # Прислать уведомление с ошибкой
        self.infoBar.pushMessage('Отсуствуют указанный атрибут \"' + attr + '\" с координатами', Qgis.Warning )
        return
