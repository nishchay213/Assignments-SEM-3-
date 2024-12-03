import hash_table as ht
import dynamic_hash_table as dht


class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass

    def distinct_words(self, book_title):
        pass

    def count_distinct_words(self, book_title):
        pass

    def search_keyword(self, keyword):
        pass

    def print_books(self):
        pass


class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):

        super().__init__()
        books = []
        books_tuple_with_count = []
        books_with_dist_words = []
        for i in range(len(book_titles)):
            books.append([book_titles[i], []])
            texts_2 = self.merge_sort(texts[i])

            count1 = self.count(texts_2)
            books_tuple_with_count.append((book_titles[i], count1))
            books_with_dist_words.append((book_titles[i], self.dist(texts_2)))

            books[-1][1] = texts_2

        self.books = self.merge_sort(books)
        self.books_tuple_with_count = self.merge_sort(books_tuple_with_count)
        self.books_with_dist_words = self.merge_sort(books_with_dist_words)

    def find_book(self, book_title):
        # binary search for book
        left = 0
        right = len(self.books) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.books[mid][0] == book_title:
                return mid
            elif self.books[mid][0] < book_title:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def dist(self, word_list):
        distinct = []
        for word in word_list:
            if distinct == [] or distinct[-1] != word:
                distinct.append(word)
        return distinct

    def count(self, word_list):
        count = 0
        for i in range(len(word_list)):
            if i == 0 or word_list[i] != word_list[i - 1]:
                count += 1
        return count

    def distinct_words(self, book_title):
        book_index = self.find_book(book_title)
        if book_index == -1:
            return []
        return self.books_with_dist_words[book_index][1]

    def count_distinct_words(self, book_title):
        book_index = self.find_book(book_title)
        if book_index == -1:
            return 0
        return self.books_tuple_with_count[book_index][1]

    def keyword_exists(self, keyword, book_title):
        book_index = self.find_book(book_title)
        if book_index == -1:
            return False
        left = 0
        right = len(self.books[book_index][1]) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.books[book_index][1][mid] == keyword:
                return True
            elif self.books[book_index][1][mid] < keyword:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def search_keyword(self, keyword):
        books = []
        for book in self.books:
            if self.keyword_exists(keyword, book[0]):
                books.append(book[0])
        return books

    def print_books(self):
        for book in self.books:
            print(f"{book[0]}", end=": ")
            for word in self.distinct_words(book[0]):

                if word == book[1][-1]:

                    print(word, end="")
                else:
                    print(word, end=" | ")
            print()

    def merge(self, list1, list2):
        i1 = 0
        i2 = 0
        merged = []
        while i1 < len(list1) and i2 < len(list2):
            if list1[i1] < list2[i2]:
                merged.append(list1[i1])
                i1 += 1
            else:
                merged.append(list2[i2])
                i2 += 1
        while i1 < len(list1):
            merged.append(list1[i1])
            i1 += 1
        while i2 < len(list2):
            merged.append(list2[i2])
            i2 += 1
        return merged

    def merge_sort(self, lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = self.merge_sort(lst[0:mid])
        right = self.merge_sort(lst[mid:])
        return self.merge(left, right)


class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function

            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        super().__init__()
        self.name = name
        self.params = params
        self.books_list = []

        if name == "Jobs":
            self.collision = "Chain"
            # self.table = dht.DynamicHashMap("Chain", params)
            self.book_table = ht.HashMap("Chain", params)

        elif name == "Gates":
            self.collision = "Linear"
            # self.table = dht.DynamicHashMap("Linear", params)
            self.book_table = ht.HashMap("Linear", params)


        else:
            self.collision = "Double"
            # self.table = dht.DynamicHashMap("Double", params)
            self.book_table = ht.HashMap("Double", params)

    def add_book(self, book_title, text):
        hash_table = ht.HashSet(self.collision, self.params)
        dist_words = []
        for word in text:
            # self.table.insert((word, book_title))
            if hash_table.find(word) == False:
                dist_words.append(word)
            hash_table.insert(word)

        self.book_table.insert((book_title, hash_table))
        self.books_list.append(book_title)

    def distinct_words(self, book_title):

        distinct = []
        book_hash = self.book_table.find(book_title)
        if book_hash == None:
            return []
        for word in book_hash.table:

            if word is not None:
                if type(word) == list:
                    for w in word:
                        distinct.append(w)
                else:
                    distinct.append(word)
        return distinct

    def count_distinct_words(self, book_title):
        book_hash = self.book_table.find(book_title)
        if book_hash == None:
            return 0
        else:
            return book_hash.size

    def search_keyword(self, keyword):
        books = []
        for title in self.books_list:
            book_hash = self.book_table.find(title)
            if book_hash == None:
                continue
            if book_hash.find(keyword) == True:
                books.append(title)
        return books

        # for k in self.table.find(keyword):
        #
        #     books.append(k)
        # return books

    def print_books(self):
        for book in self.books_list:
            book_hash = self.book_table.find(book)
            print(f"{book}", end=": ")
            print(book_hash)









