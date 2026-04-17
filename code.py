import heapq
import itertools
from collections import defaultdict


ROOM_CLUSTERS = {
    # Ground Floor
    'Block C L1 GF': ['G01', 'G03', 'G04', 'G06'],
    'Block C L2 GF': ['G07', 'G09', 'G10', 'G11'],
    'Main Block GF': ['G14', 'G15', 'G16'],
    'Block C R1 GF': ['G18', 'G19', 'G20', 'G21'],
    'Block C R2 GF': ['G23', 'G24', 'G25', 'G26'],
    'Block B GF': ['G31', 'G32', 'G33', 'G34', 'G35', 'G36', 'G37', 'G38', 'G39', 'G41'],
    'Block A GF': ['G43', 'G44', 'G48', 'G51', 'G52', 'G53', 'G54'],

    'Main Entrance': [115, 116],
    'Block D': [172, 173, 174, 175, 176],
    'Block C L1': [119, 120, 121, 122, 123, 124],
    'Block C L2': [125, 126, 127, 128, 129, 130, 131],
    'Block E': [132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145],
    'Block A': [146, 147, 150, 159],
    'CR1': [109, 110, 111, 112, 113],
    'CR2': [104, 105, 106, 107, 108],
    'Block F': ['F_WING'],
    'Block B': ['B_WING'],
    
    # 2nd Floor
    'Block C L1 F2': [219, 220, 221, 222],
    'Block C R2 F2': [202, 203, 205, 207, 208, 209, 210],
    'Block E F2': [228, 229, 230, 231, 232, 233, 234, 235, 238, 239, 242, 243, 244],
    'Block A F2': [241, 242, 243, 244, 247, 248, 249, 250, 251, 253, 254, 255, 256],
    'Block B F2': [258, 259, 260, 262, 263, 264, 265, 266, 267, 268, 269],
    'Main Area F2': [213, 214, 218],

    # 3rd Floor
    'Main Block F3': [312, 313, 314, 316],
    'Block F F3': [315],
    'Block C L1 F3': [310, 318, 319],
    'Block E-A F3': [307, 308, 309],
    'Block C R2 F3': [303, 304, 305, 306],
    'Block E F3': [325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 339, 341],
    'Block A F3': [342, 343, 344, 345, 346, 347, 348, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361],
    'Block B F3': [362, 363, 364, 365, 366, 367, 368, 369, 370],
    'Block D F3': [371, 372, 373, 374, 375, 376, 377, 378, 379],

    # 4th Floor
    'Block E F4': [422, 423, 424, 425, 426, 427, 428, 429, 430],
    'Block D F4': [464, 465, 466, 467, 468, 469, 471, 472],
    'Block A F4': [440, 441, 444, 445, 446, 447, 448, 449, 450, 454, 455],
    'Main Block F4': [411, 413],
    'Block B F4': [456, 457, 458, 459, 460, 461, 462, 463],

    # 5th Floor
    'Block D F5': [569, 571, 572, 573, 574, 575],
    'Block B F5': [560, 562, 563, 564, 565],
    'Block C L1 F5': [519, 520, 525, 578],
    'Block C L2 F5': [521, 522, 523, 524, 526, 529],
    'Block E F5': [527, 528, 530, 531, 532, 533, 534, 535, 545, 546, 547, 548, 549],

    # 6th Floor
    'Block C R1 F6': [605, 606, 607],
    'Block C L2 F6': [621, 622, 623, 624, 625, 628],
    'F-Block F6':    [611, 612, 613, 614],
    'Block A F6':    [641, 642, 646, 647, 648, 649, 650, 652, 653, 655, 656, 657, 659],
    'Block C R2 F6': [601, 603, 604, 608, 609],

    # 7th Floor
    'Block C R1 F7': [706, 707, 710, 711, 712, 713],
    'Block C L2 F7': [722, 723, 724, 725, 726, 727, 728],
    'Block C R2 F7': [701, 702, 703, 704, 705],
    'Block C L1 F7': [716, 717, 718, 719, 720, 721],
    'Main Block F7': ['714A', '714B', 715],
    'Block E F7': [729, 730, 731, 732, 733, 734, 735, 736, 739, 740, 741],
    'Block B F7': [759, 760, 762, 763, 764, 765],
    'Block D F7': [766, 767, 768, 769, 771, 772, 773],

    # Vertical transit nodes (per-floor, chained)
    'Stairs GF': ['Stairs_G'],
    'Stairs F1': ['Stairs_F1'],
    'Stairs F2': ['Stairs_F2'],
    'Stairs F3': ['Stairs_F3'],
    'Stairs F4': ['Stairs_F4'],
    'Stairs F5': ['Stairs_F5'],
    'Stairs F6': ['Stairs_F6'],
    'Stairs F7': ['Stairs_F7'],
    'Lift GF':   ['Lift_G'],
    'Lift F1':   ['Lift_F1'],
    'Lift F2':   ['Lift_F2'],
    'Lift F3':   ['Lift_F3'],
    'Lift F4':   ['Lift_F4'],
    'Lift F5':   ['Lift_F5'],
    'Lift F6':   ['Lift_F6'],
    'Lift F7':   ['Lift_F7'],
    'Canteen':   ['Canteen']
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
        # The Block C -> E 
        (115, 119, 2),        # Main to C L1 (start of C L1)
        (124, 125, 2),        # C L1 (end) to C L2 (start)
        (131, 132, 2),        # C L2 (end) to Block E (start)
        
        # The CR -> Main -> D 
        (116, 172, 3),        # Main to Block D
        (115, 113, 3),        # Main to CR1
        (109, 108, 1),        # CR1 to CR2 bridge
        (104, 146, 3),        # CR2 to Block A
        
        # Other Main Hub connections
        (115, 'F_WING', 2),
        (115, 'B_WING', 2),
        
        # Floor 2 connections
        (213, 219, 2),
        (222, 228, 3),
        (210, 202, 2),
        (244, 247, 2),
        (256, 258, 3),
        (218, 213, 1),
        
        # FLOOR G internal block connections
        ('G01', 'G03', 1), ('G03', 'G04', 1), ('G04', 'G06', 1),          # C L1 GF
        ('G07', 'G09', 1), ('G09', 'G10', 1), ('G10', 'G11', 1),          # C L2 GF
        ('G14', 'G15', 1), ('G15', 'G16', 1),                             # Main Block GF
        ('G18', 'G19', 1), ('G19', 'G20', 1), ('G20', 'G21', 1),          # C R1 GF
        ('G23', 'G24', 1), ('G24', 'G25', 1), ('G25', 'G26', 1),          # C R2 GF
        ('G31', 'G32', 1), ('G32', 'G33', 1), ('G33', 'G34', 1), 
        ('G34', 'G35', 1), ('G35', 'G36', 1), ('G36', 'G37', 1), 
        ('G37', 'G38', 1), ('G38', 'G39', 1), ('G39', 'G41', 1),          # Block B GF
        ('G43', 'G44', 1), ('G44', 'G48', 1), ('G48', 'G51', 1), 
        ('G51', 'G52', 1), ('G52', 'G53', 1), ('G53', 'G54', 1),          # Block A GF

        # FLOOR G inter-block connections
        ('G06', 'G07', 2),    # C L1 GF -> C L2 GF
        ('G21', 'G23', 2),    # C R1 GF -> C R2 GF
        ('G14', 'G01', 2),    # Main Block GF -> C L1 GF
        ('G15', 'G18', 2),    # Main Block GF -> C R1 GF
        ('G26', 'G43', 3),    # C R2 GF -> Block A GF
        ('G16', 'G31', 3),    # Main Block GF -> Block B GF

        # STAIRS: per-floor nodes chained GF->F1→F2→F3→F4→F5
        ('Stairs_G', 'Stairs_F1', 8),
        ('Stairs_F1', 'Stairs_F2', 8),
        ('Stairs_F2', 'Stairs_F3', 8),
        ('Stairs_F3', 'Stairs_F4', 8),
        ('Stairs_F4', 'Stairs_F5', 8),
        ('Stairs_F5', 'Stairs_F6', 8),
        ('Stairs_F6', 'Stairs_F7', 8),

        # GF rooms that touch stairs
        ('G51', 'Stairs_G', 2),
        ('G20', 'Stairs_G', 2),

        # F1 rooms that touch stairs
        (113, 'Stairs_F1', 2),

        # F2 rooms that touch stairs
        (219, 'Stairs_F2', 2),
        (242, 'Stairs_F2', 2),
        (244, 'Stairs_F2', 2),
        (208, 'Stairs_F2', 2),
        (213, 'Stairs_F2', 2),

        # F3 rooms that touch stairs
        (313, 'Stairs_F3', 2),
        (319, 'Stairs_F3', 2),
        (306, 'Stairs_F3', 2),
        (341, 'Stairs_F3', 2),
        (366, 'Stairs_F3', 2),
        (374, 'Stairs_F3', 2),

        # F4 rooms that touch stairs
        (422, 'Stairs_F4', 2),
        (430, 'Stairs_F4', 2),
        (469, 'Stairs_F4', 2),
        (463, 'Stairs_F4', 2),

        # LIFT: per-floor nodes chained GF->F1→F2→F3→F4→F5
        # Lift chain (each hop = 1 floor = 4 units)
        ('Lift_G', 'Lift_F1', 4),
        ('Lift_F1', 'Lift_F2', 4),
        ('Lift_F2', 'Lift_F3', 4),
        ('Lift_F3', 'Lift_F4', 4),
        ('Lift_F4', 'Lift_F5', 4),
        ('Lift_F5', 'Lift_F6', 4),
        ('Lift_F6', 'Lift_F7', 4),

        # GF rooms that touch lift
        ('G44', 'Lift_G', 1),
        ('G18', 'Lift_G', 1),

        # F1 rooms that touch lift
        (110, 'Lift_F1', 1),

        # F2 rooms that touch lift
        (244, 'Lift_F2', 1),
        (260, 'Lift_F2', 1),

        # F3 rooms that touch lift
        (312, 'Lift_F3', 1),
        (346, 'Lift_F3', 1),
        (339, 'Lift_F3', 1),
        (378, 'Lift_F3', 1),

        # F4 rooms that touch lift (mirrors F2: Block A area + Block B area + Main)
        (446, 'Lift_F4', 1),   # Block A F4
        (460, 'Lift_F4', 1),   # Block B F4
        (411, 'Lift_F4', 1),   # Main Block F4

        # ── FLOOR 3 internal block connections
        (312, 313, 1), (313, 314, 1), (314, 316, 1),  # Main Block F3
        (303, 304, 1), (304, 305, 1), (305, 306, 1),  # Block C R2 F3
        (307, 308, 1), (308, 309, 1),                 # Block E-A F3
        (310, 318, 1), (318, 319, 1),                 # Block C L1 F3

        # ── FLOOR 3 inter-block connections
        (313, 319, 2),
        (316, 315, 2),
        (319, 309, 3),
        (306, 312, 2),
        (309, 307, 1),
        (309, 'Canteen', 2),
        (327, 307, 2),    # E to E-A
        (342, 309, 2),    # A to E-A
        (361, 362, 3),    # A to B
        (370, 371, 3),    # B to D
        (379, 316, 3),    # D to Main
        (341, 327, 2),    # E internal loop
        (334, 339, 2),    # E internal loop

        # FLOOR 4 internal block connections
        (422, 423, 1), (423, 424, 1), (424, 425, 1), (425, 426, 1),
        (426, 427, 1), (427, 428, 1), (428, 429, 1), (429, 430, 1),
        (464, 465, 1), (465, 466, 1), (466, 467, 1), (467, 468, 1),
        (468, 469, 1), (469, 471, 2), (471, 472, 1),
        (440, 441, 1), (441, 444, 3), (444, 445, 1), (445, 446, 1),
        (446, 447, 1), (447, 448, 1), (448, 449, 1), (449, 450, 1),
        (450, 454, 2), (454, 455, 1),
        (411, 413, 2),
        (456, 457, 1), (457, 458, 1), (458, 459, 1), (459, 460, 1),
        (460, 461, 1), (461, 462, 1), (462, 463, 1),

        # FLOOR 4 inter-block connections
        (430, 422, 1),
        (472, 411, 3),
        (411, 446, 3),
        (455, 463, 2),
        (430, 469, 3),

        # 5 stairs/lift connections
        # F5 rooms that touch stairs
        (527, 'Stairs_F5', 2),   # Block E F5 entrance side
        (535, 'Stairs_F5', 2),   # Block E F5 far end
        (569, 'Stairs_F5', 2),   # Block D F5
        (562, 'Stairs_F5', 2),   # Block B F5

        # F4 rooms that touch stairs (bridge up to F5)
        (422, 'Stairs_F4', 2),
        (430, 'Stairs_F4', 2),
        (469, 'Stairs_F4', 2),
        (463, 'Stairs_F4', 2),

        # F5 rooms that touch lift
        (560, 'Lift_F5', 1),   # Block B F5
        (533, 'Lift_F5', 1),   # Block E F5 centre
        (571, 'Lift_F5', 1),   # Block D F5

        # FLOOR 5 internal block connections
        (519, 520, 1), (520, 525, 3), (525, 578, 3),          # Block C L1 F5
        (521, 522, 1), (522, 523, 1), (523, 524, 1),
        (524, 526, 2), (526, 529, 2),                          # Block C L2 F5
        (527, 528, 1), (528, 530, 2), (530, 531, 1),
        (531, 532, 1), (532, 533, 1), (533, 534, 1),
        (534, 535, 1), (535, 545, 2), (545, 546, 1),
        (546, 547, 1), (547, 548, 1), (548, 549, 1),           # Block E F5
        (560, 562, 2), (562, 563, 1), (563, 564, 1),
        (564, 565, 1),                                          # Block B F5
        (569, 571, 2), (571, 572, 1), (572, 573, 1),
        (573, 574, 1), (574, 575, 1),                          # Block D F5

        # FLOOR 5 inter-block connections 
        (525, 523, 2),    # Block C L1 F5 -> Block C L2 F5
        (523, 535, 3),    # Block C L2 F5 -> Block E F5
        (529, 527, 2),    # Block C L2 F5 -> Block E F5 (alt)
        (565, 560, 2),    # Block B F5 internal wrap
        (565, 575, 2),    # Block B F5 -> Block D F5
        (549, 535, 1),    # Block E F5 loop

        # FLOOR 6 stairs/lift connections 
        # F6 rooms that touch stairs
        (605, 'Stairs_F6', 2),   # Block C R1 F6
        (621, 'Stairs_F6', 2),   # Block C L2 F6 entrance
        (611, 'Stairs_F6', 2),   # F-Block F6

        # F5 rooms that touch stairs (bridge up to F6)
        (527, 'Stairs_F5', 2),
        (535, 'Stairs_F5', 2),
        (569, 'Stairs_F5', 2),
        (562, 'Stairs_F5', 2),

        # F6 rooms that touch lift
        (624, 'Lift_F6', 1),   # Block C L2 F6 (lift marked)
        (607, 'Lift_F6', 1),   # Block C R1 F6
        (641, 'Lift_F6', 1),   # Block A F6
        (659, 'Lift_F6', 1),   # Block A F6 far end

        # FLOOR 6 internal block connections
        (605, 606, 1), (606, 607, 1),                                  # Block C R1 F6
        (621, 622, 1), (622, 623, 1), (623, 624, 1),
        (624, 625, 1), (625, 628, 2),                                  # Block C L2 F6
        (611, 612, 1), (612, 613, 1), (613, 614, 1),                  # F-Block F6
        (641, 642, 1), (642, 646, 3), (646, 647, 1), (647, 648, 1),
        (648, 649, 1), (649, 650, 2), (650, 652, 2), (652, 653, 1),
        (653, 655, 2), (655, 656, 1), (656, 657, 1), (657, 659, 2),  # Block A F6
        (601, 603, 2), (603, 604, 1), (604, 608, 2), (608, 609, 1),  # Block C R2 F6

        # FLOOR 6 inter-block connections
        (607, 601, 2),    # Block C R1 F6 -> Block C R2 F6 (R2 direction arrow)
        (628, 641, 3),    # Block C L2 F6 -> Block A F6
        (614, 641, 3),    # F-Block F6 -> Block A F6
        (609, 605, 2),    # Block C R2 F6 -> Block C R1 F6 (loop)

        # FLOOR 7 stairs/lift connections
        # F7 rooms that touch stairs
        (707, 'Stairs_F7', 2),   # Block C R1 F7
        (722, 'Stairs_F7', 2),   # Block C L2 F7 (entrance side)
        (760, 'Stairs_F7', 2),   # Block B F7
        (739, 'Stairs_F7', 2),   # Block E F7 stairs 1
        (741, 'Stairs_F7', 2),   # Block E F7 stairs 2

        # F6 rooms that touch stairs (bridge up to F7)
        (605, 'Stairs_F6', 2),
        (621, 'Stairs_F6', 2),
        (641, 'Stairs_F6', 2),   

        # F7 rooms that touch lift
        (713, 'Lift_F7', 1),   # Block C R1 F7
        (727, 'Lift_F7', 1),   # Block C L2 F7
        (702, 'Lift_F7', 1),   # Block C R2 F7
        (741, 'Lift_F7', 1),   # Block E F7
        (762, 'Lift_F7', 1),   # Block B F7
        (769, 'Lift_F7', 1),   # Block D F7

        # FLOOR 7 internal block connections
        (701, 702, 1), (702, 703, 1), (703, 704, 1), (704, 705, 1),        # Block C R2 F7
        (722, 723, 1), (723, 724, 1), (724, 725, 1), (725, 726, 1),
        (726, 727, 1), (727, 728, 1),                                      # Block C L2 F7
        (706, 707, 1), (707, 710, 1), (710, 711, 1), (711, 712, 1),
        (712, 713, 1),                                                     # Block C R1 F7
        (716, 717, 2), (717, 718, 1), (718, 719, 1), (719, 720, 1),
        (720, 721, 1),                                                     # Block C L1 F7
        ('714A', '714B', 1), ('714B', 715, 2),                             # Main Block F7
        (729, 730, 1), (730, 731, 1), (731, 732, 1), (731, 733, 2),
        (732, 734, 1), (734, 735, 1), (735, 736, 1), (739, 740, 2),
        (740, 741, 1), (729, 741, 3), (736, 739, 3),                       # Block E F7
        (759, 760, 1), (760, 762, 2), (762, 763, 1), (763, 764, 1),
        (764, 765, 1),                                                     # Block B F7
        (766, 767, 1), (767, 768, 1), (768, 769, 1), (769, 771, 1),
        (771, 772, 1), (772, 773, 1),                                      # Block D F7

        # FLOOR 7 inter-block connections
        (701, 706, 2),    # Block C R2 -> Block C R1
        (722, 721, 2),    # Block C L2 -> Block C L1
        (715, 716, 3),    # Main Block -> Block C L1
        (715, 705, 3),    # Main Block -> Block C R2
        (728, 729, 3),    # Block C L2 -> Block E
        (736, 759, 3),    # Block E -> Block B
        (765, 766, 2)     # Block B -> Block D
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
    print("      PRP CAMPUS NAVIGATION SYSTEM")
    print("-" * 50)

    while True:
        print("OPTIONS:")
        print("1. Find Route")
        print("2. View Blocks")
        print("3. Exit")
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

                display_steps = []
                i = 0
                while i < len(path):
                    node = path[i]
                    if isinstance(node, str) and node.startswith('Lift_'):
                        #To collect all consecutive Lift nodes
                        lift_nodes = []
                        while i < len(path) and isinstance(path[i], str) and path[i].startswith('Lift_'):
                            lift_nodes.append(path[i])
                            i += 1
                        from_floor = lift_nodes[0].split('_')[1]
                        to_floor   = lift_nodes[-1].split('_')[1]
                        if from_floor == to_floor:
                            display_steps.append(('transit', f'Take Lift (stay on {to_floor})'))
                        else:
                            display_steps.append(('transit', f'Take Lift: {from_floor} → {to_floor}'))
                    elif isinstance(node, str) and node.startswith('Stairs_'):
                        # Collect all consecutive Stairs nodes
                        stair_nodes = []
                        while i < len(path) and isinstance(path[i], str) and path[i].startswith('Stairs_'):
                            stair_nodes.append(path[i])
                            i += 1
                        from_floor = stair_nodes[0].split('_')[1]
                        to_floor   = stair_nodes[-1].split('_')[1]
                        if from_floor == to_floor:
                            display_steps.append(('transit', f'Use Stairs (stay on {to_floor})'))
                        else:
                            display_steps.append(('transit', f'Use Stairs: {from_floor} → {to_floor}'))
                    else:
                        display_steps.append(('room', node))
                        i += 1

                last_block = None
                step_num = 1
                for kind, value in display_steps:
                    if kind == 'transit':
                        print(f"\n  🔼 {value}")
                    else:
                        current_block = identify_block(value)
                        if current_block != last_block:
                            print(f"\n[ Entering {current_block} ]")
                            last_block = current_block
                        print(f" Step {step_num}: {value}")
                        step_num += 1
            else:
                print("No path exists.")

if __name__ == "__main__":
    main()