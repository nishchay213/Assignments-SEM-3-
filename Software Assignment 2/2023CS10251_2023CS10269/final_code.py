import random
import math
import time
import sys

sys.setrecursionlimit(1000000)
gate_dict = {}
#nishchay_23

class GatePacker:
    def __init__(self, tries=1):
        self.tries = tries

    def arranging(self, box, gatesnew):
        packing = []
        for name, width, height in gatesnew:
            position = box.add(width, height)
            if position is None:
                return None
            packing.append((name, position[0], position[1]))
        return packing

    def pack_gates(self, gates):
        gatesnew = sorted(gates, key=lambda g: g[1], reverse=True)
        totalarea = sum(h * w for _, w, h in gatesnew)
        maxw = gatesnew[0][1]
        maxh = max(h for _, w, h in gatesnew)
        minh = min(h for _, w, h in gatesnew)
        best_box = None
        box_width = maxw
        box_height = maxh
        boxes = 0
        while boxes < self.tries:
            box = algo1(box_width, box_height)
            current = self.arranging(box, gatesnew)
            if current is None:
                box_width += min(gatesnew[-1][1], minh)
                box_height += min(gatesnew[-1][1], minh)
            else:
                curr_width, curr_height = box.getmax()
                curr = totalarea / (curr_width * curr_height)
                if best_box is None or curr_width * curr_height < best_box['area']:
                    best_box = {'area': curr_width * curr_height, 'width': curr_width, 'height': curr_height,
                                'packing': current}
                    if curr >= 1.0:
                        break
                box_width = curr_width
                box_height = curr_height
                boxes += 1
        return best_box


class algo1:
    def __init__(self, boxw, boxh):
        self.boxw = int(boxw)
        self.boxh = int(boxh)
        self.valid = [[False] * self.boxh for _ in range(self.boxw)]

    def add(self, width, height):
        for i in range(self.boxw - width + 1):
            for j in range(self.boxh - height + 1):
                if self.place(i, j, width, height):
                    self.poss(i, j, width, height)
                    return (i, j)
        return None

    def place(self, x, y, width, height):
        for i in range(x, x + width):
            for j in range(y, y + height):
                if self.valid[i][j]:
                    return False
        return True

    def poss(self, x, y, width, height):
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.valid[i][j] = True

    def getmax(self):
        maxw = maxh = 0
        for i in range(self.boxw):
            for j in range(self.boxh):
                if self.valid[i][j]:
                    maxw = max(maxw, i + 1)
                    maxh = max(maxh, j + 1)
        return maxw, maxh


class GatePlacer:
    def __init__(self):
        self.root = None

    def locate_space(self, curr_space, width, height):
        if curr_space['used']:
            return self.locate_space(curr_space['right'], width, height) or \
                self.locate_space(curr_space['top'], width, height)
        elif width <= curr_space['w'] and height <= curr_space['h']:
            return curr_space
        else:
            return None

    def divide_space(self, space, width, height):
        space['used'] = True
        space['top'] = {'x': space['x'], 'y': space['y'] + height, 'w': space['w'], 'h': space['h'] - height,
                        'used': False, 'right': None, 'top': None}
        space['right'] = {'x': space['x'] + width, 'y': space['y'], 'w': space['w'] - width, 'h': height, 'used': False,
                          'right': None, 'top': None}
        return space

    def expand_top(self, width, height):
        self.root = {
            'used': True, 'x': 0, 'y': 0, 'w': self.root['w'], 'h': self.root['h'] + height, 'right': self.root,
            'top': {'x': 0, 'y': self.root['h'], 'w': self.root['w'], 'h': height, 'used': False, 'right': None,
                    'top': None}
        }
        space = self.locate_space(self.root, width, height)
        return self.divide_space(space, width, height) if space else None

    def expand_right(self, width, height):
        self.root = {
            'used': True, 'x': 0, 'y': 0, 'w': self.root['w'] + width, 'h': self.root['h'], 'top': self.root,
            'right': {'x': self.root['w'], 'y': 0, 'w': width, 'h': self.root['h'], 'used': False, 'right': None,
                      'top': None}
        }
        space = self.locate_space(self.root, width, height)
        return self.divide_space(space, width, height) if space else None

    def expand_space(self, width, height):
        can_expand_top = width <= self.root['w']
        can_expand_right = height <= self.root['h']
        should_expand_right = can_expand_right and (self.root['h'] >= self.root['w'] + width)
        should_expand_top = can_expand_top and (self.root['w'] >= self.root['h'] + height)
        if should_expand_right:
            return self.expand_right(width, height)
        elif should_expand_top:
            return self.expand_top(width, height)
        elif can_expand_right:
            return self.expand_right(width, height)
        elif can_expand_top:
            return self.expand_top(width, height)
        else:
            return None

    def place_gates(self, gates):
        if not gates:
            return
        # Initialize the root with the first block's dimensions
        width, height = gates[0][1], gates[0][2]
        self.root = {'x': 0, 'y': 0, 'w': width, 'h': height, 'used': False, 'right': None, 'top': None}
        # Process each block
        for i, gate in enumerate(gates):
            name, w, h = gate[:3]
            space = self.locate_space(self.root, w, h)
            if space:
                fit_gate = self.divide_space(space, w, h)
                gates[i] = (name, w, h, fit_gate['x'], fit_gate['y'])
            else:
                fit_gate = self.expand_space(w, h)
                if fit_gate:
                    gates[i] = (name, w, h, fit_gate['x'], fit_gate['y'])
                else:
                    gates[i] = (name, w, h, None, None)


def run_algo2sort2(input_data):
    # input_data.sort(key=lambda x: (x[2], x[1]), reverse=True)
    placer = GatePlacer()
    placer.place_gates(input_data)

    if placer.root:
        total_area = sum(w * h for _, w, h, *_ in input_data)
        bounding_box_area = placer.root['w'] * placer.root['h']
        efficiency = (total_area / bounding_box_area) * 100
        bounding_box = (placer.root['w'], placer.root['h'])
        packing_data = [(name, x, y) for name, _, _, x, y in input_data if x is not None]
    else:
        efficiency = 0
        bounding_box = (0, 0)
        packing_data = []

    return bounding_box, packing_data, efficiency


class Gate:
    def __init__(self, name, width, height, pins):
        self.name = name
        self.width = width
        self.height = height
        self.pins = pins  # List of pin (x, y) coordinates relative to the gate's bottom-left corner


class Wire:
    def __init__(self, gate1, pin1, gate2, pin2):
        self.gate1 = gate1  # Gate object
        self.pin1 = pin1  # Pin index on gate1
        self.gate2 = gate2  # Gate object
        self.pin2 = pin2  # Pin index on gate2


def wire_length_cluster(wires, positions):
    pin_connections = {}
    pin_positions = {}

    for wire in wires:
        pin1_id = (wire.gate1.name, wire.pin1)
        pin2_id = (wire.gate2.name, wire.pin2)

        gate1_pos = positions[wire.gate1]
        gate2_pos = positions[wire.gate2]
        pin1_pos = (gate1_pos[0] + wire.gate1.pins[wire.pin1][0], gate1_pos[1] + wire.gate1.pins[wire.pin1][1])
        pin2_pos = (gate2_pos[0] + wire.gate2.pins[wire.pin2][0], gate2_pos[1] + wire.gate2.pins[wire.pin2][1])

        pin_positions[pin1_id] = pin1_pos
        pin_positions[pin2_id] = pin2_pos

        if pin1_id not in pin_connections:
            pin_connections[pin1_id] = []

        pin_connections[pin1_id].append(pin2_id)

    total_length = 0
    for pin, connected in pin_connections.items():
        pin_x, pin_y = pin_positions[pin][0], pin_positions[pin][1]
        maxx, minx = pin_x, pin_x
        maxy, miny = pin_y, pin_y
        for connected_pin in connected:
            pin2_x, pin2_y = pin_positions[connected_pin][0], pin_positions[connected_pin][1]
            maxx = max(maxx, pin_x, pin2_x)
            maxy = max(maxy, pin_y, pin2_y)
            minx = min(minx, pin_x, pin2_x)
            miny = min(miny, pin_y, pin2_y)
        total_length += maxx + maxy - minx - miny
        # semi perimeter of the bounding box created by one pin

    def dfs(node, visited, component):
        visited.add(node)
        component.append(node)
        for neighbor in pin_connections.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, visited, component)

    # visited = set()
    # components = []
    # for pin_id in graph:
    #     if pin_id not in visited:
    #         component = []
    #         dfs(pin_id, visited, component)
    #         components.append(component)
    #
    # total_length = 0
    # for component in components:
    #     min_x = min(pin_positions[pin_id][0] for pin_id in component)
    #     max_x = max(pin_positions[pin_id][0] for pin_id in component)
    #     min_y = min(pin_positions[pin_id][1] for pin_id in component)
    #     max_y = max(pin_positions[pin_id][1] for pin_id in component)
    #     semi_perimeter = (max_x - min_x) + (max_y - min_y)
    #     total_length += semi_perimeter

    return total_length


def form_gate_clusters(wires):
    connected = {}
    for wire in wires:
        if wire.gate1 not in connected:
            connected[wire.gate1] = []
        if wire.gate2 not in connected:
            connected[wire.gate2] = []
        connected[wire.gate1].append(wire.gate2)
        connected[wire.gate2].append(wire.gate1)

    def dfs(gate, visited, cluster):
        visited.add(gate)
        cluster.append(gate)
        for neighbor in connected[gate]:
            if neighbor not in visited:
                dfs(neighbor, visited, cluster)

    visited = set()
    clusters = []
    for gate in connected:
        if gate not in visited:
            cluster = []
            dfs(gate, visited, cluster)
            clusters.append(cluster)
    return clusters


def initial_placements_by_sw1(gates, clusters):
    placements = {}
    x_box = 10
    visited = set()
    for cluster in clusters:
        # Prepare the input data for the algorithm
        gate_data = [(gate.name, gate.width, gate.height) for gate in cluster]

        # Run the packing algorithm
        # bounding_box, packing_data, _ = run_algo2sort2(input_data)
        if len(gate_data) < 100:
            packer = GatePacker(tries=5)
            packing_result = packer.pack_gates(gate_data)
            bounding_box = packing_result['width'], packing_result['height']
            packing_data = packing_result['packing']
        else:
            bounding_box, packing_data, _ = run_algo2sort2(gate_data)

        # Place gates based on the algorithm's result, using Gate objects as keys
        for name, x, y in packing_data:
            gate_object = gate_dict[name]  # Get the Gate object from gate_dict using its name
            placements[gate_object] = (x + x_box, y)  # Use the Gate object as the key
            visited.add(name)
        x_box += bounding_box[0] + 10  # Increment the position of bounding box for no overlap

    for gate in gates:
        if gate.name not in visited:
            placements[gate] = (x_box, 0)
            x_box += gate.width + 10

    return placements


# Function to process the input file and extract gates and connections
def process_input(file_content):
    # Split input content into lines and initialize lists for gates and connections
    lines = file_content.strip().split("\n")
    gates = []
    wires = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Process lines starting with 'g' (gates)
        if line.lower().startswith("g"):
            gate_name, width, height, pins = parse_gate_line(line, lines[i + 1].strip())
            gate = Gate(gate_name, width, height, pins)
            gates.append(gate)
            gate_dict[gate_name] = gate
            i += 1  # Skip to the next line after processing pins
        # Process lines that describe a wire connection
        elif line.lower().startswith("wire"):
            g1, p1, g2, p2 = parse_wire_line(line)
            wire = Wire(gate_dict[g1], int(p1) - 1, gate_dict[g2], int(p2) - 1)
            # to maintain index that's why did int(p1)-1
            wires.append(wire)
        i += 1  # Move to the next line
    return gates, wires


def parse_gate_line(gate_line, pin_line):
    parts = gate_line.split()
    gate_name = parts[0]
    width = int(parts[1])
    height = int(parts[2])
    # Extract pin coordinates from the following line
    pin_parts = pin_line.split()[2:]
    pins = [(int(pin_parts[i]), int(pin_parts[i + 1])) for i in range(0, len(pin_parts), 2)]
    # because there's x coordinate and y coordinate
    return gate_name, width, height, pins


def parse_wire_line(wire_line):
    parts = wire_line.split()
    g1, p1 = parts[1].split(".")
    g2, p2 = parts[2].split(".")
    return g1, p1[1], g2, p2[1]


def write_output(best_solution, best_cost):
    box_height = max(y + gate.height for gate, (x, y) in best_solution.items())
    box_width = max(x + gate.width for gate, (x, y) in best_solution.items())
    output = f"bounding_box {box_width} {box_height}\n"
    for gate, (x, y) in best_solution.items():
        output += f"{gate.name} {x} {y}\n"
    output += f"wire_length {best_cost}\n"
    print(best_cost)
    # prints the wire length
    return output


def check_overlap(positions, gate, new_x, new_y):
    for diff_gate, (x, y) in positions.items():
        if diff_gate != gate:
            if not (
                    new_x + gate.width <= x or new_x >= x + diff_gate.width or new_y + gate.height <= y or new_y >= y + diff_gate.height):
                return True  # Overlap detected
    return False  # No overlap


# def initial_placement(gates, grid_spacing=20, bounding_box_size=100):
#     placements = {}
#     x_offset, y_offset = 0, 0
#     max_height_in_row = 0
#
#     for gate in gates:
#         while True:
#             if x_offset + gate.width > bounding_box_size:
#                 x_offset = 0
#                 y_offset += max_height_in_row + grid_spacing
#                 max_height_in_row = 0
#
#             new_position = (x_offset, y_offset)
#
#             if not check_overlap(placements, gate, x_offset, y_offset):
#                 placements[gate] = new_position
#                 x_offset += gate.width + grid_spacing
#                 max_height_in_row = max(max_height_in_row, gate.height)
#                 break
#
#     return placements
#
# import random

def initial_placement(gates, min_spacing=2, max_spacing=10, bounding_box_size=100):
    placements = {}
    x, y = 0, 0
    max_height_in_row = 0

    for gate in gates:
        while True:
            # Ensure the gate fits within the bounding box width
            if x + gate.width > bounding_box_size:
                x = 0
                y += max_height_in_row + random.randint(min_spacing, max_spacing)
                max_height_in_row = 0

            # Randomize placement within a small range to avoid overly rigid grid alignment
            random_x = x + random.randint(0, 5)
            random_y = y + random.randint(0, 5)

            if not check_overlap(placements, gate, random_x, random_y):
                placements[gate] = (random_x, random_y)
                x += gate.width + random.randint(min_spacing, max_spacing)
                max_height_in_row = max(max_height_in_row, gate.height)
                break

    return placements


def simulated_annealing(gates, wires, max_iterations=10000, initial_temp=1000, cooling_rate=0.95):
    # clusters = form_gate_clusters(wires)
    current_placement = initial_placement(gates)
    current_length = wire_length_cluster(wires, current_placement)
    best_placement = current_placement.copy()
    best_length = current_length
    temperature = initial_temp
    if len(gates) > 500:
        max_iterations = 1000
    elif len(gates) <=50:
        max_iterations = 100000
    for iteration in range(max_iterations):
        gate_to_move = random.choice(gates)
        gate_name = gate_to_move.name
        new_placement = current_placement.copy()
        new_x = new_placement[gate_dict[gate_name]][0] + random.randint(-5, 5)
        new_y = new_placement[gate_dict[gate_name]][1] + random.randint(-5, 5)
        if new_x < 0 or new_y < 0:
            continue
        if not check_overlap(new_placement, gate_to_move, new_x, new_y):
            new_placement[gate_to_move] = (new_x, new_y)
        else:
            continue
        new_length = wire_length_cluster(wires, new_placement)
        # Acceptance criteria (Simulated Annealing)
        if new_length - current_length < 0 or random.random() < math.exp(-(new_length - current_length) / temperature):
            current_placement = new_placement
            current_length = new_length

        # Update best placement
        if current_length < best_length:
            best_placement = current_placement.copy()
            best_length = current_length
        # Cool down the temperature
        temperature *= cooling_rate

    return best_placement, best_length


def simulated_annealing_by_initial_placement(gates, connections, max_iterations=10000, initial_temp=1000,
                                             cooling_rate=0.95):
    components = form_gate_clusters(connections)
    current_placement = initial_placements_by_sw1(gates, components)
    current_length = wire_length_cluster(connections, current_placement)
    best_placement = current_placement.copy()
    best_length = current_length
    temperature = initial_temp
    if len(gates) > 500:
        max_iterations = 1000
    elif len(gates) <=50:
        max_iterations = 100000
    for iteration in range(max_iterations):
        gate_to_move = random.choice(gates)
        gate_name = gate_to_move.name
        new_placement = current_placement.copy()
        new_x = new_placement[gate_dict[gate_name]][0] + random.randint(-5, 5)
        new_y = new_placement[gate_dict[gate_name]][1] + random.randint(-5, 5)
        if new_x < 0 or new_y < 0:
            continue
        if not check_overlap(new_placement, gate_to_move, new_x, new_y):
            new_placement[gate_to_move] = (new_x, new_y)
        else:
            continue
        new_length = wire_length_cluster(connections, new_placement)
        # Acceptance criteria (Simulated Annealing)
        if new_length - current_length < 0 or random.random() < math.exp(-(new_length - current_length) / temperature):
            current_placement = new_placement
            current_length = new_length
        # Update best placement
        if current_length < best_length:
            best_placement = current_placement.copy()
            best_length = current_length
        # Cool down the temperature
        temperature *= cooling_rate
    return best_placement, best_length


def main(input_file, output_file):
    # Read from the input file
    start_time = time.time()
    with open(input_file, "r") as file:
        file_content = file.read()

    gates, wires = process_input(file_content)
    best_placement, best_length = simulated_annealing_by_initial_placement(gates, wires)

    # Run simulated annealing to find the best placement
    if len(gates) <= 50:
        for i in range(10):
            temp_placement, temp_length = simulated_annealing(gates, wires)
            if temp_length < best_length:
                best_placement = temp_placement
                best_length = temp_length

    for i in range(10):
        temp_placement, temp_length = simulated_annealing_by_initial_placement(gates, wires)
        if temp_length < best_length:
            best_placement = temp_placement
            best_length = temp_length
    # Write the output
    output = write_output(best_placement, best_length)
    # Write to the output file
    with open(output_file, "w") as file:
        file.write(output)
    print("--- %s seconds ---" % (time.time() - start_time))


# Run the program with input from 'input.txt' and write the result to 'output.txt'
if __name__ == "__main__":
    main("input.txt", "output.txt")