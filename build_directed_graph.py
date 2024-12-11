import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


df_bus_stops_containing_intersection = pd.read_csv(
    "data/bus_stops_containing_intersection_annotated.csv"
)
df_bus_stops_containing_intersection = df_bus_stops_containing_intersection.dropna()
df_bus_stops_containing_intersection["vertical_first"] = (
    df_bus_stops_containing_intersection["vertical_first"].astype(int).astype(bool)
)

nodes, edges = set(), set()
for _, row in df_bus_stops_containing_intersection.iterrows():
    nodes.add(row["vertical"])
    nodes.add(row["horizontal"])
    if row["vertical_first"]:
        edges.add((row["vertical"], row["horizontal"]))
    else:
        edges.add((row["horizontal"], row["vertical"]))

df_nodes = pd.DataFrame(list(nodes), columns=["node"])
df_edges = pd.DataFrame(list(edges), columns=["from", "to"])
for _, row in df_nodes.iterrows():
    node = row["node"]
    if node in df_bus_stops_containing_intersection["vertical"].values:
        df_nodes.loc[df_nodes["node"] == node, "is_vertical"] = True
    else:
        df_nodes.loc[df_nodes["node"] == node, "is_vertical"] = False

df_nodes.to_csv("data/nodes.csv", index=False)
df_edges.to_csv("data/edges.csv", index=False)

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

plt.figure(figsize=(8, 12))
nx.draw(
    G,
    with_labels=True,
    font_family="Osaka",
    node_size=800,
    node_color="tab:cyan",
    font_size=8,
    pos=nx.bipartite_layout(G, df_bus_stops_containing_intersection["vertical"].values),
)
plt.savefig("fig/bipartite_graph.png")
plt.figure(figsize=(12, 8))
nx.draw(
    G,
    with_labels=True,
    font_family="Osaka",
    node_size=800,
    node_color="tab:cyan",
    font_size=8,
    pos=nx.nx_pydot.graphviz_layout(G),
)
plt.savefig("fig/directed_graph.png")
