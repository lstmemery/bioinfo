__author__ = 'memery'

import networkx as nx
from itertools import product
from random import choice

def eulerian_cycle(graph):
    return [i for i in nx.eulerian_circuit(graph)]


def make_graph(*edges):
    graph = nx.DiGraph()
    for edge in edges:
        start, end = edge.split(' -> ')
        if ',' in end:
            for node in end.split(','):
                graph.add_edge(start, node.strip())
        else:
            graph.add_edge(start, end.strip())
    return graph


def add_eulerian_bridge(G):
    [start_node] = [x for x in G.in_degree() if G.in_degree(x) - G.out_degree(x) == 1]
    [end_node] = choice([x for x in G.in_degree() if G.in_degree(x) - G.out_degree(x) == -1])
    G.add_edge(start_node, end_node)
    cycle = eulerian_cycle(G)
    for i in range(len(cycle)):
        if cycle[i] == (start_node, end_node):
            prefix, suffix = cycle[:i], cycle[i + 1:]
            del cycle[i]
            cycle = suffix + prefix
            break
    return cycle

def add_random_eulerian_bridge(G):
    start_nodes = [x for x in G.in_degree() if G.in_degree(x) - G.out_degree(x) == 1]
    end_nodes = [x for x in G.in_degree() if G.in_degree(x) - G.out_degree(x) == -1]
    start_node, end_node = choice(start_nodes), choice(end_nodes)
    G.add_edge(start_node, end_node)
    answered = False
    while not answered:
        try:
            cycle = eulerian_cycle(G)
        except nx.exception.NetworkXError:
            pass
        else:
            answered = True
    for i in range(len(cycle)):
        if cycle[i] == (start_node, end_node):
            prefix, suffix = cycle[:i], cycle[i + 1:]
            del cycle[i]
            cycle = suffix + prefix
            break
    return cycle

def print_eulerian(*euler):
    path = euler[0][0]
    for i in range(len(euler)):
        path = '{}->{}'.format(path, euler[i][1])
    return path


def make_de_bruijin_graph(*kmers): #used to have a k. see if this matters
    graph = nx.DiGraph()
    for kmer in kmers:
        graph.add_edge(kmer[:-1], kmer[1:])
    return graph

def reconstruct_string(graph):
    path = add_eulerian_bridge(graph)
    reconstructed = path[0][0]
    for i in path:
        reconstructed = '{}{}'.format(reconstructed, i[1][-1])
    return reconstructed

def reconstruct_uni_string(k, graph):
    cycle = eulerian_cycle(graph)
    reconstructed = cycle[0][0]
    for i in cycle[:-k+1]:
        reconstructed = '{}{}'.format(reconstructed, i[1][-1])
    return reconstructed

def make_double_string_graph(*double_kmers):
    first_graph, second_graph = nx.DiGraph(), nx.DiGraph()
    for double_kmer in double_kmers:
        first, second = double_kmer.strip().split('|')
        first_graph.add_edge(first[:-1], first[1:])
        second_graph.add_edge(second[:-1], second[1:])
    return first_graph, second_graph

def reconstruct_double_string(first_graph, second_graph, l, d):
    first_path = reconstruct_string(first_graph)
    second_path = reconstruct_string(second_graph)
    reconstructed = '{}{}'.format(first_path, second_path[-d-l:])
    return reconstructed

def generate_binary_strings(size):
    return [''.join(x) for x in product('01', repeat=int(size))]

if __name__ == '__main__':
    with open('dataset_6206_7.txt') as data:
        l, d = data.readline().split(' ')
        l, d = int(l), int(d)
        graph1, graph2 = make_double_string_graph(*(x.strip() for x in data.readlines()))
    with open('output.txt', 'w+') as out:
        out.write(reconstruct_double_string(graph1, graph2, l, d))