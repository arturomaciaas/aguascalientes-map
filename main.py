from graph import Grafo

print("--- Hubber Maps para Aguascalientes --- (modo kawai)")
grafo = Grafo()
grafo.cargar_datos("data.xlsx")

while True:
    try:
        entrada_inicio = input("ID del nodo inicio: ")
        entrada_fin = input("ID del nodo fin: ")

        id_inicio = int(entrada_inicio)
        id_fin = int(entrada_fin)
        break
    except ValueError:
        print("Pon números válidos para los ids, hubber!!!")
        continue

print(f"Buscando camino de {id_inicio} a {id_fin}")
ruta, distancia = grafo.buscar_ruta(id_inicio, id_fin)

if ruta:
    print(f"\nCamino encontrado! Distancia total: {distancia:.2f} km")
    print("Ruta a seguir:")
    for paso, id_nodo in enumerate(ruta):
        nombre = grafo.nodos[id_nodo].name_loc
        print(f"{paso + 1}. [{id_nodo}] {nombre}")
else:
    print("No se encontró un camino entre estos puntos.")
