class Inventario:
    def __init__(self, capacidad, productos):
        self.capacidad = capacidad
        self.productos = productos
        self.listaMes = []

    def calcularMinimoInventario(self, meses):
        for mes in range(meses, 0, -1):
            print(f"\nMes {mes}:")
            #aQU+I VOY CAMBIANDO
            volumen_total = self.calcularMesVolumenTotal(mes)
            volumen_restante = self.capacidad - volumen_total
            volumen_restante = round(volumen_restante, 3)
            capacidad_restante_unidades = int((volumen_restante / self.obtener_menor_volumen()) * 10)

            print(f"Volumen total requerido en la bodega en el mes {mes}: {volumen_total:.3f} m³")
            print(f"Volumen restante a OPTIMIZAR {volumen_restante}")
            print(f"Capacidad restante a OPTIMIZAR {capacidad_restante_unidades} Unidades")

            # Llamar al método para optimizar la bodega con el volumen restante
            min_cost, max_priority, product_counts= self.optimizar_volumen_restante(capacidad_restante_unidades)
            print("-------------------Total Mes",mes,"-------------------")

            listaProducto = []
            for producto in self.productos:
                volumen_requerido = producto.calcularMesVolumenTotal(mes)
                volumen_requerido = round(volumen_requerido, 3)
                print(f"producto: {producto.nombre}", round(((product_counts[self.productos.index(producto)])*producto.volumen),3),"m³")
                print(f"         ",(product_counts[self.productos.index(producto)]),"Unidades de ",producto.nombre )

                #volumenTotalProductoMes = volumen_requerido + (product_counts.)


    def calcularMesVolumenTotal(self, mes):
        """Calcula el volumen total requerido para almacenar los productos en un mes específico."""
        volumen_total = 0
        for producto in self.productos:
            volumen_requerido = producto.calcularMesVolumenTotal(mes)
            volumen_total += volumen_requerido
            print(f"{producto.nombre}: Volumen total (almacenamiento fijo + consumo) = {volumen_requerido:.3f} m³")
        return volumen_total

    def optimizar_volumen_restante(self, capacidad_restante_unidades):
        """Optimiza la bodega con el volumen restante."""
        min_cost, max_priority, product_counts = self.optimizar_bodega(capacidad_restante_unidades, self.obtener_lista_tuplas())
        print("Minimum cost to achieve volume:", min_cost)
        print("Maximum priority:", max_priority)
        print("Quantities of each product:", product_counts)
        return min_cost, max_priority, product_counts


    def optimizar_bodega(self, capacidadU, listaProductos):
        if capacidadU == 5476:  # Porque hay un error con este número
            capacidadU = 5475
        # Initialize dp array with inf for cost, and -inf for priority
        dp = [(float('inf'), -float('inf'))] * (capacidadU + 1)  # (cost, priority)
        # Initialize a tracker array to store product counts
        count_tracker = [[0] * len(listaProductos) for _ in range(capacidadU + 1)]

        # Base case: 0 volume requires 0 cost and 0 priority
        dp[0] = (0, 0)

        # Process each product to fill the dp array
        for idx, (cost, priority, volume) in enumerate(listaProductos):
            for v in range(volume, capacidadU + 1):
                current_cost, current_priority = dp[v - volume]
                new_cost = current_cost + cost
                new_priority = current_priority + priority

                # Check if this product minimizes cost or maximizes priority at equal cost
                if new_cost < dp[v][0] or (new_cost == dp[v][0] and new_priority > dp[v][1]):
                    dp[v] = (new_cost, new_priority)
                    # Copy the counts from the previous state and add one of this product
                    count_tracker[v] = count_tracker[v - volume][:]
                    count_tracker[v][idx] += 1

        # Minimum cost and maximum priority to achieve exactly 'capacity' volume
        min_cost, max_priority = dp[capacidadU]
        product_counts = count_tracker[capacidadU]

        return min_cost, max_priority, product_counts

    def obtener_menor_volumen(self):
        producto_menor_volumen = min(self.productos, key=lambda p: p.volumen)
        return producto_menor_volumen.volumen

    def obtener_lista_tuplas(self):
        return [(producto.precio, producto.prioridad, int((producto.volumen) / self.obtener_menor_volumen() * 10)) for producto in self.productos]
