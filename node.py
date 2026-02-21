class Node:
    """Clase que representa un punto (nodo) en el mapa"""
    def __init__(self, id, cvegeo, name_loc, lat, lon, neighbors):
        self.id = id
        self.cvegeo = cvegeo
        self.name_loc = name_loc
        self.lat = lat
        self.lon = lon
        self.neighbors = neighbors
