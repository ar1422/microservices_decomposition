import ast
import os
import itertools
from graph import Node
from git_operations import clone_repository, get_all_file_names
from function_call_tracker import FunctionCallTracker


def get_all_function_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_visitor = FunctionCallTracker()
            call_visitor.visit(node.func)
            func_calls.append(call_visitor.name)

    return func_calls


def perform_structural_similarity_coupling(repository_path, local_path):
    if not os.path.exists(local_path):
        clone_repository(repository_path, local_path)

    all_files_list = get_all_file_names(repository_path)
    all_pairs = generate_pair_of_classes(all_files_list)
    nodes = {}
    for file_1, file_2 in all_pairs:
        if file_1 not in nodes:
            node_1 = Node(file_1)
            nodes[file_1] = node_1
        if file_2 not in nodes:
            node_2 = Node(file_2)
            nodes[file_2] = node_2

    return nodes


def generate_pair_of_classes(all_files_list):
    all_pairs = []
    for pair_of_classes in itertools.combinations(all_files_list, 2):
        all_pairs.append(pair_of_classes)
    return all_pairs


if __name__ == '__main__':
    test_repository_path = "https://github.com/ar1422/retail-transaction-data-management-and-customer-analytics.git"
    test_local_path = r"C:\Users\Lenovo\PycharmProjects\CSCI-620-Summer-2205\retail-transaction-data-management-and-customer-analytics"
    test_nodes = perform_structural_similarity_coupling(test_repository_path, test_local_path)
    for _, test_node in test_nodes.items():

        for test_edge in test_node.edges:
            if test_edge.cost > 5:
                print(test_edge)
