import os
import itertools
from git_operations import clone_repository, get_all_file_names, get_contributors_map
from graph import Node


def perform_contributor_coupling(repository_path, local_path):

    nodes = {}
    if not os.path.exists(local_path):
        clone_repository(repository_path, local_path)

    list_of_all_files = get_all_file_names(local_path)
    contributors_map = get_contributors_map(local_path, list_of_all_files)

    for file_1, file_2 in itertools.combinations(contributors_map.keys(), 2):
        if file_1 not in nodes:
            node_1 = Node(file_1)
            nodes[file_1] = node_1
        if file_2 not in nodes:
            node_2 = Node(file_2)
            nodes[file_2] = node_2

        common_developers = contributors_map[file_1].intersection(contributors_map[file_2])
        if len(common_developers) == 0:
            weight = 0
        else:
            weight = 1 / len(common_developers)

        source = nodes[file_1]
        destination = nodes[file_2]
        source.add_edge(destination, weight)
        destination.add_edge(source, weight)

    return nodes


if __name__ == '__main__':
    test_repository_path = "https://github.com/ar1422/retail-transaction-data-management-and-customer-analytics.git"
    test_local_path = r"C:\Users\Lenovo\PycharmProjects\CSCI-620-Summer-2205\retail-transaction-data-management-and-customer-analytics"
    test_nodes = perform_contributor_coupling(test_repository_path, test_local_path)
    for _, test_node in test_nodes.items():

        for test_edge in test_node.edges:
            if test_edge.cost > 5:
                print(test_edge)

