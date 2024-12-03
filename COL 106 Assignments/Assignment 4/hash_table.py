from prime_generator import get_next_size


class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        pass

    def insert(self, x):
        pass

    def number_for_latin_letter(self, c):
        if c.islower():
            return ord(c) - ord('a')
        return ord(c) - ord('A') + 26

    def find(self, key):
        pass

    def get_slot(self, key):
        pass

    def get_load(self):
        pass

    def __str__(self):
        pass

    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass


# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF,
# YOU WOULD NOT NEED TO WRITE IT TWICE

class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.collision_type = collision_type
        self.params = params
        self.table_size = params[-1]
        self.table = [None] * self.table_size
        self.size = 0
        self.slots = 0

    def hash_function(self, x):
        return self.calc_hash(list(x), self.params[0], self.table_size)

    def calc_hash(self, x, z, p):
        h = 0
        while len(x) > 0:
            last = x.pop()
            h = (h * z + self.number_for_latin_letter(last)) % p
        return h

    def double_hash(self, x):
        return self.params[2] - self.calc_hash(list(x), self.params[1], self.params[2])

    def insert(self, key):
        if self.find(key):
            return
        if self.collision_type != "Chain":
            if self.size == self.table_size:
                raise Exception("Table is full")
        self.size += 1
        k = self.hash_function(key)
        k = k % self.table_size
        if self.table[k] == None:
            if self.collision_type == "Chain":
                self.table[k] = [key]
            else:
                self.table[k] = key

            self.slots += 1
        else:
            if self.collision_type == "Chain":
                if type(self.table[k]) == list:
                    self.table[k].append(key)
                else:
                    self.table[k] = [self.table[k], key]

            if self.collision_type == "Linear":
                for i in range(1, self.table_size):
                    if self.table[(k + i) % self.table_size] == None:
                        self.table[(k + i) % self.table_size] = key

                        self.slots += 1
                        break
            if self.collision_type == "Double":
                for i in range(1, self.table_size):
                    if self.table[(k + i * self.double_hash(key)) % self.table_size] == None:
                        self.table[(k + i * self.double_hash(key)) % self.table_size] = key

                        self.slots += 1
                        break

    def find(self, key):
        k = self.hash_function(key)
        k = k % self.table_size

        if self.table[k] == key:
            return True
        if self.collision_type == "Chain":
            if type(self.table[k]) == list:
                if key in self.table[k]:
                    return True
        if self.collision_type == "Linear":
            for i in range(1, self.table_size):
                if self.table[(k + i) % self.table_size] == key:
                    return True
                elif self.table[(k + i) % self.table_size] == None:
                    return False
        if self.collision_type == "Double":
            for i in range(1, self.table_size):
                if self.table[(k + i * self.double_hash(key)) % self.table_size] == key:
                    return True
                elif self.table[(k + i * self.double_hash(key)) % self.table_size] == None:
                    return False
        return False

    def get_slot(self, key):
        return self.hash_function(key) % self.table_size

    def get_load(self):
        return self.size / self.table_size

    def __str__(self):
        result = []
        for i in range(self.table_size):
            if self.table[i] == None:
                result.append("<EMPTY>")
            else:
                if type(self.table[i]) == list:
                    result.append(" ; ".join(self.table[i]))
                else:
                    result.append(self.table[i])
        return " | ".join(result)



class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.collision_type = collision_type
        self.params = params
        self.table_size = params[-1]
        self.table = [None] * self.table_size
        self.size = 0
        self.slots = 0

    def hash_function(self, x):
        return self.calc_hash(list(x), self.params[0], self.table_size)

    def calc_hash(self, x, z, p):
        h = 0
        while len(x) > 0:
            last = x.pop()
            h = (h * z + self.number_for_latin_letter(last)) % p
        return h

    def double_hash(self, x):
        return self.params[2] - self.calc_hash(list(x), self.params[1], self.params[2])

    def insert(self, x):
        # x = (key, value)

        key = x[0]
        if self.find(key) is not None:
            return
        if self.collision_type != "Chain":
            if self.size == self.table_size:
                raise Exception("Table is full")
        value = x[1]
        k = self.hash_function(key)
        k = k % self.table_size
        if self.table[k] == None:
            if self.collision_type == "Chain":
                self.table[k] = [x]
            else:

                self.table[k] = x
            self.size += 1
            self.slots += 1
        else:
            if self.collision_type == "Chain":
                if type(self.table[k]) == list:
                    self.table[k].append(x)
                else:
                    self.table[k] = [x]
                self.size += 1
            if self.collision_type == "Linear":
                for i in range(1, self.table_size):
                    if self.table[(k + i) % self.table_size] == None:
                        self.table[(k + i) % self.table_size] = x
                        self.size += 1
                        self.slots += 1
                        break
            if self.collision_type == "Double":
                for i in range(1, self.table_size):
                    if self.table[(k + i * self.double_hash(key)) % self.table_size] == None:
                        self.table[(k + i * self.double_hash(key)) % self.table_size] = x
                        self.size += 1
                        self.slots += 1
                        break

    def find(self, key):
        # return value
        k = self.hash_function(key)
        k = k % self.table_size
        if self.table[k] == None:
            return None
        if self.table[k][0] == key:
            return self.table[k][1]
        if self.collision_type == "Chain":
            if type(self.table[k]) == list:
                for i in range(len(self.table[k])):
                    if self.table[k][i][0] == key:
                        return self.table[k][i][1]
        if self.collision_type == "Linear":
            for i in range(1, self.table_size):
                if self.table[(k + i) % self.table_size] == None:
                    return None
                if self.table[(k + i) % self.table_size][0] == key:
                    return self.table[(k + i) % self.table_size][1]

        if self.collision_type == "Double":
            for i in range(1, self.table_size):
                if self.table[(k + i * self.double_hash(key)) % self.table_size] == None:
                    return None
                if self.table[(k + i * self.double_hash(key)) % self.table_size][0] == key:
                    return self.table[(k + i * self.double_hash(key)) % self.table_size][1]

        return None

    def get_slot(self, key):
        return self.hash_function(key) % self.table_size

    def get_load(self):
        return self.size / self.table_size

    def __str__(self):
        result = []
        for i in range(self.table_size):
            if self.table[i] == None:
                result.append("<EMPTY>")
            else:
                if type(self.table[i]) == list:
                    result.append(" ; ".join([f"({k} , {v})" for k, v in self.table[i]]))
                else:
                    result.append(f"({self.table[i][0]} , {self.table[i][1]})")
        return " | ".join(result)
