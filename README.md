# Pathfinding Algorithm Visualizer

An interactive grid-based visualizer that runs **BFS**, **DFS**, and
**Dijkstra's algorithm** and animates how each one explores the grid
before finding a path from a start cell to an end cell.

## Features

- Interactive grid-based environment
- Place a start and destination cell
- Create and remove walls
- Animated BFS exploration
- Animated DFS exploration
- Animated Dijkstra exploration
- Visual representation of visited cells
- Final path highlighted separately
- Runtime, number of visited cells, and path length displayed
- Algorithms separated from the visualization layer


## How to run it

```bash
pip install pygame
python main.py
```

**Controls:**
- Left click: 1st click places the **start** (green), 2nd click places
  the **end** (red), every click after that draws **walls**
- Right click: erase a cell
- `B` → run BFS
- `D` → run DFS
- `J` → run Dijkstra
- `C` → clear the grid

While an algorithm runs, cells light up light blue as they're
*visited*, and the final path is highlighted in yellow, along with a
status line showing runtime (ms), number of cells visited, and path
length.

## Project structure

```
pathfinder/
├── main.py         # Pygame UI: grid drawing, mouse/keyboard input, animation
├── algorithms.py   # BFS, DFS, Dijkstra — pure functions, no UI dependency
└── README.md
```

`algorithms.py` has no dependency on Pygame at all — the algorithms
take a plain grid and two coordinates and return plain data. That
separation was deliberate: it means the pathfinding logic can be
tested (see below) completely independently of the visualization.

## Complexity comparison

| Algorithm | Data structure | Time complexity | Space | Shortest path guaranteed? |
|---|---|---|---|---|
| BFS | Queue (FIFO) | O(V + E) | O(V) | Yes, if all edges have equal weight |
| DFS | Stack (LIFO) | O(V + E) | O(V) | No — finds a path, not necessarily the shortest |
| Dijkstra | Min-heap (priority queue) | O((V + E) log V) | O(V) | Yes, with non-negative edge weights |

On this specific grid, every move costs exactly 1, so BFS and Dijkstra
will return a path of the same minimum length. Dijkstra performs
additional priority-queue bookkeeping to solve a problem that BFS
already solves optimally on an unweighted grid.

The distinction becomes important when edges have different weights.
For example, some cells could represent terrain with higher movement
costs. BFS cannot account for these weights, while Dijkstra can find
the minimum-cost path by expanding the node with the smallest known
total distance.

DFS is included as a contrast. It can determine whether a path exists,
but it does not guarantee the shortest path. Its depth-first exploration
also makes it useful for problems such as maze generation, cycle
detection, and topological sorting.

## Technologies

- Python
- Pygame
- Data Structures & Algorithms
- Graph Traversal

