import os
from git_operations import clone_repository, get_commits
from graph import Node


def perform_logical_coupling(repository_path, local_path):
    if not os.path.exists(local_path):
        clone_repository(repository_path, local_path)

    list_of_commits = get_commits(local_path)
    nodes = create_graph(list_of_commits)
    return nodes


def create_graph(commits: list):
    nodes = {}
    for commit in commits:
        for itr, file in enumerate(commit["changes"]):
            if file not in nodes:
                node = Node(file)
                nodes[file] = node
            source: Node = nodes[file]
            for next_ptr in range(itr + 1, len(commit["changes"])):
                file_name = commit["changes"][next_ptr]
                if file_name not in nodes:
                    node = Node(file_name)
                    nodes[file_name] = node
                destination: Node = nodes[file_name]
                source.add_edge(destination)
                destination.add_edge(source)

    return nodes


if __name__ == "__main__":
    test_repository_path = "https://github.com/iKevinY/EulerPy.git"
    test_local_path = r"C:\Users\Lenovo\PycharmProjects\CSCI-620-Summer-2205\retail-transaction-data-management-and-customer-analytics"
    test_nodes = perform_logical_coupling(test_repository_path, test_local_path)
    for _, test_node in test_nodes.items():

        for test_edge in test_node.edges:
            if test_edge.cost > 5:
                print(test_edge)
