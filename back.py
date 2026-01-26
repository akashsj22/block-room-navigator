import heapq
import itertools
from collections import defaultdict


ROOM_CLUSTERS = {
    'Main Entrance': [115, 116],
    'Block D': [172, 173, 174, 175, 176],
    'Block C L1': [119, 120, 121, 122, 123, 124],
    'Block C L2': [125, 126, 127, 128, 129, 130, 131],
    'Block E': [132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145],
    'Block A': [146, 147, 150, 159],
    'CR1': [109, 110, 111, 112, 113],
    'CR2': [104, 105, 106, 107, 108],
    'Block F': ['F_WING'],
    'Block B': ['B_WING']
}

def build_building_graph():
    graph = defaultdict(dict)
    
    # 1. Internal connections: Rooms within the same block
    for block, rooms in ROOM_CLUSTERS.items():
        numeric_rooms = sorted([r for r in rooms if isinstance(r, int)])
        for i in range(len(numeric_rooms) - 1):
            u, v = numeric_rooms[i], numeric_rooms[i+1]
            graph[u][v] = 1
            graph[v][u] = 1

  
    connections = [
        # The Block C -> E Chain
        (115, 119, 2),        # Main to C L1 (start of C L1)
        (124, 125, 2),        # C L1 (end) to C L2 (start)
        (131, 132, 2),        # C L2 (end) to Block E (start)
        
        # The CR -> Main -> D Chain
        (116, 172, 3),        # Main to Block D
        (115, 113, 3),        # Main to CR1
        (109, 108, 1),        # CR1 to CR2 bridge
        (104, 146, 3),        # CR2 to Block A
        
        # Other Main Hub connections
        (115, 'F_WING', 2),
        (115, 'B_WING', 2)
    ]
    
    for u, v, w in connections:
        graph[u][v] = w
        graph[v][u] = w
        
    return graph


def get_shortest_path(graph, start, end):
    counter = itertools.count()
    queue = [(0, next(counter), start)]
    distances = {start: 0}
    previous = {start: None}

    while queue:
        current_dist, _, u = heapq.heappop(queue)

        if u == end:
            break

        if current_dist > distances.get(u, float('inf')):
            continue

        if u in graph:
            for v, weight in graph[u].items():
                new_dist = current_dist + weight
                if new_dist < distances.get(v, float('inf')):
                    distances[v] = new_dist
                    previous[v] = u
                    heapq.heappush(queue, (new_dist, next(counter), v))

    if end not in distances:
        return None, 0

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = previous.get(curr)
        
    return path[::-1], distances[end]


def identify_block(room_node):
    for block_name, rooms in ROOM_CLUSTERS.items():
        if room_node in rooms:
            return block_name
    return "Transition Area"

def validate_room(room_node):
    for rooms in ROOM_CLUSTERS.values():
        if room_node in rooms:
            return True
    return False


def main():
    building_graph = build_building_graph()
    
    print("-" * 50)
    print("      PRP CAMPUS NAVIGATION SYSTEM - V3.4")
    print("-" * 50)

    while True:
        print("\nOPTIONS: 1. Find Route | 2. View Blocks | 3. Exit")
        user_choice = input("Action: ")

        if user_choice == '3':
            break

        if user_choice == '2':
            for b in ROOM_CLUSTERS.keys(): print(f"- {b}")
            continue

        if user_choice == '1':
            start_in = input("Enter current room: ")
            end_in = input("Enter target room: ")

            start = int(start_in) if start_in.isdigit() else start_in
            end = int(end_in) if end_in.isdigit() else end_in

            if not validate_room(start) or not validate_room(end):
                print("Error: Room not found.")
                continue

            path, total_weight = get_shortest_path(building_graph, start, end)

            if path:
                print("\n" + "="*40)
                print(f"PATH: {start} to {end}")
                print(f"Total Movement Units: {total_weight}")
                print("="*40)

                last_block = None
                for i, node in enumerate(path):
                    current_block = identify_block(node)
                    if current_block != last_block:
                        print(f"\n[ Entering {current_block} ]")
                        last_block = current_block
                    print(f" Step {i+1}: {node}")
            else:
                print("No path exists.")

if __name__ == "__main__":
    main()