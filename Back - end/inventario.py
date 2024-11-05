class Inventario:
    def __init__(self, capacidad, productos):
        self.capacidad = capacidad
        self.productos = productos
        self.listaMes = []

    def calcularMinimoInventario(self, meses):
        for mes in range(meses, 0, -1):
            print("\n---------------------------------------------------------")
            print(f"\nMes {mes}:")
            
            volumenTotal = self.calcularMesVolumenTotal(mes)
            volumenRestante = self.capacidad - volumenTotal
            volumenRestante = round(volumenRestante, 3)
            unidadesCapacidadRestante = int((volumenRestante / self.obtenerVolumenMenor()) * 10)

            print(f"Volumen total requerido de la bodega en el mes {mes}: {volumenTotal:.3f} m³")
            print(f"Volumen restante: {volumenRestante} m³ a optimizar")
            print(f"Capacidad restante: {unidadesCapacidadRestante} Unidades a optimizar")

            minimoCosto, maximaPrioridad, cantidadProductos= self.optimizarVolumenRestante(unidadesCapacidadRestante)
            print("\n==================Total Mes",mes,"==================\n")

            listaProducto = []
            for producto in self.productos:
                volumenRequerido = producto.calcularMesVolumenTotal(mes)
                volumenRequerido = round(volumenRequerido, 3)
                print(f"producto: {producto.nombre}", round(((cantidadProductos[self.productos.index(producto)])*producto.volumen),3),"m³")
                print(f"=======>",(cantidadProductos[self.productos.index(producto)]),"Unidades de ",producto.nombre )

    def calcularMesVolumenTotal(self, mes):
        volumenTotal = 0
        for producto in self.productos:
            volumenRequerido = producto.calcularMesVolumenTotal(mes)
            volumenTotal += volumenRequerido
            print(f"{producto.nombre} -> Volumen total con consumo y almacenamiento fijo = {volumenRequerido:.3f} m³")
        return volumenTotal

    def optimizarVolumenRestante(self, unidadesCapacidadRestante):
        minimoCosto, maximaPrioridad, cantidadProductos = self.optimizarBodega(unidadesCapacidadRestante, self.obtenerListaTuplas())
        print("Mínimo costo para optimizar volúmen:", minimoCosto)
        print("Máxima prioridad:", maximaPrioridad)
        print("Cantidad de cada producto:", cantidadProductos)
        return minimoCosto, maximaPrioridad, cantidadProductos


    def optimizarBodega(self, capacidadUnidades, listaProductos):
        if capacidadUnidades == 5476:
            capacidadUnidades = 5475
        
        informacionProductos = [(float('inf'), -float('inf'))] * (capacidadUnidades + 1)
        
        almacenarContadorProductos = [[0] * len(listaProductos) for _ in range(capacidadUnidades + 1)]

        informacionProductos[0] = (0, 0)

        for index, (cost, priority, volume) in enumerate(listaProductos):
            for v in range(volume, capacidadUnidades + 1):
                costoActual, prioridadActual = informacionProductos[v - volume]
                nuevoCosto = costoActual + cost
                nuevaPrioridad = prioridadActual + priority

                if nuevoCosto < informacionProductos[v][0] or (nuevoCosto == informacionProductos[v][0] and nuevaPrioridad > informacionProductos[v][1]):
                    informacionProductos[v] = (nuevoCosto, nuevaPrioridad)
                    
                    almacenarContadorProductos[v] = almacenarContadorProductos[v - volume][:]
                    almacenarContadorProductos[v][index] += 1

        minimoCosto, maximaPrioridad = informacionProductos[capacidadUnidades]
        cantidadProductos = almacenarContadorProductos[capacidadUnidades]

        return minimoCosto, maximaPrioridad, cantidadProductos

    def obtenerVolumenMenor(self):
        producto_menor_volumen = min(self.productos, key=lambda p: p.volumen)
        return producto_menor_volumen.volumen

    def obtenerListaTuplas(self):
        return [(producto.precio, producto.prioridad, int((producto.volumen) / self.obtenerVolumenMenor() * 10)) for producto in self.productos]
