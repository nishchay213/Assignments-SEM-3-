from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)

    def h1(self, key, size):
        return self.calc_hash(list(key), self.params[0], size)

    def h2(self, key, size):
        return self.params[2] - self.calc_hash(list(key), self.params[1], self.params[2])

    def rehash(self):
        # IMPLEMENT THIS FUNCTION

        new_size = get_next_size()
        new_table = [None] * new_size
        old_table = self.table
        old_size = self.table_size
        self.table = new_table
        self.table_size = new_size
        for i in range(old_size):
            if old_table[i]!=None:
                if self.collision_type == "Chain":
                    if type(old_table[i]) == list:
                        for j in old_table[i]:
                            k = self.h1(j, new_size)
                            if self.table[k] == None:
                                self.table[k] = [j]
                            else:
                                self.table[k].append(j)

                    else:
                        k = self.h1(old_table[i], new_size)
                        if self.table[k] == None:
                            self.table[k] = old_table[i]
                        else:
                            self.table[k].append(old_table[i])


                if self.collision_type == "Linear":
                    k = self.h1(old_table[i], new_size)
                    if self.table[k] == None:
                        self.table[k] = old_table[i]
                    else:
                        k = (k + 1) % new_size
                        while self.table[k] != None:
                            k = (k + 1) % new_size
                        self.table[k] = old_table[i]


                if self.collision_type == "Double":
                    k = self.h1(old_table[i], new_size)

                    if self.table[k] == None:
                        self.table[k] = old_table[i]
                    else:
                        step_size = self.double_hash(old_table[i])
                        k = (k + step_size) % new_size
                        while self.table[k] != None:
                            k = (k + step_size) % new_size
                        self.table[k] = old_table[i]











        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:

            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    def h1(self, key, size):
        return self.calc_hash(list(key), self.params[0], size)
    def h2(self, key, size):
        return self.params[2] - self.calc_hash(list(key), self.params[1], self.params[2])

    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size = get_next_size()
        new_table = [None] * new_size
        old_table = self.table
        old_size = self.table_size
        self.table = new_table
        self.table_size = new_size
        for i in range(old_size):
            if old_table[i]!=None:
                if self.collision_type == "Chain":
                    if type(old_table[i]) == list:
                        for j in old_table[i]:
                            k = self.h1(j[0], new_size)
                            if self.table[k] == None:
                                self.table[k] = [j]
                            else:
                                self.table[k].append(j)

                    else:
                        k = self.h1(old_table[i][0], new_size)
                        if self.table[k] == None:
                            self.table[k] = old_table[i]
                        else:
                            self.table[k].append(old_table[i])


                if self.collision_type == "Linear":
                    k = self.h1(old_table[i][0], new_size)
                    if self.table[k] == None:
                        self.table[k] = old_table[i]
                    else:
                        k = (k + 1) % new_size
                        while self.table[k] != None:
                            k = (k + 1) % new_size
                        self.table[k] = old_table[i]


                if self.collision_type == "Double":
                    k = self.h1(old_table[i][0], new_size)

                    if self.table[k] == None:
                        self.table[k] = old_table[i]
                    else:
                        step_size = self.double_hash(old_table[i][0])
                        k = (k + step_size) % new_size
                        while self.table[k] != None:
                            k = (k + step_size) % new_size
                        self.table[k] = old_table[i]








        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()