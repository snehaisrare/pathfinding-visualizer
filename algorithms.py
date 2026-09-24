"""
Pathfinding algorithms on a 2D grid.

Each function takes:
    grid  -> 2D list of ints (0 = open cell, 1 = wall)
    start -> (row, col) tuple
    end   -> (row, col) tuple

Each function returns:
    (visited_order, path)
    visited_order -> list of (row, col) in the order they were explored
                     (used to animate the search)
    path          -> list of (row, col) from start to end, or [] if
                     no path exists

All three algorithms share the same 4-directional neighbor logic, so
the only real difference between them is the *data structure* used to
decide which node to expand next:
    BFS      -> collections.deque   (FIFO queue)
    DFS      -> Python list used as a stack (LIFO)
    Dijkstra -> heapq               (min-heap, priority = distance so far)
"""

from collections import deque
import heapq


def get_neighbors(grid, node):
    """Return valid, non-wall neighbors of `node` (up/down/left/right)."""
    rows, cols = len(grid), len(grid[0])
    r, c = node
    neighbors = []
    # Order matters only for tie-breaking / visual style, not correctness
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def reconstruct_path(came_from, start, end):
    """Walk backwards from `end` to `start` using the came_from map."""
    if end not in came_from and end != start:
        return []  # end was never reached

    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def bfs(grid, start, end):
    """
    Breadth-First Search.

    Explores the grid layer by layer (all nodes at distance 1, then all
    nodes at distance 2, etc.) using a FIFO queue.

    Time complexity:  O(V + E) -> for a grid, V = rows*cols, E ~= 4V,
                       so effectively O(rows * cols)
    Space complexity: O(V) for the visited set + queue

    Guarantee: BFS finds the SHORTEST path in terms of number of edges,
    but only because every edge here has the same weight (1). It has
    no notion of edge weight at all.
    """
    queue = deque([start])
    visited = {start}
    came_from = {}
    visited_order = []

    while queue:
        current = queue.popleft()  # FIFO: oldest node first
        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return visited_order, reconstruct_path(came_from, start, end)


def dfs(grid, start, end):
    """
    Depth-First Search.

    Explores as far as possible down one branch before backtracking,
    using a stack (here, a Python list with append/pop from the end).

    Time complexity:  O(V + E) same asymptotic bound as BFS
    Space complexity: O(V) for the visited set + stack

    Important: DFS does NOT guarantee the shortest path. It just
    guarantees *a* path if one exists. It's included here mainly to
    visually contrast against BFS/Dijkstra during the interview demo.
    """
    stack = [start]
    visited = {start}
    came_from = {}
    visited_order = []

    while stack:
        current = stack.pop()  # LIFO: most recently added node first
        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

    return visited_order, reconstruct_path(came_from, start, end)


def dijkstra(grid, start, end):
    """
    Dijkstra's Algorithm.

    Always expands the unvisited node with the smallest known distance
    from `start`, using a min-heap as a priority queue.

    Time complexity:  O((V + E) log V) because every heap push/pop is
                       O(log V), and each edge can trigger one push
    Space complexity: O(V) for distances + heap

    On this grid every edge has weight 1, so Dijkstra will find the
    same shortest path as BFS here -- the difference only shows up
    once edges have different weights (e.g. "rough terrain" cells
    costing more to enter). It's included so you can explain WHY you'd
    reach for Dijkstra over BFS the moment weights stop being uniform.
    """
    rows, cols = len(grid), len(grid[0])
    dist = {(r, c): float('inf') for r in range(rows) for c in range(cols)}
    dist[start] = 0

    came_from = {}
    visited_order = []
    visited = set()

    # heap entries: (distance_so_far, node)
    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)

        if current in visited:
            continue  # stale entry, a shorter one was already processed
        visited.add(current)
        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            weight = 1  # uniform edge weight; swap in a cost grid for
                        # weighted terrain
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                came_from[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    return visited_order, reconstruct_path(came_from, start, end)


ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "dijkstra": dijkstra,
}