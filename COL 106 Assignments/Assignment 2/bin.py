from avl import AVLTree

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects = AVLTree()



    def add_object(self, object):
        # Implement logic to add an object to this bin
        self.objects.insert(object.object_id, object)


    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        self.objects.delete(object_id)
