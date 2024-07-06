import heapq  #para trabajar con colas de prioridad

# definimos mapa inicial
mapa = [
    [0, 0, 0, 1, 0],
    [0, 2, 0, 0, 3],
    [3, 0, 0, 0, 0],
    [0, 0, 3, 0, 0],
    [0, 0, 0, 2, 0]
]

# Coordenadas de inicio y fin
inicio = (0, 0)
fin = (4, 4)

# Definimos los códigos ANSI para cada tipo de celda y damos un valor a cada tipo de terreno
colores = {
    0: '\033[97m.',     # Carretera (Blanco)
    1: '\033[91mE',     # Edificio (Rojo)
    2: '\033[94mA',     # Agua (Azul)
    3: '\033[93mB',     # Área bloqueada (Amarillo)
    'ruta': '\033[92m*',  # Ruta más corta (Verde)
}

def agregar_obstaculo(mapa):
    while True:
        try:
            fila = int(input("Ingrese la fila del obstáculo: "))
            columna = int(input("Ingrese la columna del obstáculo: "))
            if mapa[fila][columna] == 0:
                mapa[fila][columna] = 1
                print(f"Obstáculo añadido en ({fila}, {columna})")
                break
            else:
                print("Ya existe un obstáculo en esa posición. Intente de nuevo.")
        except (ValueError, IndexError):
            print("Coordenadas inválidas. Intente de nuevo.")

def solicitar_coordenadas(mensaje, mapa):
    while True:
        try:
            fila = int(input(f"Ingrese la fila del {mensaje}: "))
            columna = int(input(f"Ingrese la columna del {mensaje}: "))
            if mapa[fila][columna] == 0:
                return (fila, columna)
            else:
                print(f"La posición ({fila}, {columna}) es un obstáculo. Intente de nuevo.")
        except (ValueError, IndexError):
            print("Coordenadas inválidas. Intente de nuevo.")

def visualizar_mapa(mapa, camino=None):
    filas = len(mapa)
    columnas = len(mapa[0])
    
    # Imprimir las coordenadas de la columna
    print("    " + " ".join(f"{i}" for i in range(columnas))) #Imprime una línea que muestra las coordenadas de las columnas del mapa
    
    # Imprimir el borde superior del tablero
    print("  " + "--" * columnas)

    #verifica si la celda actual (fila, columna) pertenece al camino más corto encontrado o no.

    for fila in range(filas):
        visualizacion = f"{fila} | "
        for columna in range(columnas):
            if camino and (fila, columna) in camino:
                visualizacion += colores['ruta']  # Aquí se utiliza 'ruta' para la ruta más corta
            else:
                visualizacion += colores[mapa[fila][columna]]
            visualizacion += " "
        print(visualizacion + '|')
    
    # Imprimir el borde inferior del tablero
    print("  " + "--" * columnas)
    print('\033[0m')  # Restablecer el color al valor predeterminado

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(mapa, inicio, fin):
    filas = len(mapa)
    columnas = len(mapa[0])
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    
    # Cola de prioridad para A*
    cola = [] #Se inicializa una lista vacía que se utilizará como cola de prioridad.
    heapq.heappush(cola, (0, inicio)) # agregan un elemento con un costo inicial de 0 desde el nodo inicio.
    
    # Diccionarios para almacenar los costos y las rutas

    costos = {inicio: 0} #nodo inicial desde el cual comenzamos la búsqueda. Se asigna un costo inicial de 0
    rutas = {inicio: None}
    
    while cola:
        prioridad, actual = heapq.heappop(cola) #eliminamos el elemento con la prioridad mas baja
        
        if actual == fin: #Después de extraer un nodo de la cola, verifica si este nodo actual es igual al nodo objetivo
            break

                             # Calcula las coordenadas del vecino nx, ny sumando las coordenadas del nodo actual con las del movimiento actual

        for movimiento in movimientos:
            nx, ny = actual[0] + movimiento[0], actual[1] + movimiento[1] 

          #verificamos si las coordenadas nx ny están dentro de los límites del mapa 
            if 0 <= nx < filas and 0 <= ny < columnas and mapa[nx][ny] != 1:
                nuevo_costo = costos[actual] + 1 #Se calcula el nuevo costo acumulado para llegar al vecino, Supone que el costo de cada movimiento es 1
                vecino = (nx, ny) 
            #si el vecino no está en el diccionario costos,significa que es la primera vez que se está explorando este nodo.   
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo  #Se actualiza el costo acumulado
                    prioridad = nuevo_costo + heuristica(fin, vecino)
                    heapq.heappush(cola, (prioridad, vecino))
                    rutas[vecino] = actual #Se actualiza el diccionario rutas para almacenar que la ruta conocida de vecino es del actual
    
    # Reconstruir el camino 
    camino = []
    if fin in rutas:
        actual = fin
        while actual:
            camino.append(actual) # se anade el nodo actual a la lista camino
            actual = rutas[actual]
        camino.reverse()
    
    return camino

def main():
    global colores
    
    print("\nMapa inicial:")
    visualizar_mapa(mapa)
    
    # Preguntar si el usuario quiere agregar obstáculos
    respuesta = input("¿Desea agregar obstáculos? (s/n): ").lower()
    if respuesta == 's':
        num_obstaculos = int(input("¿Cuántos obstáculos desea agregar? "))
        for _ in range(num_obstaculos):
            agregar_obstaculo(mapa)
    
    # Solicitar nuevas coordenadas de inicio y fin
    inicio = solicitar_coordenadas("inicio", mapa)
    fin = solicitar_coordenadas("fin", mapa)
    
    # Encontrar camino más corto
    camino = a_estrella(mapa, inicio, fin)
    
    # Mostrar resultado
    print("\nMapa con la ruta más corta encontrada:")
    visualizar_mapa(mapa, camino)

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
