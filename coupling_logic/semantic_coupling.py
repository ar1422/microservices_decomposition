import itertools
import keyword
import os
from graph import Node
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from git_operations import get_all_file_names, clone_repository

STOP_WORDS = ["@", "''", ".com", ']', '.', '{', ')', '-', '[', '/', '%', '}', '(', '\\', ':', "'", '=']


def apply_stop_words(list_of_tokens):
    filtered_tokens = []
    stop_words = keyword.kwlist + STOP_WORDS
    for token in list_of_tokens:
        if token not in stop_words:
            filtered_tokens.append(token)

    return filtered_tokens


def get_all_doc_content(filenames):
    all_tokens = []
    for filename in filenames:
        with open(filename) as file:
            text = file.read()
            tokens = word_tokenize(text)
            all_tokens = all_tokens + tokens
    return all_tokens


def tokenize_the_file_content(filename):
    with open(filename) as file:
        text = file.read()

    tokens = word_tokenize(text)
    tokens = apply_stop_words(tokens)
    return tokens


def cosine_similarity(text_1, text_2, all_doc):
    vectorizer = TfidfVectorizer(all_doc)
    tfidf = vectorizer.fit_transform([text_1, text_2])
    return (tfidf * tfidf.T).A[0, 1]


def generate_pair_of_classes(all_files_list):
    all_pairs = []
    for pair_of_classes in itertools.combinations(all_files_list, 2):
        all_pairs.append(pair_of_classes)
    return all_pairs


def construct_string_from_list(text_list):
    return_string = ""
    for text in text_list:
        return_string += text + " "

    return return_string


def perform_semantic_coupling(repository_path, local_path):
    if not os.path.exists(local_path):
        clone_repository(repository_path, local_path)

    all_files_list = get_all_file_names(local_path)
    all_pairs = generate_pair_of_classes(all_files_list)
    nodes = {}
    for file_1, file_2 in all_pairs:
        if file_1 not in nodes:
            node_1 = Node(file_1)
            nodes[file_1] = node_1
        if file_2 not in nodes:
            node_2 = Node(file_2)
            nodes[file_2] = node_2

        all_tokens = get_all_doc_content(all_files_list)
        tokens_1 = tokenize_the_file_content(file_1)
        tokens_2 = tokenize_the_file_content(file_2)
        cosine_score = cosine_similarity(construct_string_from_list(tokens_1), construct_string_from_list(tokens_2), all_tokens)
        source = nodes[file_1]
        destination = nodes[file_2]
        source.add_edge(destination, cosine_score)
        destination.add_edge(source, cosine_score)

    return nodes


if __name__ == '__main__':
    test_repository_path = "https://github.com/ar1422/retail-transaction-data-management-and-customer-analytics.git"
    test_local_path = r"C:\Users\Lenovo\PycharmProjects\CSCI-620-Summer-2205\retail-transaction-data-management-and-customer-analytics"
    test_nodes = perform_semantic_coupling(test_repository_path, test_local_path)
    for _, test_node in test_nodes.items():

        for test_edge in test_node.edges:
            if test_edge.cost > 5:
                print(test_edge)
