from queue import *


class Vertex:

    # Modification of the Vertex class may involve adding another argument to the constructor.
    # That argument will be to add an object of the location type to the vertex object
    # The 'label' will be the 'location.id_' and the location will be the 'location' object
    def __init__(self, label, location):
        self.label = label
        self.location = location
        self.distance = float('inf')
        self.pred_vertex = None

    def __str__(self):
        return f'{self.label}'
      
    def __hash__(self):
        return hash(self.label)
    
    def __eq__(self, other):
        return self.label == other
    

class Graph:
  
  # O(1)
    def __init__(self):
        self.vertex_list = []
        self.adjacency_list = {}
        self.edge_weights = {}

    # O(1)
    def __str__(self):
        return f'{self.adjacency_list}, {self.edge_weights}'

    # O(n)
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # O(1)
    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    # O(1)
    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # O(n)
    def breadth_first_search(self, graph, start_vertex):
        discovered_set = []
        frontier_queue = Queue()

        frontier_queue.push(start_vertex)
        discovered_set.append(start_vertex)

        while frontier_queue.list.head is None:
            current_vertex = frontier_queue.pop()
            for adjacent_vertex in graph.adjacency_list[current_vertex]:
                if discovered_set.count(adjacent_vertex == 0):
                    frontier_queue.push(adjacent_vertex)
                    discovered_set.append(adjacent_vertex)
                    adjacent_vertex.distance = current_vertex.distance + 1
        return discovered_set
      
#     def  dijkstra_shortest_path(g, start_vertex):
#         #Put all vertices in an unvisited queue
#         unvisited_queue = []
#         for current_vertex in g.adjacency_list:
#             unvisited_queue.append(current_vertex)
            
#         #start_vertex has a distance of 0 from itself
#         start_vertex.distance = 0
        
#         #One vertex is removed with each iteration; repeat until the list is empty
#         while len(unvisited_queue) > 0:
#             # Visit vertex with minimum distance from start_vertex
#             smallest_index = 0
#             for i in range(1, len(unvisited_queue)):
#                 if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
#                     smallest_index = i
#             current_vertex = unvisited_queue.pop(smallest_index)
            
#             #Check potential path lengths from the current vertex to all neighbors
#             for adj_vertex in g.adjacency_list[current_vertex]:
#                 edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
#                 alternative_path_distance = current_vertex.distance + edge_weight
#                 # If shroter path from start_vertex to adj_vertex is found, update adj_vertex distance and predecessor
#                 if alternative_path_distance < adj_vertex.distance:
#                     adj_vertex.distance = alternative_path_distance
#                     adj_vertex.pred_vertex = current_vertex
        
        