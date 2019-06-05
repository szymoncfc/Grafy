import sys
import matplotlib.pyplot as plt
import random
import time


class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.Matrix = [[0 for column in range(vertices)]for row in range(vertices)]
        self.licznik = 0

    def add_edge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        if self.Matrix[v1][v2] == 0 and self.Matrix[v2][v1] == 0:
            weight = random.randint(0, 100)
            self.Matrix[v1][v2] = weight
            self.Matrix[v2][v1] = weight
            self.licznik += 1
#           print("Dodano krawedź ", self.licznik, "(", v1, ",", v2, ")")
#        else:
#           print("Taka krawedz już istnieje (", v1, ",", v2, ")")

    def remove_edge(self, v1, v2):
        if self.Matrix[v1][v2] == 0:
            print("Nie ma krawedzi pomiedzy %d i %d" % (v1, v2))
            return
        self.Matrix[v1][v2] = 0
        self.Matrix[v2][v1] = 0

    def print_solution(self, dist):
        print('Dystans z wierzchołka źrodłowego')
        for node in range(self.V):
            if dist[node] == sys.maxsize:
                print("Dystans do wierzchołka", node, "wynosi ->", "Brak połączenia do tego wierzchołka")
            else:
                print("Dystans do wierzchołka", node, "wynosi ->", dist[node])

    def min_distance(self, dist, sptset):

        global min_index
        min = sys.maxsize

        for v in range(self.V):
            if dist[v] < min and sptset[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def print_graph(self):
        print("Graf w postaci macierzy: ")
        for i in range(len(self.Matrix)):
            for j in range(len(self.Matrix)):
                print(self.Matrix[i][j], ' ', end='')
            print()

    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptset = [False] * self.V

        for cout in range(self.V):

            u = self.min_distance(dist, sptset)

            sptset[u] = True

            for v in range(self.V):
                if self.Matrix[u][v] > 0 and sptset[v] == False and dist[v] > dist[u] + self.Matrix[u][v]:
                    dist[v] = dist[u] + self.Matrix[u][v]

        self.print_solution(dist)

    def build_graph(self, edges1):
        tab_x = []
        tab_y = []
        tab_z = []
        for i in range(int(self.V)):
            tab_x.append(i)
            tab_z.append(i)
        for i in range(int(self.V) - 1, -1, -1):
            tab_y.append(i)
        i = 0
        z = 0
        x = 0
        while x < edges1:
            if i < int(self.V):
                a = tab_x[z]
                b = tab_y[i]
                if a != b:
                    self.add_edge(a, b)
                    x = self.licznik
#                    print(i, " - > iteracja")
                    i += 1
                else:
#                    print(i, " - > iteracja")
#                    print("Ten sam wierzchołek -> (", a, ",", b, ")")
                    i += 1
            else:
                z += 1
                i = 0
#                print("Koniec zakresu")
        else:
            print("Dodano wszystkie krawedzie")


# vertex_quantity = input("Podaj ilość wierzchołków: ")
# density = input("Podaj gęstość w procentach: ")

vertex_quantity = [10, 50, 100, 500, 1000]
density = [25, 50, 75, 100]
for i in range(len(vertex_quantity)):
    edges = (int(vertex_quantity[i])*(int(vertex_quantity[i])-1)*(float(density[3])/100))/2
    print('Ilość krawedzi: ', int(edges))
    g = Graph(int(vertex_quantity[i]))
    g.build_graph(int(edges))
#    g.print_graph()
    source_vertex = input("Podaj wierzchołek od którego chcesz wartości najtańszych ścieżek: ")
    start = time.time()
    g.dijkstra(int(source_vertex))
    end = time.time()
    graph_time = (end - start)
    print("Czas wykonania:", graph_time)
    plt.scatter(vertex_quantity[i], graph_time, color='b')
plt.ylabel('Czas działania [s]')
plt.xlabel('Ilość wierzchołków')
plt.title('Czasy dla gestosci 100% graf pełny - macierz sąsiedztwa')
plt.grid()
plt.show()