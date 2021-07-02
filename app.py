import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, text
import pandas as pd


st.title("Christie Pavey's Council App")

df = pd.read_csv("data/council_data_new.csv")
councils = df["council"].values.tolist()
councils = list(set(councils))
all_data  = {}
for item in councils:
    all_data[item] = []

for index, row in df.iterrows():
    all_data[row['council']].append(row['person'])
people = df["person"].values.tolist()
people = list(set(people))
person_data = {}
for item in people:
    person_data[item] = []
for index, row in df.iterrows():
    person_data[row['person']].append(row['council'])

new_people = ["councils"]+people
everything = {}
everything2 = []
for council in councils:
    temp = [council]
    temp2 = {"councils": council}
    for person in people:
        if person in all_data[council]:
            temp.append(1)
            temp2[person] = 1
        else:
            temp.append(0)
            temp2[person] = 0
    everything[council] = temp
    everything2.append(temp2)
new_df = pd.DataFrame(columns=new_people)
new_df = new_df.append(everything2)
from collections import Counter
import operator
def find_groups(min_occurences):
    total = 0
    groupings = []
    for person in people:
        council_matches = []
        pairs = []
        counter = 0
        for council in all_data:
            for person2 in people:
                if person2 != person:
                    if person2 in all_data[council] and person in all_data[council]:
                        pairs.append((person, person2))
                        council_matches.append(council)
        pairs = Counter(pairs)
        x=0
        for pair in pairs:
            x=x+1
            if pairs[pair] > min_occurences:
                counter += 1
                groupings.append(pair)
        total += counter
        final = []
        for group in groupings:
            sorted_list = tuple(sorted(group))
            final.append(sorted_list)
        final = list(set(final))

    return (len(final), final)
def find_max_overlap(min_occurences):
    total = 0
    groupings = []
    for person in people:
        pairs = []
        counter = 0
        for council in all_data:
            council_matches = []
            for person2 in people:
                if person2 != person:
                    for person3 in people:
                        if person3 !=person and person3 != person2:
                            if person2 in all_data[council] and person in all_data[council] and person3 in all_data[council]:
                                pairs.append((person, person2, person3))
                                council_matches.append(council)
        pairs = Counter(pairs)
        x=0
        for pair in pairs:
            x=x+1
            if pairs[pair] > min_occurences:
                counter += 1
                groupings.append(pair)
        total += counter
        final = []
        for group in groupings:
            sorted_list = tuple(sorted(group))
            final.append(sorted_list)
        final = list(set(final))
    return (len(final), final)
option = st.selectbox(
                        'Search for Group of:',
                        ('Pairs', 'Triplets'))
search = int(st.text_input("Enter Number of Councils Pairs appear at Councils:"))
if option == "Pairs":
    quantity, hits = find_groups(search)
    grouping = "pairs"
else:
    quantity, hits = find_max_overlap(search)
    grouping = "triplets"

st.text(f"There are {quantity} examples of {grouping} that appear at councils {search} times together. They are:")
for hit in hits:
    if grouping == "pairs":
        st.text(f"{hit[0]} and {hit[1]}")
    else:
        st.text(f"{hit[0]}, {hit[1]} and {hit[2]}")
G = nx.Graph()
df1 = df[['council', 'person']]
G = nx.from_pandas_edgelist(df1, 'council', 'person')
color_map = []

for node in G:
    if node in df["council"].values:
        color_map.append("coral")
    else:
        color_map.append("darkseagreen")
d = nx.degree(G)
d = [(d[node]+1) * 40 for node in G.nodes()]
import math
import pydot
pos = nx.spring_layout(G, k=10/math.sqrt(G.order()))
from matplotlib.pyplot import figure
fig = figure(figsize=(30, 30))
data = nx.draw_networkx(G,  node_color=color_map, with_labels=True, node_size=d, font_size=12)
plt.savefig("temp.png")
st.image("temp.png")
