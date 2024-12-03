wire_delay = 0
gate_dict = {}
gates = []
wires = []
pins_dict = {}
pin_adj_list = {}
primary_inputs = []
primary_outputs = []

#nishchay213

class Gate:
    def __init__(self, name, width, height,delay, pins):
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

def process_input(file_content):
    global wire_delay
    # global pins_count
    lines = file_content.strip().split("\n")
    # pins_count = 0
    i = 0
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

            # Update all_pins dictionary
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
            if (g1, int(p1) - 1) not in pin_adj_list:
                pin_adj_list[(g1, int(p1) - 1)] = []
            pin_adj_list[(g1, int(p1) - 1)].append((g2, int(p2) - 1))

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
        if i!=0:
            newp1+=p1[i]
    newp2 = ""
    for i in range(len(p2)):
        if i!=0:
            newp2+=p2[i]
    return g1, newp1, g2, newp2

all_paths = []

def find_all_complete_paths():
    for pin in primary_inputs:
        for output_pin in primary_outputs:

            paths = find_paths(pin, output_pin)
            for path in paths:
                all_paths.append(path)

def wire_length(placements, pin):
    max_x = placements[gate_dict[pin[0]]][0] + gate_dict[pin[0]].pins[pin[1]][0]
    min_x = placements[gate_dict[pin[0]]][0] + gate_dict[pin[0]].pins[pin[1]][0]
    max_y = placements[gate_dict[pin[0]]][1] + gate_dict[pin[0]].pins[pin[1]][1]
    min_y = placements[gate_dict[pin[0]]][1] + gate_dict[pin[0]].pins[pin[1]][1]

    for neighbor in pin_adj_list[pin]:
        x = placements[gate_dict[neighbor[0]]][0] + gate_dict[neighbor[0]].pins[neighbor[1]][0]
        y = placements[gate_dict[neighbor[0]]][1] + gate_dict[neighbor[0]].pins[neighbor[1]][1]

        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)
    semi = max_x + max_y - min_x - min_y

    return semi * wire_delay

def calculate_path_delay(path, placements):

    total_delay = 0
    for i in range(len(path)-1):
        pin1 = path[i]
        pin2 = path[i+1]

        gate1 = gate_dict[pin1[0]]
        gate2 = gate_dict[pin2[0]]

        if i == 0:
            total_delay += gate1.delay
        if not gate1 == gate2:
            total_delay += wire_length(placements, pin1)
            total_delay += gate2.delay

    return total_delay

def max_delay(placements):

    max_delay = 0
    for path in all_paths:

        path_delay = calculate_path_delay(path, placements)
        max_delay = max(max_delay, path_delay)
    return max_delay

complete_graph = {}

def build_graph():
    for gate in gates:
        for pin in gate.input_pins:
            complete_graph[pin] = []
            for output_pin in gate.output_pins:
                complete_graph[pin].append(output_pin)

    for wire in wires:
        pin1 = (wire.gate1.name, wire.pin1)
        pin2 = (wire.gate2.name, wire.pin2)
        if pin1 not in complete_graph:
            complete_graph[pin1] = []
        complete_graph[pin1].append(pin2)

def find_paths(start, end, path=[]):

    path = path + [start]
    if start == end:

        return [path]
    if start not in complete_graph:
        return []
    paths = []
    for node in complete_graph[start]:
        if node not in path:
            newpaths = find_paths(node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

their_wire_delay = 0
their_critical_path = []
def process_output(file_content):
    global their_wire_delay
    lines = file_content.strip().split("\n")
    placements = {}
    for line in lines:
        if line.startswith("critical_path_delay"):
            their_wire_delay = int(line.split()[1])
        elif line.startswith("bounding_box"):
            continue
        elif line.startswith("critical_path"):
            parts = line.split()
            for i in range(1, len(parts)):
                gate_name, pin = parts[i].split(".")
                newp1 = ""
                for i in range(len(pin)):
                    if i != 0:
                        newp1 += pin[i]
                their_critical_path.append((gate_name, int(newp1)-1))

        elif line.startswith("g"):
            parts = line.split()
            gate_name = parts[0]
            x = int(parts[1])
            y = int(parts[2])
            placements[gate_dict[gate_name]] = (x, y)
        else:
            continue
    return placements

def find_critical_path(placements):
    critical_path =[]
    max_delay = 0
    for path in all_paths:
        path_delay = calculate_path_delay(path, placements)
        # print(path_delay)
        if path_delay > max_delay:
            max_delay = path_delay
            critical_path = path
    return critical_path, max_delay

def main():
    global their_wire_delay
    global gates, wires
    with open("input.txt", "r") as f:
        file_content = f.read()
    gates, wires = process_input(file_content)
    build_graph()
    find_all_complete_paths()





    with open("output.txt", "r") as f:
        file_content = f.read()
    placements = process_output(file_content)
    calculated_critical_path, calculated_max_delay = find_critical_path(placements)
    for path in all_paths:
        print(path)
        print(calculate_path_delay(path, placements))

    if calculated_max_delay == 0:
        print("No paths from primary inputs to primary outputs")
        return
    if their_wire_delay != calculated_max_delay:
        print("Incorrect wire delay")
        print("Expected:", calculated_max_delay, their_wire_delay)

    print(f"Max delay is correct: {calculated_max_delay}")

    if their_critical_path != calculated_critical_path:
        print("Incorrect critical path")
        print("Expected:", calculated_critical_path)
        print("Got:", their_critical_path)
        return
    print("Critical path is correct")

if __name__ == "__main__":
    main()




