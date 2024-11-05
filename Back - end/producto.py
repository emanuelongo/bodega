class Producto:
    def __init__(self, nombre, volumen, precio, inventarioMinimo, consumoPromedio, prioridad):
        self.nombre = nombre
        self.volumen = volumen
        self.precio = precio
        self.inventarioMinimo = inventarioMinimo
        self.consumoPromedio = consumoPromedio
        self.prioridad = prioridad
        self.almacenamientoFijo = 0.25

    def calcularMinimoConsumo(self, mes):
        return self.consumoPromedio * (1.2 ** (mes - 1)) * self.volumen

    def calcularMesVolumenTotal(self, mes):
        consumoMinimo = self.calcularMinimoConsumo(mes)
        return self.almacenamientoFijo + consumoMinimo
