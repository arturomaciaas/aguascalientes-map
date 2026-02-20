from graph import Grafo

def main():
    print("--------------------------------------------------")
    print("Buscador de Ruta Más Corta en Aguascalientes")
    print("--------------------------------------------------")
    
    # Inicializar el grafo
    grafo = Grafo()
    print("Cargando datos del mapa...")
    grafo.cargar_datos('data.xlsx')

    # Mostrar algunos ejemplos de nodos
    print("\nEjemplos de nodos:")
    contador = 0
    for id_nodo, nodo in grafo.nodos.items():
        print(f"ID: {id_nodo:<5} Nombre: {nodo.name_loc}")
        contador += 1
        if contador >= 5:
            break
    
    while True:
        print("\nIngrese IDs de nodos para buscar la ruta (o 'salir' para terminar):")
        entrada_inicio = input("ID Nodo Inicio: ")
        if entrada_inicio.lower() == 'salir':
            break
            
        entrada_fin = input("ID Nodo Fin: ")
        if entrada_fin.lower() == 'salir':
            break
            
        try:
            inicio_id = int(entrada_inicio)
            fin_id = int(entrada_fin)
            
            # Verificar si los nodos existen
            if inicio_id not in grafo.nodos:
                print(f"Error: Nodo de inicio {inicio_id} no encontrado.")
                continue
            if fin_id not in grafo.nodos:
                print(f"Error: Nodo de fin {fin_id} no encontrado.")
                continue
                
            # Calcular ruta
            ruta, distancia = grafo.obtener_ruta_mas_corta(inicio_id, fin_id)
            
            if ruta:
                print("\n¡Ruta más corta encontrada!")
                print(f"Distancia Total: {distancia:.2f} km")
                print("Secuencia del camino:")
                for i, id_nodo in enumerate(ruta):
                    nombre_nodo = grafo.nodos[id_nodo].name_loc
                    print(f"{i+1}. [{id_nodo}] {nombre_nodo}")
            else:
                print("\nNo se encontró un camino entre estos nodos.")
                
        except ValueError:
            print("Entrada inválida. Por favor ingrese números para los IDs.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
