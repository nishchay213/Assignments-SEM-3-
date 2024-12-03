import random
import math
import time
import sys

#nishchay213

sys.setrecursionlimit(10000)
gate_dict = {}
pin_conn = {}
gates = []
wires = []
wire_delay = 0
primary_outputs = []
primary_inputs = []


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
    def __init__(self, name, width, height, delay, pins):
        self.name = name
        self.width = width
        self.height = height
        self.delay = delay
        self.pins = pins  # List of pin (x, y) coordinates relative to the gate's bottom-left corner
        self.input_pins = []
        self.output_pins = []


class Wire:
    def __init__(self, gate1, pin1, gate2, pin2):
        self.gate1 = gate1  # Gate object
        self.pin1 = pin1  # Pin index on gate1
        self.gate2 = gate2  # Gate object
        self.pin2 = pin2  # Pin index on gate2


def initial_placement_by_sw1(gates):
    placements = {}
    x_offset = 10
    visited = set()

    input_data = [(gate.name, gate.width, gate.height) for gate in gates]

    if len(input_data) < 100:
        packer = GatePacker(tries=10)
        packing_result = packer.pack_gates(input_data)
        bounding_box = packing_result['width'], packing_result['height']
        packing_data = packing_result['packing']

    else:
        bounding_box, packing_data, _ = run_algo2sort2(input_data)

    # Place gates based on the algorithm's result, using Gate objects as keys
    for name, x, y in packing_data:
        gate_object = gate_dict[name]  # Get the Gate object from gate_dict using its name
        placements[gate_object] = (x + x_offset, y)  # Use the Gate object as the key
        visited.add(name)
    x_offset += bounding_box[0] + 10  # Increment the offset for the next component

    for gate in gates:
        if gate.name not in visited:
            placements[gate] = (x_offset, 0)
            x_offset += gate.width
    return placements


def process_input(file_content):
    global wire_delay
    lines = file_content.strip().split("\n")
    i = 0
    pins_dict = {}
    while i < len(lines):
        line = lines[i].strip()
        # Process lines starting with 'g' (gates)
        if line.lower().startswith("g"):
            gate_name, width, height, delay = parse_gate_line(line)
            gate = Gate(gate_name, width, height, delay, [])
            gate_dict[gate_name] = gate
            gates.append(gate)
            i += 1  # Move to the next line to process pins
            # Process pins line
            pin_parts = lines[i].strip().split()[2:]  # Skip the "pins" keyword and gate name
            pin_coordinates = list(map(int, pin_parts))
            pins = [(pin_coordinates[j], pin_coordinates[j + 1]) for j in range(0, len(pin_coordinates), 2)]
            gate.pins = pins

            # Classify input and output pins
            inp_pins = [(gate_name, idx) for idx, pin in enumerate(pins) if pin[0] == 0]
            outp_pins = [(gate_name, idx) for idx, pin in enumerate(pins) if pin[0] != 0]
            gate.input_pins = inp_pins
            gate.output_pins = outp_pins

            for idx in range(len(pins)):
                pins_dict[(gate_name, idx)] = 0

        # Process wire_delay line before wire lines
        elif line.lower().startswith("wire_delay"):
            wire_delay = int(line.split()[1])  # Extract wire delay value

        # Process lines that describe a wire connection
        elif line.lower().startswith("wire"):
            g1, p1, g2, p2 = parse_wire_line(line)
            wire = Wire(gate_dict[g1], int(p1) - 1, gate_dict[g2], int(p2) - 1)
            wires.append(wire)

            if (g1, int(p1) - 1) in pins_dict:
                pins_dict[(g1, int(p1) - 1)] = 1
            if (g2, int(p2) - 1) in pins_dict:
                pins_dict[(g2, int(p2) - 1)] = 1

        i += 1  # Move to the next line
    for pin in pins_dict.keys():
        if pins_dict[pin] == 0:
            if gate_dict[pin[0]].pins[pin[1]][0] == 0:
                primary_inputs.append(pin)
            else:
                primary_outputs.append(pin)

    return gates, wires


def parse_gate_line(gate_line):
    parts = gate_line.split()
    gate_name = parts[0]
    width = int(parts[1])
    height = int(parts[2])
    delay = int(parts[3])
    # Extract pin coordinates from the following line
    # pin_parts = pin_line.split()[2:]
    # pins = [(int(pin_parts[i]), int(pin_parts[i + 1])) for i in range(0, len(pin_parts), 2)]
    # because there's x coordinate and y coordinate
    return gate_name, width, height, delay


def parse_wire_line(wire_line):
    parts = wire_line.split()
    g1, p1 = parts[1].split(".")
    g2, p2 = parts[2].split(".")
    newp1 = ""
    for i in range(len(p1)):
        if i != 0:
            newp1 += p1[i]
    newp2 = ""
    for i in range(len(p2)):
        if i != 0:
            newp2 += p2[i]
    return g1, newp1, g2, newp2


def build_graph():
    global pin_conn
    for gate in gates:
        for pin in gate.input_pins:
            pin_conn[pin] = [[op, gate.delay] for op in gate.output_pins]
    for wire in wires:
        pin1 = (wire.gate1.name, wire.pin1)
        pin2 = (wire.gate2.name, wire.pin2)

        if gate_dict[pin1[0]].pins[pin1[1]][0] != 0 and gate_dict[pin2[0]].pins[pin2[1]][0] == 0:
            if pin1 not in pin_conn:
                pin_conn[pin1] = []
            pin_conn[pin1].append([pin2, 0])
        # elif gate_dict[pin1[0]].pins[pin1[1]][0] == 0 and gate_dict[pin2[0]].pins[pin2[1]][0] != 0:
        #     if pin2 not in pin_conn:
        #         pin_conn[pin2] = []
        #     pin_conn[pin2].append([pin1, 0])
        else:
            raise Exception("Invalid wire connection")

    for pin in primary_inputs:
        if detect_loop(pin, set(), set()):
            raise Exception("Loop detected in the circuit")
    return pin_conn


def detect_loop(start, visited, vis2):
    if start not in pin_conn:
        return False
    visited.add(start)
    vis2.add(start)
    for adjacent_pin in pin_conn[start]:
        if adjacent_pin[0] not in visited:
            if detect_loop(adjacent_pin[0], visited, vis2):
                return True
        elif adjacent_pin[0] in vis2:
            return True
    vis2.remove(start)
    return False

def store_pin_delay(placements):
    for pin in pin_conn:
        max_x = placements[gate_dict[pin[0]]][0] + gate_dict[pin[0]].pins[pin[1]][0]
        min_x = placements[gate_dict[pin[0]]][0] + gate_dict[pin[0]].pins[pin[1]][0]
        max_y = placements[gate_dict[pin[0]]][1] + gate_dict[pin[0]].pins[pin[1]][1]
        min_y = placements[gate_dict[pin[0]]][1] + gate_dict[pin[0]].pins[pin[1]][1]
        for adjacent_pin, _ in pin_conn[pin]:
            adjacent_x = placements[gate_dict[adjacent_pin[0]]][0] + gate_dict[adjacent_pin[0]].pins[adjacent_pin[1]][0]
            adjacent_y = placements[gate_dict[adjacent_pin[0]]][1] + gate_dict[adjacent_pin[0]].pins[adjacent_pin[1]][1]
            max_x = max(max_x, adjacent_x)
            max_y = max(max_y, adjacent_y)
            min_x = min(min_x, adjacent_x)
            min_y = min(min_y, adjacent_y)
        semi_perimeter = (max_x + max_y) - (min_x + min_y)
        for connected in pin_conn[pin]:
            connected[1] = semi_perimeter * wire_delay
    for gate in gates:
        for pin in gate.input_pins:
            pin_conn[pin] = [[op, gate.delay] for op in gate.output_pins]

def max_delay(placement):
    store_pin_delay(placement)  # Assuming this function is needed
    max_delay = 0
    max_input_pin = None

    def compute_delay(current_pin, delay_map):
        if current_pin in delay_map:
            return delay_map[current_pin]

        max_delay = 0
        max_neighbor_pin = None

        if current_pin not in pin_conn:
            delay_map[current_pin] = (0, None)
            return (0, current_pin)

        for adjacent_pin, connection_delay in pin_conn[current_pin]:
            total_delay = compute_delay(adjacent_pin, delay_map)[0] + connection_delay
            if total_delay >= max_delay:
                max_delay = total_delay
                max_neighbor_pin = adjacent_pin

        delay_map[current_pin] = (max_delay, max_neighbor_pin)
        return delay_map[current_pin]

    delaypin = {}
    for pin in primary_inputs:
        if pin in delaypin:
            pin_delay, _ = delaypin[pin]
        else:
            pin_delay, _ = compute_delay(pin, delaypin)
        if pin_delay >= max_delay:
            max_delay = pin_delay
            max_input_pin = pin

    # Construct the path
    path = []
    while max_input_pin is not None:
        path.append(max_input_pin)
        max_input_pin = delaypin[max_input_pin][1]

    return max_delay, path

def write_output(best_solution, best_cost):
    box_height = max(y + gate.height for gate, (x, y) in best_solution.items())
    box_width = max(x + gate.width for gate, (x, y) in best_solution.items())
    output = f"bounding_box {box_width} {box_height}\n"
    critical_path_delay, critical_path = max_delay(best_solution)
    output += f"critical_path"
    for pin in critical_path:
        output += f" {pin[0]}.p{pin[1] + 1}"
    output += "\n"
    output += f"critical_path_delay {critical_path_delay}\n"
    for gate, (x, y) in best_solution.items():
        output += f"{gate.name} {x} {y}\n"

    print(f" critical_delay {critical_path_delay}")
    # prints the wire length
    return output


def check_overlap(positions, gate, new_x, new_y):
    for diff_gate, (x, y) in positions.items():
        if diff_gate != gate:
            if not (
                    new_x + gate.width <= x or new_x >= x + diff_gate.width or new_y + gate.height <= y or new_y >= y + diff_gate.height):
                return True  # Overlap detected
    return False  # No overlap


def initial_placement(gates, min_spacing=2, max_spacing=10, bounding_box_size=100):
    placements = {}
    x, y = 0, 0
    max_height_in_row = 0

    for gate in gates:
        while True:
            if x + gate.width > bounding_box_size:
                x = 0
                y += max_height_in_row + random.randint(min_spacing, max_spacing)
                max_height_in_row = 0

            random_x = x + random.randint(0, 5)
            random_y = y + random.randint(0, 5)

            if not check_overlap(placements, gate, random_x, random_y):
                placements[gate] = (random_x, random_y)
                x += gate.width + random.randint(min_spacing, max_spacing)
                max_height_in_row = max(max_height_in_row, gate.height)
                break

    return placements


def simulated_annealing(gates, max_iterations=10000, initial_temp=1000, cooling_rate=0.95):
    # clusters = form_gate_clusters(wires)
    current_placement = initial_placement_by_sw1(gates)
    current_delay, current_path = max_delay(current_placement)

    best_placement = current_placement.copy()
    best_delay = current_delay
    temperature = initial_temp
    if len(gates) >= 500:
        max_iterations = 1000
    elif len(gates) <= 50:
        max_iterations = 10000
    for iteration in range(max_iterations):
        gate_to_move = random.choice(gates)
        gate_name = gate_to_move.name
        new_placement = current_placement.copy()
        new_x = new_placement[gate_dict[gate_name]][0] + random.randint(-75, 75)
        new_y = new_placement[gate_dict[gate_name]][1] + random.randint(-75, 75)
        if new_x < 0 or new_y < 0:
            continue
        if not check_overlap(new_placement, gate_to_move, new_x, new_y):
            new_placement[gate_to_move] = (new_x, new_y)
        else:
            continue
        new_delay, new_path = max_delay(new_placement)
        # Acceptance criteria (Simulated Annealing)
        if new_delay - current_delay < 0 or random.random() < math.exp(-(new_delay - current_delay) / temperature):
            current_placement = new_placement
            current_delay = new_delay

        # Update best placement
        if current_delay < best_delay:
            best_placement = current_placement.copy()
            best_delay = current_delay
        # Cool down the temperature
        temperature *= cooling_rate

    return best_placement, best_delay


def main(input_file, output_file):
    # Read from the input file
    start_time = time.time()
    with open(input_file, "r") as file:
        file_content = file.read()

    gates, wires = process_input(file_content)
    initial_placement(gates)
    build_graph()

    if len(primary_inputs) == 0:
        print("No primary inputs")
        return
    if len(primary_outputs) == 0:
        print("No primary outputs")
        return

    best_placement, best_delay = simulated_annealing(gates)
    # print(len(all_paths))
    # for path in all_paths:
    #     print(path, end=' ')
    #     print(f" delay: {calculate_path_delay(path, best_placement)}")

    #Run simulated annealing to find the best placement
    if len(gates) <= 50:
        for i in range(10):
            temp_placement, temp_delay = simulated_annealing(gates)
            if temp_delay < best_delay:
                best_placement = temp_placement
                best_delay = temp_delay

    # for i in range(10):
    #     temp_placement, temp_length = simulated_annealing_by_initial_placement(gates, wires)
    #     if temp_length < best_length:
    #         best_placement = temp_placement
    #         best_length = temp_length
    # Write the output

    output = write_output(best_placement, best_delay)
    # Write to the output file
    with open(output_file, "w") as file:
        file.write(output)
    print("--- %s seconds ---" % (time.time() - start_time))


# Run the program with input from 'input.txt' and write the result to 'output.txt'
if __name__ == "__main__":
    main("input.txt", "output.txt")
