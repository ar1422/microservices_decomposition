class Edge(object):

    def __init__(self, source, destination, cost: int = 0) -> None:
        self.source = source
        self.destination = destination
        self.cost = cost

    def __str__(self):
        return "{0}: {1} - cost={2}".format(self.source.name, self.destination.name, self.cost)

    def __lt__(self, other):
        if isinstance(other, Edge):
            return self.cost < other.cost
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.source == other.source and self.destination == other.destination and self.cost == other.cost
        else:
            return False


class Node(object):
    def __init__(self, name) -> None:
        self.name = name
        self.edges = list()
        self.connections = {}

    def add_edge(self, destination, weight=1) -> None:

        if destination.name not in self.connections:
            edge = Edge(self, destination, 0)
            self.edges.append(edge)
            self.connections[destination.name] = edge

        edge = self.connections[destination.name]
        edge.cost += weight

    def __str__(self):
        return_string = "Node: {0}".format({0: self.name})
        return_string += "\n Edges: \n"
        for edge in self.edges:
            return_string += str(edge) + "\n"
        return return_string


class Subset(object):
    def __init__(self, parent, rank):
        self.parent = parent
        self.rank = rank
