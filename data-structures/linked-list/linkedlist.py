from node import Node

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True

    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return True

    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
            self.length = 0
        else:
            self.head = temp.next
            self.length -= 1
        return temp

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next


print(f'Linked List: Append 11->3->23->7')
my_linked_list = LinkedList(11)
my_linked_list.append(3)
my_linked_list.append(23)
my_linked_list.append(7)
my_linked_list.print_list()

print()

print(f'Linked List: Prepend')
my_linked_list.prepend(500)
my_linked_list.print_list()

print()

print(f'Linked List: Pop One')
popped = my_linked_list.pop()
print(f'Popped {popped.value}')
print(f'Updated list:')
my_linked_list.print_list()

print()

print(f'Linked List: Pop All')
while my_linked_list.length > 0:
    popped = my_linked_list.pop()
    print(f'Popped {popped.value}')
print(f'Updated list:')
my_linked_list.print_list()