import pqueue

def manhattan_dist(a, b):
    """
    Returns the Manhattan distance between two points.

    >>> manhattan_dist((0, 0), (5, 5))
    10
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(neighbour_fn, start, end, passable):
    """
    Returns a list of points between 2 points using A*.
    If no path can be found, an empty list is returned.

    The cost function shows how much it cost to take a step. F(x) = g(x) + h(x)
    should always be greater than 1 or else the shortest path is not guaranteed.

    The passable function returns whether or not the agent can pass through the node.

    The heuristic function uses the manhattan distance for a quick and guarantee
    esitamte of the optimal path cost.
    """
    cost = 1
    costs = 0
    # tiles to check (tuples of (x, y), cost)
    frontier = pqueue.PQueue()
    frontier.update(start, 0)

    # tiles we've been to
    visited = set()

    # associated G and H costs for each tile (tuples of G, H)
    if(not costs):
        costs = { start: (0, manhattan_dist(start, end)) }

    # parents for each tile
    parents = {}

    while (frontier and (end not in visited)):
        cur, c = frontier.pop_smallest()

        visited.add(cur)

        # check neighbours
        for n in neighbour_fn(cur):
            # skip it if we've already checked it, or if it isn't passable
            if ((n in visited) or
                (not passable(n, None))):
                continue

            if not (n in frontier):
                # we haven't looked at this tile yet, so calculate its costs
                g = costs[cur][0] + cost
                h = manhattan_dist(n, end)
                costs[n] = (g, h)
                parents[n] = cur
                frontier.update(n, g + h)
            else:
                # if we've found a better path, update it
                g, h = costs[n]
                new_g = costs[cur][0] + cost
                if new_g < g:
                    g = new_g
                    frontier.update(n, g + h)
                    costs[n] = (g, h)
                    parents[n] = cur

    # we didn't find a path
    if end not in visited:
        return []

    # build the path backward
    path = []
    while end != start:
        path.append(end)
        end = parents[end]
    path.append(start)
    path.reverse()

    return path, (len(path) - 1)
