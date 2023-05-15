import argparse
from clustering import perform_clustering
from coupling_logic.contributor_coupling import perform_contributor_coupling
from coupling_logic.structural_similarity_coupling import perform_structural_similarity_coupling
from coupling_logic.logical_coupling import perform_logical_coupling
from coupling_logic.semantic_coupling import perform_semantic_coupling
from coupling_logic.helper import CouplingType


def pretty_print_connected_components(connected_components):
    i = 1
    for component in connected_components:
        print("Cluster " + str(i) + " :")
        print("Python files part of the cluster - ")
        for file in component:
            if isinstance(file, str):
                print(file)
            else:
                print(file.name, end="\n")
        print("\n")
        i += 1


def run(repository_path, local_path, target_partition, coupling_type: CouplingType):

    nodes_map = {}
    if coupling_type == CouplingType.CONTRIBUTOR_COUPLING:
        nodes_map = perform_contributor_coupling(repository_path, local_path)
    if coupling_type == CouplingType.STRUCTURAL_COUPLING:
        nodes_map = perform_structural_similarity_coupling(repository_path, local_path)
    if coupling_type == CouplingType.SEMANTIC_COUPLING:
        nodes_map = perform_semantic_coupling(repository_path, local_path)
    if coupling_type == CouplingType.LOGICAL_COUPLING:
        nodes_map = perform_logical_coupling(repository_path, local_path)

    connected_components = perform_clustering(nodes_map, target_partition)
    pretty_print_connected_components(connected_components)


if __name__ == '__main__':
    test_repository_path = "https://github.com/ar1422/retail-transaction-data-management-and-customer-analytics.git"
    parser = argparse.ArgumentParser(prog='Extraction of Microservices',
                                      description='Extraction of Microservices from Monolithic Software Architectures',
                                      epilog='Text at the bottom of help')

    parser.add_argument('localpath', type=str, help="Local directory for cloning the Github repository")
    args = parser.parse_args()
    run(test_repository_path, args.localpath, 4, CouplingType.SEMANTIC_COUPLING)

