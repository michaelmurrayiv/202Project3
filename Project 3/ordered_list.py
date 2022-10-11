class Node:
    """Node for use with doubly-linked list"""

    def __init__(self, item):
        self.item = item
        self.next = None  # towards head, decreasing values
        self.prev = None  # towards tail, increasing values


class OrderedList:
    """A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)"""

    def __init__(self):
        """Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size"""

        self.dummy = Node('dummy')

    def is_empty(self):
        """Returns True if OrderedList is empty
            MUST have O(1) performance"""
        if (self.dummy.next is None and self.dummy.prev is None) or self.dummy.next == self.dummy:
            return True
        return False

    def add(self, item):
        """Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance"""

        if self.is_empty():  # if the list is only the dummy, add item as a node connected to the dummy
            new_node = Node(item)
            self.dummy.next = new_node
            self.dummy.prev = new_node
            new_node.next = self.dummy
            new_node.prev = self.dummy
            return True

        else:  # if the list already has items, need to search the list for the right spot for item
            stop = False
            added = False
            current = self.dummy.next
            new = Node(item)

            while not stop:
                if item == current.item:  # if the item is already in the list, don't add it and return False
                    added = False
                    stop = True
                elif item < current.item:  # if a spot has been found in the list,
                    # break the link and insert the new node. Return True
                    last = current.prev

                    last.next = new
                    current.prev = new
                    new.next = current
                    new.prev = last
                    added = True
                    stop = True
                elif current.next == self.dummy:  # if item is larger than the rest of the list, add it to the end
                    current.next = new
                    self.dummy.prev = new
                    new.next = self.dummy
                    new.prev = current
                    added = True
                    stop = True
                elif item > current.item:  # if the item is not in the right spot, check the next spot
                    current = current.next

            return added

    def remove(self, item):
        """Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
          returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance"""

        index = self.index(item)  # use index to find if the item is in the list, and where
        if index is None:
            return False
        self.pop(index)  # use pop to remove the item if present in the list
        return True

    def index(self, item):
        """Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance"""
        if self.is_empty():
            return None

        stop = False
        index = 0
        current = self.dummy.next

        while not stop:  # add 1 to the index every time .next is called, until the value is reached.
            # If the end of the list is reached first, return False
            if current.item == item:
                stop = True
            elif current.next == self.dummy:
                index = None
                stop = True
            else:
                current = current.next
                index += 1
        return index

    def pop(self, index):
        """Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance"""

        if index < 0 or index >= self.size():  # invalid inputs
            raise IndexError

        current = self.dummy.next
        for i in range(index):
            current = current.next

        pop = current.item

        prev_link = current.prev
        next_link = current.next
        prev_link.next = next_link # connect the links on both sides of the pop value to each other
        next_link.prev = prev_link

        return pop

    def search(self, item):
        """Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance"""
        if self.is_empty():
            return False

        return self.recursive_search(item, self.dummy.next)  # call the recursive method to search for the item

    def python_list(self):
        """Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance"""
        result = []
        stop = False

        if self.is_empty():
            return result

        current = self.dummy.next

        while not stop:  # until the end of the list is reached, append each item to the list

            result.append(current.item)

            if current.next == self.dummy:
                stop = True
            else:
                current = current.next
        return result

    def python_list_reversed(self):
        """Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance"""

        if self.is_empty():
            return []
        result = []
        # calls the recursive method to produce a reversed list
        return self.recursive_list_reversed(self.dummy.prev, result)

    def size(self):
        """Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance"""

        if self.is_empty():
            return 0
        else:
            return self.recursive_size(self.dummy.next)  # calls the recursive method to determine the list size

    def recursive_search(self, item, current):
        """Recursive method for the search function. Searches OrderedList for item,
        returns True if item is in list, False otherwise."""
        if current.item == item:  # end conditions: if the item is found, return true, and if not return False
            return True
        elif current.next == self.dummy:
            return False
        return self.recursive_search(item, current.next)

    def recursive_size(self, current):
        if current.next == self.dummy:  # end condition: reached the end of the list
            return 1
        current = current.next
        return self.recursive_size(current) + 1  # add 1 for each item traversed

    def recursive_list_reversed(self, tail, result):
        if tail.prev == self.dummy:  # end condition: when the whole list has been traversed, return it
            result.append(tail.item)
            return result
        result.append(tail.item)  # append the next highest value to the result list
        return self.recursive_list_reversed(tail.prev, result)
