import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, text
from pyvis.network import Network

with open ("data/tags.txt", "r") as f:
    lines = f.readlines()

G = nx.Graph()
all_data = []
for line in lines:
    line = line.replace("\n", "")
    items = line.split("***")
    final = []
    for item in items:
        item =item.replace(" ", "_").strip()
        if item != "" and item != "transmission":
            final.append(item)
    items = final
    for item in items:
        for other in items:
            if other != item:
                G.add_edge(item, other)
                all_data.append((item, other))

fields = ["source", "target"]
import csv
with open ("data/christie_data.csv", "w") as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(all_data)
plt.figure(3,figsize=(20,20))

d = dict(G.degree)
pos = nx.spring_layout(G, k=0.2, iterations=20)
nx.draw(G, pos=pos,node_color='orange',
        with_labels=True,
        node_size=[d[k]*300 for k in d])



nt = Network(height="1000px", width="100%", bgcolor="#222222", font_color="white", heading="Christie Pavey's Data")



nt.from_nx(G)
neighbor_map = nt.get_adj_list()


for node in nt.nodes:
    node["title"] = node["id"]
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])

# for node, (x, y) in pos.items():
#     text(x, y, node, fontsize=d[node]*.2, ha='center', va='center')
nt.show_buttons(filter_=['physics'])
nx.write_adjlist(G, "complete-graph.txt")
nt.write_html("pavey_graph.html")

# plt.show()
