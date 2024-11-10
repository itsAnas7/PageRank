# Page Rank algorithm

This repository contains all the necessary elements to run the *Vanilla Page Rank* algorithm.

This algorithm is based on the concept of Markov's chain. This was used at a time to rank, establish order of importance between web pages.

However, this is not the only use case of course. In our case, the Page Rank algorithm is used on a history of wikispeedias games.

A game of wikispeedia consists of starting from a wikipedia's page **A** and trying to land on **B** in a minimum of pages.

Further details about the data set can be found inside the file `data\paths_finished.tsv`.

# Technical aspect

The *Vanilla Page Rank* algorithm first represents all the **hyperlinks** between the pages as **edges** and the pages being the **nodes**. We then end up with a relatively huge graph.

The first step is to construct the **adjacency matrix** noted $A$. If there is an outgoing link between **A** and **B** then $A_{B, A} = 1$ (The columns represent the sources and the rows are the targets).

Then, we build the **Transition matrix** noted $T$. This matrix is column-stochastic. For each column in $A$ (i.e each source node) we compute the total sum and divide each element of the column by this sum.

Finally, we run the *Vanilla Page Rank* algorithm :

$V_n = T.V_{n-1}$

- $V_n$ : The importance vector at the n-th iteration.

By default, 
```math 
V_0 = \begin{bmatrix} \frac{1}{N} \\ \vdots \\ \frac{1}{N} \end{bmatrix}
```

- N : The total number of pages.

## Spider-trap

In the section above, the computation of the importance vector $V$ only relies on the transition matrix, that is to say the existing **hyperlinks** there are in our network.

However, this creates a major issue called the *Spider-trap*. In a network, it could be possible that a node **A** has no outgoing links that lead to other pages (only to itself). Overtime, this node, if we only rely on $T$, will absorb all the importance over the network and the importance vector won't make sense anymore.

A solution that was imagined was called *teleportation*. We create another graph on top of the existing one and compute its own adjacency and transition matrices, we will note them $\tilde{A}$ and $\tilde{T}$.


In this graph,
```math
\tilde{A} = \begin{bmatrix}
1 & 1 & \dots & 1 \\
1 & 1 & \dots & 1 \\
\vdots & \vdots & \ddots & \vdots \\
1 & 1 & \dots & 1 \\
\end{bmatrix}
```

```math
\tilde{T} = \begin{bmatrix}
\frac{1}{N} & \frac{1}{N} & \dots & \frac{1}{N} \\
\frac{1}{N} & \frac{1}{N} & \dots & \frac{1}{N} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{1}{N} & \frac{1}{N} & \dots & \frac{1}{N} \\
\end{bmatrix}
```

The final equation for the importance vector using teleportation is :

$V_n = \beta * T.V_{n-1} + (1 - \beta)*\tilde{T}.V_{n-1}$

- $\beta$ : The weight put on relying on the original graph (i.e network)

It's important to note that since 
```math
V_0 = \begin{bmatrix} \frac{1}{N} \\ \vdots \\ \frac{1}{N} \end{bmatrix} 
```
Then,

```math
\forall n , \tilde{T}.V_{n} = \begin{bmatrix} \frac{1}{N} \\ \vdots \\ \frac{1}{N} \end{bmatrix} = V_0
```



We note $\forall n$ , $\tilde{c} = \tilde{T}.V_n$

Then, $V_n = \beta * T.V_{n-1} + (1 - \beta)*\tilde{c}$

## Couple subtleties

In our data set there are some pages (i.e nodes) that don't have any outgoing links, not even to themselves. This would cause serious problem while creating the transition matrix since the sum over that column would be 0.

The solution we came up with consists of placing an outgoing link to the node itself, basically allowing $T$ to still be column-stochastic while not distributing the node's importance elsewhere (i.e Spider-trap).

# Run the algorithm

All the code from cleaning the data set to running the algorithm is, for now, contained in the notebook `01-PageRank.ipynb`.

## Set up with Poetry

```
poetry install requirements.txt
```

## Set up without Poetry

```
pip install requirements.txt
```

The last cell of notebook returns the TOP 10, that is to say, the first ten pages with the maximum of importance.

# Source

This project was broadly inspired by the series of video made by Dr. Shahriar HOSSAIN from the YouTube channel **Computing For All**.

Here is the link to the videos :

https://www.youtube.com/watch?v=GLTmDe-l9e4&list=PLJXHwy-4vGRY8QylvZomOvyYb1qZvTghk
