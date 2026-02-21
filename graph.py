import pandas as pd
import ast
import math
import heapq
from node import Node

class Grafo:
    def __init__(self):
        self.nodos = {}

    def cargar_datos(self, archivo):
        print(f"Leyendo archivo: {archivo}")
        df = pd.read_excel(archivo)
        
        for index, fila in df.iterrows():
            # Convertimos el texto de vecinos a una lista real
            texto_vecinos = str(fila['VECINOS'])
            # ast.literal_eval convierte "[1, 2, 3]" en una lista [1, 2, 3]
            lista_vecinos = ast.literal_eval(texto_vecinos)
            
            nuevo_nodo = Node(
                id=fila['ID'],
                cvegeo=fila['CVEGEO'],
                name_loc=fila['NOM_LOC'],
                lat=fila['LAT_DECIMAL'],
                lon=fila['LON_DECIMAL'],
                neighbors=lista_vecinos
            )
            self.nodos[nuevo_nodo.id] = nuevo_nodo
        
        print(f"Listo! Se cargaron {len(self.nodos)} nodos")

    def calcular_distancia(self, nodo_a, nodo_b):
        """Calcula km entre dos nodos con Haversine"""
        radio_tierra = 6371  # Radio de la Tierra en km
        
        # Convertimos grados a radianes
        d_lat = math.radians(nodo_b.lat - nodo_a.lat)
        d_lon = math.radians(nodo_b.lon - nodo_a.lon)
        
        # Fórmula matemática para distancia en una esfera
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(nodo_a.lat)) * 
             math.cos(math.radians(nodo_b.lat)) * 
             math.sin(d_lon / 2) ** 2)
             
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = radio_tierra * c
        
        return distancia

    def buscar_ruta(self, inicio_id, fin_id):
        """Encuentra el camino más corto usando el algoritmo A*"""
        # Paso 1: Verificar que los nodos existan
        if inicio_id not in self.nodos or fin_id not in self.nodos:
            print("Error: Uno de los nodos no existe.")
            return None, 0

        # Paso 2: Preparar las estructuras de datos
        nodo_meta = self.nodos[fin_id]
        
        cola = [] # Cola de prioridad: guarda nodos por visitar
        # Se ordenan automáticamente por el costo estimado (primero el menor)
        heapq.heappush(cola, (0, inicio_id))
        
        vino_de = {}
        costo_g = {}      # Costo real desde el inicio hasta aquí
        
        costo_g[inicio_id] = 0
        
        # Paso 3: Bucle principal de búsqueda
        while len(cola) > 0:
            # Sacamos el nodo con menor costo estimado
            costo_estimado, actual_id = heapq.heappop(cola)
            
            # Si llegamos al destino, terminamos y devolvemos el camino
            if actual_id == fin_id:
                return self.reconstruir_camino(vino_de, actual_id), costo_g[fin_id]
            
            nodo_actual = self.nodos[actual_id]
            
            # Revisamos todos los vecinos de este nodo
            for vecino_id in nodo_actual.neighbors:
                if vecino_id not in self.nodos:
                    continue
                
                nodo_vecino = self.nodos[vecino_id]
                
                # Calculamos el costo para llegar a este vecino
                distancia_tramo = self.calcular_distancia(nodo_actual, nodo_vecino)
                nuevo_costo = costo_g[actual_id] + distancia_tramo
                
                # Si encontramos un camino mejor (o es la primera vez que lo vemos)
                if vecino_id not in costo_g or nuevo_costo < costo_g[vecino_id]:
                    costo_g[vecino_id] = nuevo_costo
                    vino_de[vecino_id] = actual_id
                    
                    # Prioridad = Costo real + Distancia estimada a la meta (Heurística)
                    prioridad = nuevo_costo + self.calcular_distancia(nodo_vecino, nodo_meta)
                    heapq.heappush(cola, (prioridad, vecino_id))
                    
        return None, 0

    def reconstruir_camino(self, vino_de, actual_id):
        """Construye la lista final de nodos siguiendo las pistas hacia atrás"""
        camino = [actual_id]
        while actual_id in vino_de:
            actual_id = vino_de[actual_id]
            camino.append(actual_id)
        # Se invierte la lista para tener el orden correcto: Inicio -> Fin
        return camino[::-1]
