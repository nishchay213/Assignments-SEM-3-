import random
from collections import defaultdict

wire_delay = 0


# Disjoint-set (Union-Find) to detect cycles in the graph
class UnionFind:
    def __init__(self, n):
        self.parent = {i: i for i in range(1, n + 1)}
        self.rank = {i: 0 for i in range(1, n + 1)}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootY] = rootX
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1


def generate_test_case(num_gates, max_pins, max_total_pins, max_width, max_height, wire_delay_factor, variance_sizes,
                       wire_density, variance_delays):
    # num_gates = random.randint(1, num_gates)
    # max_pins = random.randint(1, 40)

    total_pins = 0
    gates = []
    gate_delays = []
    wires = []
    gate_pins = {}  # Store pin details for each gate
    uf = UnionFind(num_gates)  # Initialize Union-Find for cycle detection
    connected_gates = []  # List to keep track of connected gates
    global wire_delay

    # Generate gates with delays and pins
    for i in range(1, num_gates + 1):
        # Gate sizes variance control based on maximum width and height
        if variance_sizes == 'high':
            width = random.randint(1, max_width)
            height = random.randint(1, max_height)
        elif variance_sizes == 'medium':
            width = random.randint(int(max_width * 0.5), int(max_width * 0.75))
            height = random.randint(int(max_height * 0.5), int(max_height * 0.75))
        else:
            width = random.randint(int(max_width * 0.75), max_width)
            height = random.randint(int(max_height * 0.75), max_height)

        # Gate delays variance control
        if variance_delays == 'high':
            delay = random.randint(1, 50)  # Wide range for high variance
        elif variance_delays == 'medium':
            delay = random.randint(20, 30)  # Medium range for medium variance
        else:
            delay = random.randint(25, 27)  # Narrow range for low variance

        gate_delays.append(delay)

        # Generate pins (at least 1 input pin at x=0 and 1 output pin at x=width)
        input_pins = []
        output_pins = []
        used_input_y = set()
        used_output_y = set()

        # Create at least 1 input pin at (0, random y)
        input_y = random.randint(0, height)
        used_input_y.add(input_y)
        input_pins.append((0, input_y))  # Input pin at x = 0

        # Create at least 1 output pin at (width, random y)
        output_y = random.randint(0, height)
        used_output_y.add(output_y)
        output_pins.append((width, output_y))  # Output pin at x = width

        # Generate additional pins if needed
        num_additional_pins = random.randint(0, min(max_pins - 2, height - 2))  # Reserve 2 for input/output
        for _ in range(num_additional_pins):
            if random.choice([True, False]):  # Randomly decide if it's input or output
                # Additional input pin
                y = random.randint(0, height)
                while y in used_input_y:  # Ensure unique input pin
                    y = random.randint(0, height)
                used_input_y.add(y)
                input_pins.append((0, y))  # Input pin at x = 0
            else:
                # Additional output pin
                y = random.randint(0, height)
                while y in used_output_y:  # Ensure unique output pin
                    y = random.randint(0, height)
                used_output_y.add(y)
                output_pins.append((width, y))  # Output pin at x = width

        # Ensure at least one "proper" input (not connected to any output) and one "proper" output (not connected to any input)
        pins = input_pins + output_pins
        total_pins += len(pins)
        if total_pins > max_total_pins:
            break

        gate_name = f'g{i}'
        gate_pins[gate_name] = {
            'input_pins': [f'{gate_name}.p{idx + 1}' for idx in range(len(input_pins))],
            'output_pins': [f'{gate_name}.p{len(input_pins) + idx + 1}' for idx in range(len(output_pins))]
        }

        # Add the generated pins to the gate's output format
        gates.append(
            f"{gate_name} {width} {height} {delay}\npins {gate_name} " + " ".join([f"{x} {y}" for x, y in pins]))

        # Connect the current gate to one of the already connected gates
        if connected_gates:
            previous_gate = random.choice(connected_gates)
            if gate_pins[previous_gate]['output_pins'] and gate_pins[gate_name]['input_pins']:
                output_pin = random.choice(gate_pins[previous_gate]['output_pins'])
                input_pin = random.choice(gate_pins[gate_name]['input_pins'])
                wires.append(f"wire {output_pin} {input_pin}")
                # Union the gates in the disjoint set
                uf.union(int(previous_gate[1:]), i)  # Connect previous gate to current gate

        connected_gates.append(gate_name)  # Add the current gate to the connected list

    # Calculate average gate delay
    avg_gate_delay = sum(gate_delays) / len(gate_delays)

    # Set wire delay based on the average gate delay and the wire_delay_factor
    wire_delay = int(wire_delay_factor * avg_gate_delay)

    return gates, wires


def write_test_case_to_file(gates, wires, filename='input.txt'):
    with open(filename, 'w') as f:
        f.write("\n".join(gates))
        f.write(f"\nwire_delay {wire_delay}\n")
        f.write("\n".join(wires))


# Example usage:
num_gates = 100
max_pins = 400
max_total_pins = 40000
max_width = 100
max_height = 100
wire_delay_factor = 0.5
variance_sizes = 'medium'
wire_density = 'high'
variance_delays = 'high'

# gates, wires = generate_test_case(num_gates, max_pins, max_total_pins, max_width, max_height, wire_delay_factor,
#                                   variance_sizes, wire_density, variance_delays)
# write_test_case_to_file(gates, wires)
def main():
    gates, wires = generate_test_case(num_gates, max_pins, max_total_pins, max_width, max_height, wire_delay_factor,
                                      variance_sizes, wire_density, variance_delays)
    write_test_case_to_file(gates, wires)

