import pandas as pd
import ast
import math
import heapq

class Node:
    def __init__(self, id, cvegeo, name_loc, lat, lon, neighbors):
        self.id = id
        self.cvegeo = cvegeo
        self.name_loc = name_loc
        self.lat = lat
        self.lon = lon
        self.neighbors = neighbors
        
class Grafo:
    def __init__(self):
        # Almacena los nodos por ID
        self.nodos = {}

    def cargar_datos(self, archivo):
        """Carga los nodos desde un archivo Excel."""
        try:
            df = pd.read_excel(archivo)
            for _, fila in df.iterrows():
                # Convertir string de lista a lista real
                try:
                    vecinos = ast.literal_eval(str(fila['VECINOS']))
                except (ValueError, SyntaxError):
                    vecinos = []
                
                nodo = Node(
                    id=fila['ID'],
                    cvegeo=fila['CVEGEO'],
                    name_loc=fila['NOM_LOC'],
                    lat=fila['LAT_DECIMAL'],
                    lon=fila['LON_DECIMAL'],
                    neighbors=vecinos
                )
                self.nodos[nodo.id] = nodo
            print(f"Cargados {len(self.nodos)} nodos exitosamente.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def calcular_distancia(self, nodo1, nodo2):
        """Calcula la distancia Haversine entre dos nodos (km)."""
        radio_tierra = 6371  # km
        
        d_lat = math.radians(nodo2.lat - nodo1.lat)
        d_lon = math.radians(nodo2.lon - nodo1.lon)
        
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(nodo1.lat)) * 
             math.cos(math.radians(nodo2.lat)) * 
             math.sin(d_lon / 2) ** 2)
             
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radio_tierra * c

    def obtener_ruta_mas_corta(self, inicio_id, fin_id):
        """Busca la ruta más corta usando el algoritmo A*."""
        if inicio_id not in self.nodos or fin_id not in self.nodos:
            return None, float('inf')

        # Cola de prioridad para nodos a visitar: (costo_estimado_total, nodo_id)
        cola_prioridad = [(0, inicio_id)]
        
        # Para reconstruir el camino: de dónde venimos
        vino_de = {}
        
        # Costo real desde el inicio hasta el nodo actual
        costo_g = {id: float('inf') for id in self.nodos}
        costo_g[inicio_id] = 0
        
        # Costo total estimado (g + heurística)
        costo_f = {id: float('inf') for id in self.nodos}
        costo_f[inicio_id] = self.calcular_distancia(self.nodos[inicio_id], self.nodos[fin_id])
        
        visitados = set()

        while cola_prioridad:
            _, actual_id = heapq.heappop(cola_prioridad)
            
            if actual_id == fin_id:
                return self._reconstruir_camino(vino_de, actual_id), costo_g[fin_id]
            
            if actual_id in visitados:
                continue
            visitados.add(actual_id)
            
            nodo_actual = self.nodos[actual_id]
            
            for vecino_id in nodo_actual.neighbors:
                if vecino_id not in self.nodos:
                    continue
                    
                nodo_vecino = self.nodos[vecino_id]
                distancia = self.calcular_distancia(nodo_actual, nodo_vecino)
                nuevo_costo_g = costo_g[actual_id] + distancia
                
                if nuevo_costo_g < costo_g[vecino_id]:
                    vino_de[vecino_id] = actual_id
                    costo_g[vecino_id] = nuevo_costo_g
                    heuristica = self.calcular_distancia(nodo_vecino, self.nodos[fin_id])
                    costo_f[vecino_id] = nuevo_costo_g + heuristica
                    heapq.heappush(cola_prioridad, (costo_f[vecino_id], vecino_id))
                    
        return None, float('inf')

    def _reconstruir_camino(self, vino_de, actual_id):
        """Reconstruye el camino desde el final hasta el inicio."""
        camino = [actual_id]
        while actual_id in vino_de:
            actual_id = vino_de[actual_id]
            camino.append(actual_id)
        return camino[::-1] # Invierte la lista para tener inicio -> fin
