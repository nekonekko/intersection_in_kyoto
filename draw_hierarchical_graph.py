import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df_edges = pd.read_csv("data/edges.csv")
df_nodes = pd.read_csv("data/nodes.csv", index_col=0)

df_nodes["outdegree"] = df_nodes.index.map(df_edges["from"].value_counts())
df_nodes["outdegree"] = df_nodes["outdegree"].fillna(0).astype(int)

df_nodes["layer"] = None
df_nodes["pos_x"] = None
current_layer = 0
while df_nodes["layer"].isna().any():
    outdegree_after = df_nodes["outdegree"].copy()
    pos_x = 0
    for node_name, row in df_nodes.iterrows():
        if row["outdegree"] == 0 and row["layer"] is None:
            df_nodes.loc[node_name, "layer"] = current_layer
            df_nodes.loc[node_name, "pos_x"] = pos_x
            outdegree_after.loc[df_edges[df_edges["to"] == node_name]["from"]] -= 1
            if pos_x >= 0:
                pos_x = -pos_x - 1
            else:
                pos_x = -pos_x

    current_layer += 1
    df_nodes["outdegree"] = outdegree_after

pos = {
    node_name: (row["pos_x"], row["layer"]) for node_name, row in df_nodes.iterrows()
}


plt.figure(figsize=(15, 8))
G = nx.DiGraph()
G.add_nodes_from(df_nodes.index)
G.add_edges_from(df_edges[["from", "to"]].values)

node_color = []
for node in G._node:
    if df_nodes.loc[node, "is_vertical"]:
        node_color.append("tab:cyan")
    else:
        node_color.append("tab:olive")

nx.draw(
    G,
    pos,
    with_labels=True,
    font_family="Osaka",
    node_size=800,
    node_color=node_color,
    font_size=8,
)
plt.savefig("fig/hierarchical_graph.png")
