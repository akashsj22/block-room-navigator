import heapq
from collections import defaultdict

def room_to_pos(floor, room):
    local = room - floor * 100 - 1
    row = local // 10
    col = local % 10
    return row, col

def get_room(floor, row, col):
    return floor * 100 + row * 10 + col + 1

def get_direction(curr, nxt):
    cf, cr, cc = curr
    nf, nr, nc = nxt
    if cf != nf:
        if (cr, cc) in elevator_positions:
            return f"Take elevator to floor {nf}"
        else:
            return f"Take stairs {'up' if nf > cf else 'down'} to floor {nf}"
    dr = nr - cr
    dc = nc - cc
    if abs(dr) + abs(dc) > 1:
        return "Continue straight"
    if dr == 1:
        return "Go south"
    elif dr == -1:
        return "Go north"
    elif dc == 1:
        return "Go east"
    elif dc == -1:
        return "Go west"
    return ""

def dijkstra(graph, start, end):
    queue = [(0, start)]
    dist = {start: 0}
    prev = {start: None}
    while queue:
        d, u = heapq.heappop(queue)
        if u == end:
            break
        if d > dist.get(u, float('inf')):
            continue
        for v, weight in graph[u].items():
            alt = d + weight
            if alt < dist.get(v, float('inf')):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(queue, (alt, v))
    if end not in dist:
        return None
    path = []
    u = end
    while u is not None:
        path.append(u)
        u = prev.get(u)
    return path[::-1]

num_floors = 5
grid_size = 10
graph = defaultdict(dict)
stair_positions = [(0, 0), (0, 5), (5, 0), (5, 5), (9, 0), (9, 5)]
elevator_positions = [(0, 9), (9, 9)]

for floor in range(1, num_floors + 1):
    for r in range(grid_size):
        for c in range(1, grid_size):
            node1 = (floor, r, c - 1)
            node2 = (floor, r, c)
            weight = 1 if abs(c - (c-1)) == 1 else 1.5
            graph[node1][node2] = weight
            graph[node2][node1] = weight
    for c in range(grid_size):
        for r in range(1, grid_size):
            node1 = (floor, r - 1, c)
            node2 = (floor, r, c)
            weight = 1 if abs(r - (r-1)) == 1 else 1.5
            graph[node1][node2] = weight
            graph[node2][node1] = weight

for floor in range(1, num_floors):
    for r, c in stair_positions:
        node1 = (floor, r, c)
        node2 = (floor + 1, r, c)
        graph[node1][node2] = 10
        graph[node2][node1] = 10
    for r, c in elevator_positions:
        node1 = (floor, r, c)
        node2 = (floor + 1, r, c)
        graph[node1][node2] = 5
        graph[node2][node1] = 5

start_floor = int(input("Start floor: "))
start_room = int(input("Start room: "))
end_floor = int(input("End floor: "))
end_room = int(input("End room: "))

start_node = (start_floor,) + room_to_pos(start_floor, start_room)
end_node = (end_floor,) + room_to_pos(end_floor, end_room)

path = dijkstra(graph, start_node, end_node)

if path is None:
    print("No path found.")
else:
    print("Path:")
    for node in path:
        f, r, c = node
        room = get_room(f, r, c)
        print(f"Floor {f}, Room {room}")
    print("\nDirections:")
    prev_dir = ""
    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i + 1]
        curr_room = get_room(curr[0], curr[1], curr[2])
        direction = get_direction(curr, nxt)
        if direction == "Continue straight" and prev_dir:
            continue
        print(f"From Floor {curr[0]}, Room {curr_room}: {direction}")
        prev_dir = direction if direction != "Continue straight" else prev_dir