class Node:
  # O (1)
    def __init__(self, initial_data):
        self.data = initial_data
        self.next = None


class LinkedList:
  # O(1)
    def __init__(self):
        self.head = None
        self.tail = None

    # O(1)
    def append(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # O(1)
    def prepend(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    # O(1)
    def insert_after(self, current_node, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif current_node is self.tail:
            self.tail.next = new_node
            self.tail = new_node
        else:
            new_node.next = current_node.next
            current_node.next = new_node

    # O(1)
    def remove_after(self, current_node):
        if (current_node is None) and (self.head is not None):
            succeeding_node = self.head.next
            self.head = succeeding_node
            if succeeding_node is None:
                self.tail = None
        elif current_node.next is not None:
            succeeding_node = current_node.next
            current_node.next = succeeding_node
            if succeeding_node is None:
                self.tail = current_node


"""
Finish the methods needed for the Queue class, and the breadth first search in the graph
"""


class Queue:
   #O(1)
    def __init__(self):
        self.list = LinkedList()

    #O(1)
    def push(self, new_item):
        self.list.append(new_item)  # Insert as list tail (end of queue)

    #O(1)
    def pop(self):
        popped_item = self.list.head  # Copy list head (front of queue)
        self.list.remove_after(None)  # Remove list head
        return popped_item
