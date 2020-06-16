
class ErrorHandler:
    # def __init__(self, pushTo):
    #     self.pushTo = pushTo
    #     print(pushTo)

    def checkOnErrors(pushTo, layer, dp):
        """Проверка всех условий """

        # Если с точками не выбран
        if layer.geometryType() != 0:
            pushTo.pushMessage("Выберите слой с точками!", Qgis.Warning )
            return False

        # Проверка наличе необходимых атрибутов
        elif dp.fieldNameIndex('xcoord') == -1:
            pushTo.lostAttr('xcoord')
            return False

        elif dp.fieldNameIndex('ycoord') == -1:
            pushTo.lostAttr('ycoord')
            return False

        else: return True

    def lostAttr(attr):
        """Указать какой атрибут отсутствует """
        pushTo.iface.pushMessage("Отсуствуют необходимый атрибут " + attr + " с координатами", Qgis.Warning )
        return