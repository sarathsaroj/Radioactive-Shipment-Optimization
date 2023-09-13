```
import networkx as nx
import matplotlib.pyplot as plt
import random as rd
from gurobipy import *

# Enter number of shipments here.
k = 3
commodities = [f'commodity_{i}' for i in range(1, k+1)]

# Empty graph using NetworkX
G = nx.Graph()

# Road network data is available with the name 'WVdata.csv'
filename = "./WVdata.csv"  # Replace with your actual data file
f = open(filename, 'r')
for row in f:
    myrow = row.strip().split(sep=',', maxsplit=2)
    myrow[2] = int(myrow[2])
    G.add_node(myrow[0])
    G.add_node(myrow[1])
    G.add_edge(myrow[0], myrow[1], weight=myrow[2])


# Initialize commodity-specific attributes for each node
for commodity in commodities:
    for (i, d) in G.nodes(data=True):
        d[commodity] = 0

# Randomly select supplier and terminal nodes for each commodity
suppliers = rd.sample(list(G.nodes()), k)
terminals = rd.sample(list(G.nodes()), k)

# Visualization of the network with supplier and terminal nodes 
pos = nx.spring_layout(G)
#nx.draw(G, pos, node_size=3,width=0.1)
for i, supplier_node in enumerate(suppliers):
    #nx.draw_networkx_nodes(G, pos, nodelist=[supplier_node], node_color='y', node_size=20, label=f'Supplier {i+1}')
    #nx.draw_networkx_nodes(G, pos, nodelist=[terminals[i]], node_color='r', node_size=20, label=f'Terminal {i+1}')


# Supply/demand attributes for terminals and suppliers
for i, d in G.nodes(data=True):
    for j in range(k):
        if i == terminals[j]:
            d[commodities[j]] = 2
            print(i, d[commodities[j]])
        if i == suppliers[j]:
            d[commodities[j]] = -2
            print(i, d[commodities[j]])
```            
```

# Create a Gurobi model
m = Model('commodityflow')

# Define decision variables for flow on edges
x = {}
for commodity in commodities:
    for i, d in G.nodes(data=True):
        for j in G.nodes():
            if (i, j) in G.edges():
                x[(commodity, i, j)] = m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x.{commodity}.{i}.{j}')

# Capacity constraints for edges
for (i, j, d) in G.edges(data=True):
    for commodity in commodities:
        if ('capacity' in d):
            sum_x = quicksum(x[(commodity, i, j)] for commodity in commodities)
            m.addConstr(sum_x <= d.get('capacity', 0))

# Flow conservation constraints for nodes and commodities
for commodity in commodities:
    for i, d in G.nodes(data=True):
        sum_in = 0
        sum_out = 0
        for j in G.nodes():
            if i != j:
                if (i, j) in G.edges():
                    sum_in += x[(commodity, i, j)]
                if (j, i) in G.edges():
                    sum_out += x[(commodity, j, i)]
        m.addConstr((sum_out - sum_in) == d[commodity])




# Objective function to minimize transportation cost
obj = 0
for commodity in commodities:
    for i, j, d in G.edges(data=True):
        obj += x[(commodity, i, j)] * d['weight']

# Update the model and set the objective to minimize cost
m.update()
m.setObjective(obj, GRB.MINIMIZE)

# Optimize the Gurobi model
m.optimize()

```
```
#Route visualisation
routes = {}
for commodity in commodities:
    routes[commodity] = [(i, j) for (i, j) in G.edges() if x[(commodity, i, j)].X > 0 or x[(commodity, j, i)].X > 0]

# Visualize the graph with optimal flow routes
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='b', node_size=10, alpha=0.2)
for i, supplier_node in enumerate(suppliers):
    nx.draw_networkx_nodes(G, pos, nodelist=[supplier_node], node_color='y', node_size=20, label=f'Supplier {i+1}')
    nx.draw_networkx_nodes(G, pos, nodelist=[terminals[i]], node_color='r', node_size=20, label=f'Terminal {i+1}')
    nx.draw_networkx_edges(G, pos, edgelist=routes[commodities[i]], edge_color=f'C{i}', width=1, label=f'Route {i+1}')

plt.legend()
plt.savefig(f"k={k}.png", dpi=1000)
plt.show()
```

