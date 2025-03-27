# visualization.py: Handles graph visualization

import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(toolkit):
    """Generate resource allocation graph."""
    G = nx.DiGraph()
    for p in range(toolkit.num_processes):
        G.add_node(f"P{p}", color='lightblue')
    for r in range(toolkit.num_resources):
        G.add_node(f"R{r}", color='lightgreen')

    for p in range(toolkit.num_processes):
        for r in range(toolkit.num_resources):
            if toolkit.allocation[p][r] > 0:
                G.add_edge(f"R{r}", f"P{p}", label=f"{toolkit.allocation[p][r]}")
            if toolkit.request[p][r] > 0:
                G.add_edge(f"P{p}", f"R{r}", label=f"{toolkit.request[p][r]}")

    pos = nx.spring_layout(G)
    colors = [G.nodes[node]['color'] for node in G.nodes()]
    nx.draw(G, pos, node_color=colors, with_labels=True, node_size=800, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Resource Allocation Graph")
    plt.show()