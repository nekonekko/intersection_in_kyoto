import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df_nodes = pd.read_csv("data/nodes.csv", index_col=0)
df_edges = pd.read_csv("data/edges.csv")

df_nodes["indegree"] = df_edges["to"].value_counts()
df_nodes["indegree"] = df_nodes["indegree"].fillna(0).astype(int)

sorted_graph = df_nodes[df_nodes["indegree"] == 0].index.tolist()
q = sorted_graph.copy()
while q:
    from_node = q.pop()
    for _, (_, to_node) in df_edges[df_edges["from"] == from_node].iterrows():
        df_nodes.loc[to_node, "indegree"] -= 1
        if df_nodes.loc[to_node, "indegree"] == 0:
            q.append(to_node)
            sorted_graph.append(to_node)

assert len(sorted_graph) == len(df_nodes), "Graph is not a DAG"

print(sorted_graph)
