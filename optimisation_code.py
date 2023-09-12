import networkx as nx
import matplotlib.pyplot as plt
import random as rd
from gurobipy import *

# Define the list of commodities
commodities = ['first', 'second']

# Create an empty graph using NetworkX
G = nx.Graph()

# Read data from the CSV file to populate the graph
filename = "./WVdata.csv"
f = open(filename, 'r')
for row in f:
    myrow = row.strip().split(sep=',', maxsplit=2)
    myrow[2] = int(myrow[2])
    G.add_node(myrow[0])
    G.add_node(myrow[1])
    G.add_edge(myrow[0], myrow[1], weight=myrow[2])

# Position the nodes in the graph for visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=10)

# Initialize commodity-specific attributes for each node
for k in commodities:
    for (i, d) in G.nodes(data=True):
        d[k] = 0

# Set the capacity of each edge to 1
for (i, j, d) in G.edges(data=True):
    d['capacity'] = 1

# Randomly select supplier and terminal nodes for each commodity
supplier = rd.sample(list(G.nodes()), 2)
terminals = rd.sample(list(G.nodes()), 2)

# Set the supply/demand attributes for terminals and suppliers
for i, d in G.nodes(data=True):
    if i == terminals[0]:
        d['first'] = 2
        print(i, d['first'])
    if i == terminals[1]:
        d['second'] = 2
        print(i, d['second'])
    if i == supplier[0]:
        d['first'] = -2
        print(i, d['first'])
    if i == supplier[1]:
        d['second'] = -2
        print(i, d['second'])

# Create a Gurobi model
m = Model('commodityflow')

# Define decision variables for flow on edges
x = {}
for k in commodities:
    for i, d in G.nodes(data=True):
        for j in G.nodes():
            if (i, j) in G.edges():
                x[(k, i, j)] = m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name='x.{0}.{1}.{2}'.format(k, i, j))

# Capacity constraints for edges
for (i, j, d) in G.edges(data=True):
    sum9 = 0
    for k in commodities:
        if ('capacity' in d):
            sum9 += x[(k, i, j)]
    m.addConstr(sum9 <= d.get('capacity', 0))

# Flow conservation constraints for nodes and commodities
for k in commodities:
    for i, d in G.nodes(data=True):
        sum1 = 0
        sum2 = 0
        for j in G.nodes():
            if i != j:
                if (i, j) in G.edges():
                    sum1 += x[(k, i, j)]
                if (j, i) in G.edges():
                    sum2 += x[(k, j, i)]
        m.addConstr((sum2 - sum1) == d[k])

# Objective function to minimize transportation cost
obj = 0
for k in commodities:
    for i, j, d in G.edges(data=True):
        obj += x[(k, i, j)] * d['weight']

# Update the model and set the objective to minimize cost
m.update()
m.setObjective(obj, GRB.MINIMIZE)

# Optimize the Gurobi model
m.optimize()

# Extract the optimal flow routes for each commodity
route1 = [(i, j) for (i, j) in G.edges() if x[('first', i, j)].X > 0 or x[('first', j, i)].X > 0]
route2 = [(i, j) for (i, j) in G.edges() if x[('second', i, j)].X > 0 or x[('second', j, i)].X > 0]

# Visualize the graph with optimal flow routes
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='b', node_size=2, alpha=0.2)
nx.draw_networkx_nodes(G, pos, nodelist=supplier, node_color='y', node_size=20)
nx.draw_networkx_nodes(G, pos, nodelist=terminals, node_color='r', node_size=20)
nx.draw_networkx_edges(G, pos, edgelist=route1, edge_color='g', width=1)
nx.draw_networkx_edges(G, pos, edgelist=route2, edge_color='black', width=1)
plt.savefig("k=2.png", dpi=1000)
