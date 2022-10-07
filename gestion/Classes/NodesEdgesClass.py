import networkx as nx
import matplotlib.pyplot as plt
import random

current_file = "save.txt"
nbr_hours_max = 32

class _MatrixMaster:

    def __init__(self):
        self.color_list = self.create_color_list()

    def _write_in_a_file(self, file_name, matrix):
        # save the matrix into a .txt file
        file = open(file_name, "w")
        for row in matrix:
            text = str(row) + "\n"
            file.write(text)
        file.close()

    def printMyMatrix(self, matrix):
        for row in matrix:
            print(row)

        print("Fin de l'affichage de la matrice.")
        print("")
        return 0

    def createDefinedRelationMatrix(self, nbr_classes):
        matrix = []
        for i in range(nbr_classes):
            current_line = []
            for j in range(nbr_classes):
                if j < i:
                    value = 0
                elif j == i:
                    value = None
                else:
                    # value = 1
                    value = random.randint(0, 1)
                current_line.append(value)

            matrix.append(current_line)
        self._write_in_a_file(current_file, matrix)
        self.printMyMatrix(matrix)
        return matrix

    def createRelationList(self, matrix):
        relation_list = []
        for i in range(len(matrix)):
            for j, value in enumerate(matrix[i]):
                if value == 1:
                    current_tuple = (i, j)
                    relation_list.append(current_tuple)
        self.printMyMatrix(relation_list)
        return relation_list

    def create_Node_List(self, nbr_nodes):
        this_list = []
        for i in range(nbr_nodes):
            this_list.append(i)
        return this_list

    def create_color_list(self):
        import colorsys
        N = nbr_hours_max  # Puiqu'il n'y a que 32heures de cours au max dans une semaine
        HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
        RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
        color_list = ['b', 'r', 'g', 'c', 'm', 'y', 'tab:blue', 'tab:orange', 'tab:green', 'tab:purple', 'tab:olive',
                      'tab:brown']
        return RGB_tuples

class _G_Manager(_MatrixMaster):
    def __init__(self, nbr_classes):
        super(_G_Manager, self).__init__()
        self.matrix = self.createDefinedRelationMatrix(nbr_classes)
        self.nodes = self.create_Node_List(nbr_classes)
        self.edges = self.createRelationList(self.matrix)

        self.G = nx.Graph()  # nx.DiGraph() for directed graph
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)  # from file?
        print("Number of nodes =", self.G.number_of_nodes())
        print("Number of edges =", self.G.number_of_edges())

    def print_G_elements(self):
        print("G.nodes =", self.G.nodes)
        print("G.edges =", self.G.edges)
        print("G.degree =", self.G.degree)  # Most Important element
        print("G.adj =", self.G.adj)  # REALLY IMPORTANT TO DETERMINATE WHO ARE ADJACENT
        print("")

    def add_attributes_to_nodes(self, G):
        for i in G.nodes:  # #1 most widely used graph operation
            G.nodes[i]['smoking'] = False
            G.nodes[i]['weight'] = random.choice(range(10, 200))
            # G.nodes[i]['weight'] = 100

        G.nodes[1]['smoking'] = True
        print("G.nodes.data():", G.nodes.data())

    def add_attributes_to_edges(self, G):
        for edge in G.edges:  # also widely used operation
            G.edges[edge]['strength'] = round(random.random(), 2)
        print("G.edges.data():", G.edges.data())
        print("G.adj:", G.adj)

    def sort_according_to_degrees(self):
        liste_node = self.getNodesList()
        liste_degree = self.getDegreeOnlyList()
        print("liste_node :", liste_node)
        print("liste_degree :", liste_degree)

        sorted_list = [x for _, x in sorted(zip(liste_degree, liste_node), reverse=True)]
        print("sorted_list :", sorted_list)
        print("")
        return sorted_list

    def example(self, G):
        for nbr in G.neighbors(2):
            print(nbr)

    def getGraph(self):
        return self.G

    def getNodesList(self):
        #   Attention, cette fonction renvoie une liste de node et non pas un type(G.nodes)
        return list(self.nodes)

    def getDegreeList(self):
        return self.G.degree

    def getDegreeOnlyList(self):
        # RAPPEL graph.degree est une liste de tuple! Nous, pour faire le zip, on a besoin de n'avoir QU'UNE liste de degree
        degree_only_list = []
        for elem in self.G.degree:
            degree_only_list.append(elem[1])

        return degree_only_list

    def getMatrix(self):
        return self.matrix

class MapManager(_G_Manager):

    def __init__(self, nbr_classes):
        super(MapManager, self).__init__(nbr_classes)

        self.color_map = [None] * len(self.G.nodes)
        self.size_map = [None] * len(self.G.nodes)

    def _nobody_got_current_color(self, color, color_map, current_node):
        res = 1
        for neighbour in self.G.adj[current_node]:
            index = list(self.G.nodes).index(neighbour)
            if color_map[index] == color:
                res = 0
        return res

    def try_to_color_nodes(self, graph, color_map, sorted_list, color):
        for node in sorted_list:
            node_index = list(graph.nodes).index(node)
            if color_map[node_index] == None:  # RIEN NE SERT DE CHECK SI LE NODE A DEJA UNE COULEUR
                if self._nobody_got_current_color(color, color_map, node):
                    #   print("LE NOEUD EN QUESTION EST:", node, "ET SON INDICE VAUT", node_index)
                    color_map[node_index] = color

    def check_color(self, graph, color_map, color_list):
        #   print("A LA BASE, color_map:", color_map)
        i = 0
        sorted_list = self.sort_according_to_degrees()
        while None in self.color_map:
            color = color_list[i]
            print("LA COULEUR EN COURS :", color)
            self.try_to_color_nodes(graph, color_map, sorted_list, color)
            print("L'evolution de color_map :", color_map)
            i += 1

    def draw_with_colors(self, G, color_map, size_map):
        color_list = self.color_list

        for index, node in enumerate(G.nodes):
            #   print("LA VALUE DE INDEX:", index, "VS LA VALUE DE LEN(size_map):", len(size_map))
            size_map[index] = G.nodes[node]['weight'] * 10

        self.check_color(G, color_map, color_list)

        print("")
        print("LA COLOR_MAP :", color_map)
        print("LA SIZE_MAP :", size_map)
        nx.draw_networkx(G, node_color=color_map, node_size=size_map, pos=nx.spring_layout(G, iterations=1000),
                         arrows=False, with_labels=True)
        # self.check_color_map()

    def get_node_color(self, node):
        index_node = list(self.nodes).index(node)
        color = self.color_map[index_node]

        return color

    def check_color_map(self):
        # Permet de vérifier si la fonction get_node_color fonctionne bien en comparant à self.color_map
        this_color_map = []
        for node in self.nodes:
            this_color_map.append(self.get_node_color(node))

    def setup(self):
        # Views
        self.print_G_elements()

        # Add attributes to nodes
        self.add_attributes_to_nodes(self.G)
        # Add attributes to edges
        self.add_attributes_to_edges(self.G)
        # Color nodes and visualize network
        plt.figure("Full Colors")
        #   nx.draw_networkx(G)  # Simple 1-line code

        # A way to complete the graph with colors
        self.draw_with_colors(self.G, self.color_map, self.size_map)

        plt.show()
    def create_table_hours(self):
        jours = ["lundi: ","mardi: ","mercredi: ","jeudi: ","vendredi: "]
        table = []
        for jour in jours:
            if jour == "mercredi: ":
                for hour in range(8,12):
                    text = jour + str(hour)
                    table.append(text)
            else:
                for hour in range(8,16):
                    if hour != 12:
                        #   Ce n'est pas l'heure de midi
                        text = jour + str(hour)
                        table.append(text)
        return table

    def convert_color_hours(self):
        list_tuple = []
        table = self.create_table_hours()
        for node in self.nodes:
            color_node = self.get_node_color(node)
            if color_node is not None:
                color_index = self.color_list.index(color_node)

                hour = table[color_index]
                relation = (node,hour)
                list_tuple.append(relation)
            else:
                print("IL Y A UNE ERREUR DANS convert_color_hours")
                quit()
        return list_tuple
