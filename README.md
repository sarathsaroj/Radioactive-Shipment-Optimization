## Optimization of multi commodity network flow

### Problem Statement
The objective of this project is to formulate a linear program for solving an edge disjoint multi commodity network flow problem. The selected problem involves sending shipments carrying radioactive materials from multiple origin points to the corresponding destinations. The objective is to find edge disjoint routes (same route is not shared by shipments) while solving the MCNF at the minimum cost possible. Road network of West Virginia is the graph network used for this purpose.


### Formulation

To solve MCFP, two necessary constraints must be considered. The first one is the travel demand constraint. It means that all the commodities need to be transported to their destinations. The other one is the edge capacity constraint. It means that the flows on each edge cannot exceed the flow capacity. Since we are dealing with edge disjoint flow, capacities of all edges are 1. This means that each edge can carry only one unit of flow. The first constraint is essentially the sum of a set of single-commodity flow problems. However, the second constraint needs to consider all the commodities together and it causes the interaction between commodities.

G(V,E) is a directed network. Here V and E are the set of nodes and edges and they have a size of n and m, respectively. For each edge ij, there is a cost cij and capacity uij. We need to transport K kinds of commodities from their origin nodes to destination nodes. s and t are used to represent origin and destination node of commodity k. In addition, dk is the travel demand of commodity k. We need to find an optimal flow assignment with minimum cost, satisfying the travel demand and edge disjoint constraints for this problem. Thus, the MCFN problem can be formulated as following:

``` math
\min_{\mathbf{Z}^*} (\mathbf{x}) = \sum_{i,j,k} c_{ij} x_{ijk} \quad \text{subject to}
```

``` math
Constraint 1:

\sum_{i,j \in \mathcal{A}} x_{ijk} - \sum_{j,i \in \mathcal{A}} x_{jik} = b_{ik} \quad \forall i \in \mathcal{N}, \forall k \in \mathcal{K}
``` 
``` math
Constraint 2:

\sum_{i,j \in \mathcal{A}} x_{ijk} \leq u_{ij} \quad \forall (i,j) \in \mathcal{A}
``` 

``` math
Variable Restriction:

x_{ijk} \in \{0,1\} \quad \text{for } i \in \mathcal{A}, \forall k \in \mathcal{K}
```

``` math
Where:b_{ik} = 
\begin{cases}
d_k & \text{if } i = s_k \\
-d_k & \text{if } i = t_k \\
0 & \text{if } i \in \mathcal{N} \setminus \{s_k, t_k\}
\end{cases}
```

The objective function aims to minimize the total transportation cost. Constraint 1 is the supply/demand constraint. Constraint 2 is the capacity constraint . Capacity of every edge is set to 1 making this an edge disjoint problem and variable restriction 3 decides whether flow of commodity k happens on edge i,j.

### Methodology & Output
This project is done with Gurobi and NetworkX packages on python. Road network node data is collected as a txt file and a Graph is created with NetworkX. Gurobi optimizer is used to optimize the flow to get an edge disjoint MCNF. The formulation used in Gurobi is same as shown in earlier section.
The network is tested for single commodity,2 commodity, 3 commodity and 4 commodity minimum cost flows with edge disjoint constraint


