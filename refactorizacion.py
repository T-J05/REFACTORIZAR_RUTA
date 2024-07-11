import networkx as nx
import random as rd
import math

class Cuadricula:
    def __init__(self):
        self.tamanho = 10
        self.grafo = nx.grid_2d_graph(self.tamanho, self.tamanho)
        self.obst = set()  # conjunto que guardara los obstáculos
        self.inicio = None
        self.fin = None
        self.tablero = None

    def obtener_parametros(self):
        return self.tamanho, self.grafo, self.obst, self.inicio, self.fin, self.tablero

    def crear_tablero(self):
        self.tablero = [['.' for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        for fila in self.tablero:
            print(' '.join(fila))

    def anhadir_obstaculos(self,aleatorio, pregunta):
        while aleatorio > 40:
            print("Exceso de obstáculos")
            aleatorio = int(input('Ingrese un valor válido: '))

        if aleatorio > 0:
            for _ in range(aleatorio):
                of = rd.randint(0, 9)
                oc = rd.randint(0, 9)
                self.obst.add((of, oc))

        while pregunta.lower() == 'si':
            ox = int(input('Ingrese la coordenada x del obstáculo: '))
            oy = int(input('Ingrese la coordenada y del obstáculo: '))
            while ox < 0 or oy < 0 or ox >= 10 or oy >= 10:
                print('Coordenadas fuera de los límites')
                ox = int(input('Ingrese la coordenada x del obstáculo: '))
                oy = int(input('Ingrese la coordenada y del obstáculo: '))

            self.obst.add((ox, oy))
            pregunta = input('Si desea agregar más obstáculos, escriba "si"; de lo contrario, escriba "no": ')

        # Actualizar el tablero con los obstáculos agregados
        print("Tablero con obstáculos:")
        self.actualizar_tablero()

    def actualizar_tablero(self):
        for fila in range(self.tamanho):
            for columna in range(self.tamanho):
                if (fila, columna) in self.obst:
                    self.tablero[fila][columna] = 'o'
                else:
                    self.tablero[fila][columna] = '.'

        for fila in self.tablero:
            print(" ".join(fila))

    def eliminar_obstaculos(self, ex, ey, eliminar):
        while eliminar.lower() == "si":
            if ex < 0 or ey < 0 or ex >= 10 or ey >= 10:
                print('Coordenadas fuera de los límites')
                ex = int(input('Ingrese las coordenadas x del obstáculo a eliminar: '))
                ey = int(input('Ingrese las coordenadas y del obstáculo a eliminar: '))

            obbeliminar = (ex, ey)
            if obbeliminar not in self.obst:
                print('Ingrese un obstáculo que exista')
                ex = int(input('Ingrese las coordenadas x del obstáculo a eliminar: '))
                ey = int(input('Ingrese las coordenadas y del obstáculo a eliminar: '))
            else:
                self.obst.remove(obbeliminar)
                self.actualizar_tablero()
                eliminar = input('¿Desea eliminar otro obstáculo? (si/no): ')

    def anhadir_inicio_fin(self, inicio, fin):
        self.fin = fin
        self.inicio = inicio
        ix, iy = inicio
        fx, fy = fin

        while ix < 0 or iy < 0 or ix >= 10 or iy >= 10:
            print('Inicio fuera de rango')
            ix = int(input("Ingrese la coordenada x: "))
            iy = int(input("Ingrese la coordenada y: "))
            self.inicio = (ix, iy)

        while fx < 0 or fy < 0 or fx >= 10 or fy >= 10:
            print('Fin fuera del rango')
            fx = int(input("Ingrese la coordenada x: "))
            fy = int(input("Ingrese la coordenada y: "))
            self.fin = (fx, fy)

        while self.fin in self.obst:
            print("ERROR: tu fin está en un obstáculo")
            print("Ingrese las coordenadas x e y de tu punto de destino")
            finr = input('Ingrese las coordenadas de fin en este formato (x,y): ')
            finn = tuple(map(int, finr.strip().split(',')))
            # fx, fy = fin
            self.fin = finn
            if self.fin not in self.obst:
                break 

        while self.inicio in self.obst:
            print("ERROR: tu inicio está en un obstáculo")
            print("Ingrese las coordenadas x e y de tu punto de inicio")
            inicior = input('Ingrese las coordenadas de inicio en este formato (x,y): ')
            inicioo = tuple(map(int, inicior.strip().split(',')))
            
            self.inicio = (inicioo)
            if self.inicio not in self.obst:
                break 

        self.grafo.add_nodes_from(self.grafo.nodes)  # Agregar todos los nodos del tablero como nodos en el grafo

        self.tablero[ix][iy] = 'I'
        self.tablero[fx][fy] = 'F'

        for fila in self.tablero:
            print(' '.join(fila))


class EncontrarRuta:
    def __init__(self, tamanho, grafo, obst, inicio, fin, tablero):
        self.tamanho = tamanho
        self.grafo = grafo
        self.obst = obst
        self.inicio = inicio
        self.fin = fin
        self.tablero = tablero
        self.ruta = None

    @staticmethod
    def heuristica(x, y):  # heurística con distancia Manhattan
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def asignar_peso(self):
        for u, v in self.grafo.edges():
            if u in self.obst or v in self.obst:
                self.grafo.edges[u, v]['peso'] = math.inf
            else:
                self.grafo.edges[u, v]['peso'] = 1

    def aestar(self):
        self.asignar_peso()  # asignar pesos

        try:
            self.ruta = nx.astar_path(self.grafo, self.inicio, self.fin, heuristic=self.heuristica, weight='peso')
            return self.ruta
        except nx.NetworkXNoPath:
            print("No hay camino disponible")
            return None

    def mostrar_ruta(self, VER):
        if VER.lower() == 'ver':
            if self.ruta:
                for nodo in self.ruta:  # imprimir la ruta
                    if nodo in self.obst:
                        print('NO HAY CAMINO')
                        break
                    self.tablero[nodo[0]][nodo[1]] = 'x'
                    self.tablero[self.inicio[0]][self.inicio[1]] = 'I'
                    self.tablero[self.fin[0]][self.fin[1]] = 'F'
                self.actualizar_tablero()
            else:
                print('No hay ruta para mostrar.')
        else:
            print('No hay ruta para mostrar.')

    def actualizar_tablero(self):
        for fila in self.tablero:
            print(' '.join(fila))


# LLAMAR A LAS CLASES Y FUNCIONES DEL INTERFAZ DEL USUARIO
cuadricula = Cuadricula()
cuadricula.crear_tablero()
alea = int(input('Ingrese la cantidad de obstáculos aprox aleatorios que quiera (max 39): '))

preg = input('Si desea agregar más obstáculos, escriba "si"; de lo contrario, escriba "no": ')
if preg == 'si':
    cuadricula.anhadir_obstaculos(alea, preg)

elim = input('Si desea eliminar obstáculos, escriba "si"; de lo contrario, escriba "no": ')
if elim.lower() == 'si':
    print(f'\nCoordenadas de los obstáculos ahora existentes: {cuadricula.obst}')
    exx = int(input('Ingrese las coordenadas x del obstáculo a eliminar: '))
    eyy = int(input('Ingrese las coordenadas y del obstáculo a eliminar: '))
    cuadricula.eliminar_obstaculos(exx, eyy, elim)

inicior = input('Ingrese las coordenadas de inicio en este formato (x,y): ')
inicioo = tuple(map(int, inicior.strip().split(',')))
finr = input('Ingrese las coordenadas de fin en este formato (x,y): ')
finn = tuple(map(int, finr.strip().split(',')))
cuadricula.anhadir_inicio_fin(inicioo, finn)

# LLAMAR A LA CLASE QUE ENCUENTRA EL CAMINO
parametros = cuadricula.obtener_parametros()
encontrar_ruta = EncontrarRuta(*parametros)
ver = input('Para ver la ruta escriba "ver": ')
encontrar_ruta.aestar()
encontrar_ruta.mostrar_ruta(ver)