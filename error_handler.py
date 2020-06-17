# Импорт QGIS компонента
from qgis.core import Qgis

class ErrorHandler:

    def __init__(self, infoBar, layer, dp):
        """Конструктор"""

        # Присвоить полученные значения
        self.infoBar = infoBar
        self.layer = layer
        self.dp = dp

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

        # Проверка наличе необходимых атрибутов
        elif dp.fieldNameIndex('xcoord') == -1:
            self.lostAttr('xcoord')
            return False

        elif dp.fieldNameIndex('ycoord') == -1:
            self.lostAttr('ycoord')
            return False

        else: return True

    def lostAttr(self, attr):
        """Указать какой атрибут отсутствует """

        self.infoBar.pushMessage("Отсуствуют необходимый атрибут " + attr + " с координатами", Qgis.Warning )
        return