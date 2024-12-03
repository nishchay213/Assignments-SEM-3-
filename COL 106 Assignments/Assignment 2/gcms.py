from bin import Bin
from avl import AVLTree
from avl import comp_1
from avl import comp_2
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.bins_by_id = AVLTree()
        self.objects = AVLTree()
        self.bins_by_capacity_bg = AVLTree(comp_1)
        self.bins_by_capacity_yr = AVLTree(comp_2)


    def add_bin(self, bin_id, capacity):
        self.bins_by_id.insert(bin_id, Bin(bin_id, capacity))
        self.bins_by_capacity_bg.insert(capacity, bin_id)
        self.bins_by_capacity_yr.insert(capacity, bin_id)



    def add_object(self, object_id, size, color):
        # raise NoBinFoundException

        if color == Color.BLUE:

            if self.bins_by_capacity_bg.is_empty() or self.bins_by_capacity_bg.find_max()<size:

                raise NoBinFoundException()

            else:
                bin_id, capacity = self.bins_by_capacity_bg.find_just_greater_or_equal(size, 0)

        elif color == Color.YELLOW:
            if self.bins_by_capacity_yr.is_empty() or self.bins_by_capacity_yr.find_max()<size:
                raise NoBinFoundException()
            else:
                bin_id, capacity = self.bins_by_capacity_yr.find_just_greater_or_equal(size, 1)

        elif color == Color.RED:
            # print("this2")
            if self.bins_by_capacity_yr.is_empty() or self.bins_by_capacity_yr.find_max()<size:

                raise NoBinFoundException()
            else:
                # print("this")
                bin_id, capacity = self.bins_by_capacity_yr.find_max_for_bins()

        else:
            if self.bins_by_capacity_bg.is_empty() or self.bins_by_capacity_bg.find_max()<size:
                raise NoBinFoundException()
            else:
                bin_id, capacity = self.bins_by_capacity_bg.find_max_for_bins()

        Bin = self.bins_by_id.find(bin_id)
        Bin.add_object(Object(object_id, size, color))
        new_capacity = capacity - size
        Bin.capacity = new_capacity
        self.bins_by_capacity_yr.remove_for_bins(capacity, bin_id)
        self.bins_by_capacity_yr.insert(new_capacity, bin_id)
        self.bins_by_capacity_bg.remove_for_bins(capacity, bin_id)
        self.bins_by_capacity_bg.insert(new_capacity, bin_id)
        self.objects.insert(object_id, bin_id)







    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin

        bin_id = self.objects.find(object_id)
        try:
            Bin1 = self.bins_by_id.find(bin_id)
        except ValueError:
            return None
        # Bin1 = self.bins_by_id.find(bin_id)
        capacity = self.bins_by_id.find(bin_id).capacity

        object1 = Bin1.objects.find(object_id)
        new_capacity = capacity + object1.size
        self.bins_by_capacity_bg.remove_for_bins(capacity, bin_id)
        self.bins_by_capacity_bg.insert(new_capacity, bin_id)
        self.bins_by_capacity_yr.remove_for_bins(capacity, bin_id)
        self.bins_by_capacity_yr.insert(new_capacity, bin_id)

        Bin1.remove_object(object_id)
        Bin1.capacity = new_capacity
        self.objects.delete(object_id)


    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        Bin = self.bins_by_id.find(bin_id)

        return (Bin.capacity, [object for object in Bin.objects.inorder()])
    def object_info(self, object_id):
        # returns the bin_id in which the object is stored

        return self.objects.find(object_id)
    
    