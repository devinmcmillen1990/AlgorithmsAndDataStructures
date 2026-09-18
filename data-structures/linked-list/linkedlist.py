from node import Node

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def append(self, value):
        prev = self.tail
        new_node = Node(value)
        prev.next = new_node
        self.tail = new_node

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next


print(f'Linked List 11->3->23->7')
my_linked_list = LinkedList(11)
my_linked_list.append(3)
my_linked_list.append(23)
my_linked_list.append(7)

my_linked_list.print_list()
