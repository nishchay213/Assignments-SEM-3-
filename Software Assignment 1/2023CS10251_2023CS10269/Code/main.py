from gatepacker import GatePacker
from algo2 import GatePlacer

def read_input():
    input_data = []
    with open('input.txt', 'r') as file:
        for line in file:
            name, width, height = line.split()
            input_data.append((name, int(width), int(height)))
    return input_data

def output(bounding_box, packing_data, efficiency):
    with open('output.txt', 'w') as file:
        file.write(f"bounding_box {bounding_box[0]} {bounding_box[1]}\n")
        for name, x, y in packing_data:
            file.write(f"{name} {x} {y}\n")
    print(f"packing_efficiency {efficiency:.2f}")

def run_algo1(input_data):
    packer = GatePacker(tries=1)
    packing_result = packer.pack_gates(input_data)

    if packing_result:
        total_area = sum(w * h for _, w, h in input_data)
        bounding_box_area = packing_result['area']
        efficiency = (total_area / bounding_box_area) * 100
        bounding_box = (packing_result['width'], packing_result['height'])
        packing_data = packing_result['packing']
    else:
        efficiency = 0
        bounding_box = (0, 0)
        packing_data = []

    return bounding_box, packing_data, efficiency

def run_algo2sort1(input_data):
    input_data.sort(key=lambda x: (x[2], x[1]), reverse=True)
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

def run_algo2sort2(input_data):
    input_data.sort(key=lambda x: (x[1], x[2]), reverse=True)
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

def main():
    input_data = read_input()
    if len(input_data) > 100:
        bounding_box1, packing_data1, efficiency1 = run_algo2sort1(input_data)
        bounding_box2, packing_data2, efficiency2 = run_algo2sort2(input_data)
        if efficiency1 > efficiency2:
            bounding_box, packing_data, efficiency = bounding_box1, packing_data1, efficiency1
        else:
            bounding_box, packing_data, efficiency = bounding_box2, packing_data2, efficiency2

    else:
        bounding_box1, packing_data1, efficiency1 = run_algo1(input_data)
        bounding_box2, packing_data2, efficiency2 = run_algo2sort1(input_data)
        bounding_box3, packing_data3, efficiency3 = run_algo2sort2(input_data)
        if efficiency1 > efficiency2 and efficiency1 > efficiency3:
            bounding_box, packing_data, efficiency = bounding_box1, packing_data1, efficiency1
        elif efficiency2 > efficiency1 and efficiency2 > efficiency3:
            bounding_box, packing_data, efficiency = bounding_box2, packing_data2, efficiency2
        else:
            bounding_box, packing_data, efficiency = bounding_box3, packing_data3, efficiency3

    output(bounding_box, packing_data, efficiency)

if __name__ == "__main__":
    main()
