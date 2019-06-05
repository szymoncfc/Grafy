import sys
from collections import defaultdict
import random
import matplotlib.pyplot as plt
import time


class Heap:

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    @staticmethod
    def new_min_heap_node(v, dist):
        min_heap_node = [v, dist]
        return min_heap_node

    def swap_min_heap_node(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    def min_heapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right

        if smallest != idx:
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            self.swap_min_heap_node(smallest, idx)

            self.min_heapify(smallest)

    def extract_min(self):

        if self.empty():
            return

        root = self.array[0]

        last_node = self.array[self.size - 1]
        self.array[0] = last_node

        self.pos[last_node[0]] = 0
        self.pos[root[0]] = self.size - 1

        self.size -= 1
        self.min_heapify(0)

        return root

    def empty(self):
        return True if self.size == 0 else False

    def decrease_key(self, v, dist):

        i = self.pos[v]

        self.array[int(i)][1] = dist

        while i > 0 and self.array[int(i)][1] < self.array[int((i - 1) / 2)][1]:
            self.pos[self.array[int(i)][0]] = int((i - 1) / 2)
            self.pos[self.array[int((i - 1) / 2)][0]] = i
            self.swap_min_heap_node(int(i), int((i - 1) / 2))

            i = (i - 1) / 2

    def in_min_heap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


def print_arr(dist, n):
    print("Vertex\tDistance from source")
    for i in range(n):
        if dist[i] == sys.maxsize:
            print("%d\t\t" % i, "Nie ma połączenia")
        else:
            print("%d\t\t%d" % (i, dist[i]))


class Graph:

    def __init__(self, v):
        self.V = v
        self.graph = defaultdict(list)
        self.pom = defaultdict(list)
        self.licznik = 0

    def add_edge(self, src, dest):

        # dodajemy krawedzie z wierzchlka żródlowego do końcowego i odwrotnie bo graf nieskierowany
        # dodajemy na poczayek listy
        # krawedź zawiera 2 elemnenty destyanacje i wage
        # krawedź pomocnicza sluzy do sprawdzania czy krawedz juz istnieje

        weight = random.randint(0, 100)
        if [dest] in self.pom[src] and [src] in self.pom[dest]:
            # print("Taka krawedź już istnieje")
            q =1
        else:
            new_node = [src, weight]
            new_node_pom = [src]
            self.graph[dest].insert(0, new_node)
            self.pom[dest].insert(0, new_node_pom)
            new_node = [dest, weight]
            new_node_pom = [dest]
            self.graph[src].insert(0, new_node)
            self.pom[src].insert(0, new_node_pom)
            self.licznik += 1
#            print("Dodano krawedź: (", src, ",", dest, ")")
#            print(self.graph)

    def dijkstra(self, src):

        V = self.V # wczytujemy ilosc wierzcholkow
        dist = []

        min_heap = Heap()

        #  budujemy kopiec minimalny dla wierzcholkow z odleglosciami
        for v in range(V):
            dist.append(sys.maxsize)
            min_heap.array.append(min_heap.new_min_heap_node(v, dist[v]))
            min_heap.pos.append(v)


        min_heap.pos[src] = src
        dist[src] = 0
        min_heap.decrease_key(src, dist[src])

        min_heap.size = V

        while not min_heap.empty():

            new_heap_node = min_heap.extract_min()
            u = new_heap_node[0]

            for pCrawl in self.graph[u]:

                v = pCrawl[0]

                if min_heap.in_min_heap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]:
                    dist[v] = pCrawl[1] + dist[u]

                    min_heap.decrease_key(v, dist[v])

#        print_arr(dist, V)

    def build_graph(self, edges1):
        V = self.V
        tab_x = []
        tab_y = []
        tab_z = []
        for i in range(int(V)):
            tab_x.append(i)
            tab_z.append(i)
        for i in range(int(V) - 1, -1, -1):
            tab_y.append(i)
        i = 0
        z = 0
        x = 0
        while x < edges1:
            if i < int(V):
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
            #               print("Koniec zakresu")
        else:
            print("Dodano wszystkie krawedzie:", self.licznik)


# vertex_quantity = input("Podaj ilość wierzchołków: ")
# density = input("Podaj gęstość w procentach: ")

vertex_quantity = [10, 50, 100, 500, 1000]
density = [25, 50, 75, 100]

for i in range(len(vertex_quantity)):
    edges = (int(vertex_quantity[i])*(int(vertex_quantity[i])-1)*(float(density[0])/100))/2
    graph = Graph(int(vertex_quantity[i]))
    graph.build_graph(int(edges))
    source_vertex = input("Podaj wierzchołek od którego chcesz wartości najtańszych ścieżek: ")
    start = time.time()
    graph.dijkstra(int(source_vertex))
    end = time.time()
    graph_time = (end - start)
    print("Czas wykonania:", graph_time)
    plt.scatter(vertex_quantity[i], graph_time, color='b')

plt.ylabel('Czas działania [s]')
plt.xlabel('Ilość wierzchołków')
plt.title('Czasy dla gestości 25% - lista sąsiedztwa')
plt.grid()
plt.show()



