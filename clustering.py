import networkx as nx
from coupling_logic.contributor_coupling import perform_contributor_coupling


def perform_clustering(nodes_map, target_partition):

    input_graph = nx.Graph()

    for node_name in nodes_map:
        for edge in nodes_map[node_name].edges:
            if edge.cost != 0:
                input_graph.add_weighted_edges_from([(edge.source.name, edge.destination.name, edge.cost)])
            else:
                input_graph.add_weighted_edges_from([(edge.source.name, edge.destination.name, 0)])

    mst_tree = nx.minimum_spanning_tree(input_graph)
    sorted_edges = sorted(mst_tree.edges)
    sorted_edges.reverse()

    num_of_partition = 1
    connected_components = None
    while num_of_partition < target_partition:
        mst_tree.remove_edge(sorted_edges[0][0], sorted_edges[0][1])
        connected_components = list(nx.connected_components(mst_tree))
        num_of_partition = len(connected_components)
        sorted_edges.pop(0)

    return connected_components


if __name__ == '__main__':
    test_repository_path = "https://github.com/ar1422/retail-transaction-data-management-and-customer-analytics.git"
    test_local_path = r"C:\Users\Lenovo\PycharmProjects\CSCI-620-Summer-2205\retail-transaction-data-management-and-customer-analytics"

    perform_clustering(test_repository_path, test_local_path, 5)
