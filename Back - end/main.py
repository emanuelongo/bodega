from inventario import Inventario
from producto import Producto

papel = Producto("Papel higiénico", volumen = 0.005, precio = 2000, inventarioMinimo = 50, consumoPromedio = 50, prioridad = 2)
hipoclorito = Producto("Hipoclorito", volumen = 0.0125, precio = 1500, inventarioMinimo = 20, consumoPromedio = 20, prioridad = 3)
detergente = Producto("Detergente", volumen = 0.0125, precio = 5000, inventarioMinimo = 20, consumoPromedio = 30, prioridad= 4)

capacidadBodega = 5
inventario = Inventario(capacidadBodega, [papel, hipoclorito, detergente])

meses = 4
inventario.calcularMinimoInventario(meses)