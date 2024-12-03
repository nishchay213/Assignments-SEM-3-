class algo1:
    def __init__(self, boxw, boxh):
        self.boxw = int(boxw)
        self.boxh = int(boxh)
        self.valid = [[False] * self.boxh for _ in range(self.boxw)]

    def add(self, width, height):
        for i in range(self.boxw - width+1):
            for j in range(self.boxh - height+1):
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
