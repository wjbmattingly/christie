import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, text
from pyvis.network import Network

names = []
with open ("data/names.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        try:
            name = name.split()[0]
        except:
            IndexError
            name = line
        name  = line.replace("\n", "").replace(" senex", "")
        names.append(name)

councils = []
with open ("data/councils.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        councils.append(line.replace("\n", ""))

for name in names:
    G.add_node(name, color="blue")
print (len(names))
print (len(councils))
G = nx.Graph()
all_data = []
x=0
for name in names:
    G.add_edge(name, councils[x])
    all_data.append((name, councils[x]))


    x=x+1
for item in all_data:
    name, council = item
    for item2 in all_data:
        if name != item2[0]:
            if council == item2[1]:
                G.add_edge(name, item2[0])
fields = ["council", "person"]
import csv
with open ("data/christie_data_councils.csv", "w") as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(all_data)
plt.figure(3,figsize=(20,20))

d = dict(G.degree)
pos = nx.spring_layout(G, k=0.2, iterations=20)
nx.draw(G, pos=pos,node_color='orange',
        with_labels=True,
        node_size=[d[k]*300 for k in d])



nt = Network(height="1500px", width="100%", bgcolor="#222222", font_color="white", heading="Christie Pavey's Data")



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
nt.write_html("pavey_graph_councils.html")

# plt.show()
