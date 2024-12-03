from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)

        """
        self.flights = flights
        self.cities_max_index = 0
        self.flights_max_index = 0

        for flight in flights:
            self.cities_max_index = max(self.cities_max_index, flight.start_city, flight.end_city)
            self.flights_max_index = max(self.flights_max_index, flight.flight_no)
        self.cities_connect = [[] for i in range(self.cities_max_index + 1)]
        self.cities_reverse_connect = [[] for i in range(self.cities_max_index + 1)]

        for flight in flights:
            self.cities_connect[flight.start_city].append(flight)
            self.cities_reverse_connect[flight.end_city].append(flight)

        self.flights_graph = [[] for i in range (self.flights_max_index + 1)]
        for flight in flights:
            end_city = flight.end_city
            reaching_time = flight.arrival_time
            second_list = self.cities_connect[end_city]
            for second_flight in second_list:
                if second_flight.departure_time >= reaching_time + 20:
                    self.flights_graph[flight.flight_no].append(second_flight)





        pass
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with same number of flights,
        arrives the earliest
        """
        queue = CircularQueue(self.flights_max_index + 10)


        visited = [False] * (self.flights_max_index + 1)
        levels = [-1] * (self.flights_max_index + 1)
        for flight in self.cities_connect[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                queue.enqueue(flight)
                visited[flight.flight_no] = True
                levels[flight.flight_no] = 0

        while not queue.is_empty():

            current_flight = queue.dequeue()
            for next_flight in self.flights_graph[current_flight.flight_no]:
                if not visited[next_flight.flight_no] and next_flight.arrival_time <= t2:
                    visited[next_flight.flight_no] = True
                    levels[next_flight.flight_no] = levels[current_flight.flight_no] + 1
                    queue.enqueue(next_flight)
        best_route = []
        #best_time = 1e9

        cur_end_city = end_city
        not_exists = True
        for flight in self.cities_reverse_connect[end_city]:
            if visited[flight.flight_no]:
                not_exists = False
                break
        if not_exists:
            return []

        while end_city != start_city:
            best_flight = None
            curr_best = 1e9
            best_time = 1e9
            for flight in self.cities_reverse_connect[end_city]:



                if visited[flight.flight_no]:
                    if levels[flight.flight_no] < curr_best:
                        #print(flight.flight_no, flight.arrival_time, levels[flight.flight_no], curr_best)
                        best_flight = flight
                        curr_best = levels[flight.flight_no]
                        best_time = flight.arrival_time
                        #print(best_time)
                    elif curr_best == levels[flight.flight_no] and flight.arrival_time < best_time:
                        #print(flight.flight_no, flight.arrival_time)
                        best_flight = flight
                        curr_best = levels[flight.flight_no]
                        best_time = flight.arrival_time





            end_city = best_flight.start_city
            best_route.append(best_flight)

        best_route.reverse()
        # for flight in best_route:
        #     print(flight.flight_no, end=" ")
        # print(levels)




        return best_route











        pass
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        #consider the fare as the weight of the edge and apply dijkstra's algorithm
        source = start_city
        distance = [1e9] * (self.flights_max_index + 1)

        pri_queue = priority_queue_by_heap()
        for flight in self.cities_connect[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                pri_queue.insert(Node(flight.fare, flight))
                distance[flight.flight_no] = flight.fare
        visited = [False] * (self.flights_max_index + 1)

        while pri_queue.size() > 0:
            top_most = pri_queue.extract()
            current_flight = top_most.value
            if visited[current_flight.flight_no]:
                continue
            visited[current_flight.flight_no] = True
            cur_dist = top_most.key
            for next_flight in self.flights_graph[current_flight.flight_no]:
                add_dist = next_flight.fare
                if(next_flight.arrival_time <= t2) and (distance[next_flight.flight_no] > cur_dist + add_dist):
                    distance[next_flight.flight_no] = cur_dist + add_dist
                    pri_queue.insert(Node(distance[next_flight.flight_no], next_flight))

        best_route = []
        not_exists = True
        for flight in self.cities_reverse_connect[end_city]:
            if visited[flight.flight_no]:
                not_exists = False
                break
        if not_exists:
            return []
        cur_end_city = end_city
        while end_city != start_city:
            best_flight = None
            curr_best = 1e9
            #best_time = 100000000
            for flight in self.cities_reverse_connect[end_city]:
                if visited[flight.flight_no]:
                    if distance[flight.flight_no] < curr_best:
                        if len(best_route)==0 or best_route[-1].departure_time >= flight.arrival_time + 20:
                            best_flight = flight
                            curr_best = distance[flight.flight_no]
                        #best_time = flight.arrival_time
                    # elif curr_best == distance[flight.flight_no] and flight.arrival_time < best_time:
                    #     best_flight = flight
                    #     curr_best = distance[flight.flight_no]
                    #     best_time = flight.arrival_time
            end_city = best_flight.start_city
            best_route.append(best_flight)
        best_route.reverse()
        return best_route








        pass
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        dist = [(1e9, 1e9)] * (self.flights_max_index + 1)
        pri_queue = priority_queue_by_heap()
        for flight in self.cities_connect[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                pri_queue.insert(Node((0, flight.fare), flight))
                dist[flight.flight_no] = (0, flight.fare)
        visited = [False] * (self.flights_max_index + 1)
        while pri_queue.size() > 0:
            top_most = pri_queue.extract()
            current_flight = top_most.value
            if visited[current_flight.flight_no]:
                continue
            visited[current_flight.flight_no] = True
            cur_dist = top_most.key
            for next_flight in self.flights_graph[current_flight.flight_no]:
                add_dist = next_flight.fare
                if(next_flight.arrival_time <= t2) and (dist[next_flight.flight_no] > (cur_dist[0] + 1, cur_dist[1] + add_dist)):
                    dist[next_flight.flight_no] = (cur_dist[0] + 1, cur_dist[1] + add_dist)
                    pri_queue.insert(Node(dist[next_flight.flight_no], next_flight))
        best_route = []
        cur_end_city = end_city
        not_exists = True
        for flight in self.cities_reverse_connect[end_city]:
            if visited[flight.flight_no]:
                not_exists = False
                break
        if not_exists:
            return []
        #print(dist)
        while end_city != start_city:
            best_flight = None
            curr_best = (1e9, 1e9)
            for flight in self.cities_reverse_connect[end_city]:
                if visited[flight.flight_no]:
                    if dist[flight.flight_no] < curr_best:
                        if len(best_route)==0 or best_route[-1].departure_time >= flight.arrival_time + 20:
                            best_flight = flight
                            curr_best = dist[flight.flight_no]
            end_city = best_flight.start_city
            best_route.append(best_flight)
        best_route.reverse()

        return best_route






class CircularQueue:
    def __init__(self, capacity):
        self._data = [None] * capacity
        self._capacity = capacity
        self._size = 0
        self._front = 0
        self._rear = -1

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def first(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[self._front]

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def enqueue(self, value):
        if self.is_full():
            raise IndexError("Queue is full")
        self._rear = (self._rear + 1) % self._capacity
        self._data[self._rear] = value
        self._size += 1








'''
    Python Code to implement a heap with general comparison function
'''

class Node:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value

def comp(node1, node2):
        if node1.key < node2.key:
            return True
        return False

class Heap:
        '''
        Class to implement a heap with general comparison function
        '''

        def __init__(self, comparison_function, init_array):
            '''
            Arguments:
                comparison_function : function : A function that takes in two arguments and returns a boolean value
                init_array : List[Any] : The initial array to be inserted into the heap
            Returns:
                None
            Description:
                Initializes a heap with a comparison function
                Details of Comparison Function:
                    The comparison function should take in two arguments and return a boolean value
                    If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                    If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
            Time Complexity:
                O(n) where n is the number of elements in init_array
            '''
            self.compare = comparison_function
            self.heap = []
            for i in init_array:
                self.heap.append(i)

            for i in range(len(self.heap) // 2 - 1, -1, -1):
                left = 2 * i + 1
                right = 2 * i + 2
                j = len(self.heap)
                if right < len(self.heap):
                    if self.compare(self.heap[right], self.heap[left]):
                        if self.compare(self.heap[right], self.heap[i]):
                            self.heap[right], self.heap[i] = self.heap[i], self.heap[right]
                            j = right

                    else:
                        if self.compare(self.heap[left], self.heap[i]):
                            self.heap[left], self.heap[i] = self.heap[i], self.heap[left]
                            j = left
                else:
                    if left < len(self.heap):
                        if self.compare(self.heap[left], self.heap[i]):
                            self.heap[left], self.heap[i] = self.heap[i], self.heap[left]
                            j = left

                while j < len(self.heap):
                    left = 2 * j + 1
                    right = 2 * j + 2
                    if right < len(self.heap):
                        if self.compare(self.heap[right], self.heap[left]):
                            if self.compare(self.heap[right], self.heap[j]):
                                self.heap[right], self.heap[j] = self.heap[j], self.heap[right]
                                j = right
                                continue

                        else:
                            if self.compare(self.heap[left], self.heap[j]):
                                self.heap[left], self.heap[j] = self.heap[j], self.heap[left]
                                j = left
                                continue
                    else:
                        if left < len(self.heap):
                            if self.compare(self.heap[left], self.heap[j]):
                                self.heap[left], self.heap[j] = self.heap[j], self.heap[left]
                                j = left
                                continue
                    j = len(self.heap)
            # Write your code here

        def insert(self, value):
            '''
            Arguments:
                value : Any : The value to be inserted into the heap
            Returns:
                None
            Description:
                Inserts a value into the heap
            Time Complexity:
                O(log(n)) where n is the number of elements currently in the heap
            '''

            # Write your code here
            self.heap.append(value)
            i = len(self.heap) - 1
            while i > 0:
                parent = (i - 1) // 2
                if self.compare(self.heap[i], self.heap[parent]):
                    self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                    i = parent
                else:
                    break

        def extract(self):
            '''
            Arguments:
                None
            Returns:
                Any : The value extracted from the top of heap
            Description:
                Extracts the value from the top of heap, i.e. removes it from heap
            Time Complexity:
                O(log(n)) where n is the number of elements currently in the heap
            '''

            if len(self.heap) == 0:
                return None
            if len(self.heap) == 1:
                return self.heap.pop()

            # Swap the root with the last element and remove the last element
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            value = self.heap.pop()

            # Heapify down from the root
            i = 0
            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                smallest = i

                if left < len(self.heap) and self.compare(self.heap[left], self.heap[smallest]):
                    smallest = left
                if right < len(self.heap) and self.compare(self.heap[right], self.heap[smallest]):
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                    i = smallest
                else:
                    break

            return value

        def top(self):
            '''
            Arguments:
                None
            Returns:
                Any : The value at the top of heap
            Description:
                Returns the value at the top of heap
            Time Complexity:
                O(1)
            '''

            # Write your code here
            if len(self.heap) == 0:
                return None
            return self.heap[0]

        def size(self):
            return len(self.heap)

        # You can add more functions if you want to


class priority_queue_by_heap:
    def __init__(self):
        self.heap = Heap(comp, [])
        self.compare = comp

    def insert(self, value):
        self.heap.insert(value)

    def extract(self):
        return self.heap.extract()

    def top(self):
        return self.heap.top()

    def size(self):
        return self.heap.size()

    # You can add more functions if you want to
