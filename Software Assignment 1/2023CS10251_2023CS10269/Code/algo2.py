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
        space['top'] = {'x': space['x'], 'y': space['y'] + height, 'w': space['w'], 'h': space['h'] - height, 'used': False, 'right': None, 'top': None}
        space['right'] = {'x': space['x'] + width, 'y': space['y'], 'w': space['w'] - width, 'h': height, 'used': False, 'right': None, 'top': None}
        return space

    def expand_top(self, width, height):
        self.root = {
            'used': True,'x': 0,'y': 0,'w': self.root['w'],'h': self.root['h'] + height,'right': self.root,
            'top': {'x': 0, 'y': self.root['h'], 'w': self.root['w'], 'h': height, 'used': False, 'right': None, 'top': None}
        }
        space = self.locate_space(self.root, width, height)
        return self.divide_space(space, width, height) if space else None

    def expand_right(self, width, height):
        self.root = {
            'used': True,'x': 0,'y': 0,'w': self.root['w'] + width,'h': self.root['h'],'top': self.root,
            'right': {'x': self.root['w'], 'y': 0, 'w': width, 'h': self.root['h'], 'used': False, 'right': None, 'top': None}
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