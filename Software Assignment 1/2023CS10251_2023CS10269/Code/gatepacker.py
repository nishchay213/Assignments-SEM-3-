from algo1 import algo1
class GatePacker:
    def __init__(self,tries=1):
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
                box_width += min(gatesnew[-1][1],minh)
                box_height += min(gatesnew[-1][1],minh)
            else:
                curr_width, curr_height = box.getmax()
                curr = totalarea / (curr_width * curr_height)
                if best_box is None or curr_width * curr_height < best_box['area']:
                    best_box = {'area': curr_width * curr_height,'width': curr_width,'height': curr_height,'packing': current}
                    if curr >= 1.0:
                        break
                box_width = curr_width
                box_height = curr_height
                boxes += 1
        return best_box
    