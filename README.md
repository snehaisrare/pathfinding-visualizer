# Pathfinding Algorithm Visualizer

An interactive grid-based visualizer that runs **BFS**, **DFS**, and
**Dijkstra's algorithm** and animates how each one explores the grid
before finding a path from a start cell to an end cell.

## Why this project

Built to go deeper on graph traversal algorithms after an Amazon SDE1
coding assessment — the goal was to actually implement and compare
these algorithms myself rather than just recall their definitions.

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
| BFS | Queue (FIFO) | O(rows × cols) | O(rows × cols) | Yes, *if all edges have equal weight* |
| DFS | Stack (LIFO) | O(rows × cols) | O(rows × cols) | No — finds *a* path, not the shortest |
| Dijkstra | Min-heap (priority queue) | O(E log V) | O(rows × cols) | Yes, even with *varying* edge weights |

On this specific grid, every move costs exactly 1, so BFS and
Dijkstra will always return a path of the same length — Dijkstra is
essentially doing extra bookkeeping (the heap) to solve a problem BFS
already solves optimally for free. The moment edges get *weighted*
(e.g. some cells cost more to enter — mud, stairs, traffic), BFS stops
being correct and Dijkstra is the one that still works, because it
always expands the node with the smallest known total distance, not
just the node discovered first.

DFS is included purely as a contrast — it's the wrong tool for
*shortest*-path problems, but it's cheap, simple, and useful when you
just need to know "is a path possible at all," or for problems like
maze generation, cycle detection, or topological sorting where order
doesn't matter.

