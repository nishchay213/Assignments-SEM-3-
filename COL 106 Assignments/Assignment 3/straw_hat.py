'''
    This file contains the class definition for the StrawHat class.
'''

from crewmate import CrewMate
from heap import Heap, Node
from treasure import Treasure
def comp(node1, node2):
    if node1.key<node2.key:
        return True
    return False

def comp_treasure(node1, node2):
    if node1.key<node2.key:
        return True
    if node1.key==node2.key:
        if node1.value.id<node2.value.id:
            return True
    return False
def comp2(node1, node2):
    if node1.key>node2.key:
        return True
    return False

class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    
    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''
        crewmates_list = []
        for i in range(m):
            crewmates_list.append(Node(0, CrewMate()))
        self.crewmates = Heap(comp, crewmates_list)
        self.non_empty_crewmates = []



        # Write your code here
        pass
    
    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        least_load_node = self.crewmates.extract()

        least_load_node.value.add_treasure(treasure)
        least_finish_time = least_load_node.key
        least_finish_time = max(least_finish_time, treasure.arrival_time) + treasure.size
        self.crewmates.insert(Node(least_finish_time, least_load_node.value))
        if least_load_node.value.empty:
            self.non_empty_crewmates.append(least_load_node.value)
            least_load_node.value.empty = False







        
        # Write your code here
        pass
    
    def get_completion_time(self):
        '''
        Arguments:
            None
        Returns:
            List[Treasure] : List of treasures in the order of their ids after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Write your code here
        processed = []
        for crewmate in self.non_empty_crewmates:


            treasures_heap = Heap( comp_treasure, [])
            t = 0
            for treasure in crewmate.treasure:
                if treasures_heap.size()==0:
                    treasures_heap.insert(Node(treasure.arrival_time + treasure.size, treasure))
                    t = treasure.arrival_time
                else:
                    while t<=treasure.arrival_time:
                        if treasures_heap.size()==0:
                            treasures_heap.insert(Node(treasure.arrival_time + treasure.size, treasure))
                            t = treasure.arrival_time
                            break
                        node = treasures_heap.extract()
                        rem_size = node.key - node.value.arrival_time

                        if rem_size>(treasure.arrival_time-t):
                            node.key = node.key - (treasure.arrival_time-t)
                            treasures_heap.insert(node)
                            treasures_heap.insert(Node(treasure.arrival_time + treasure.size, treasure))
                            t = treasure.arrival_time
                            break
                        else:

                            node.value.completion_time = t + rem_size
                            node.key -= rem_size
                            processed.append(node.value)
                            t += rem_size
            while treasures_heap.size()>0:
                node = treasures_heap.extract()
                if t<node.value.arrival_time:
                    t = node.value.arrival_time


                node.value.completion_time = t + node.key - node.value.arrival_time
                processed.append(node.value)
                t = t + node.key - node.value.arrival_time

        processed.sort(key = lambda x: x.id)
        return processed


















    
    # You can add more methods if required