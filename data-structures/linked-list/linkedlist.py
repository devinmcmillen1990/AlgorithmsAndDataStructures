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


    '''
    Search for a value in the linked list.

    Returns a tuple containing the node and its index if found, otherwise returns (None, -1).
    '''
    def search(self, value) -> tuple:
        if self.length == 0:
            return (None, -1)            
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return (current, index)
            current = current.next
            index += 1
        return (None, -1)

    
    def get(self, index):
        if self.length == 0 or index < 0 or index >= self.length:
            return None
        current = self.head
        position = 0
        while current is not None and position < index:
            current = current.next
            position += 1
        return current
        

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

print(f'Linked List: Search')
print(f'search(500) -> {my_linked_list.search(500)[0].value}')
print(f'search(11)  -> {my_linked_list.search(11)[0].value}')
print(f'search(3)   -> {my_linked_list.search(3)[0].value}')
print(f'search(23)  -> {my_linked_list.search(23)[0].value}')
print(f'search(7)   -> {my_linked_list.search(7)[0].value}')

print()

print(f'Linked List: Get')
print(f'get(0) -> {my_linked_list.get(0).value}')
print(f'get(1) -> {my_linked_list.get(1).value}')
print(f'get(2) -> {my_linked_list.get(2).value}')
print(f'get(3) -> {my_linked_list.get(3).value}')
print(f'get(4) -> {my_linked_list.get(4).value}')

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
print(f'Updated list after all popped:')
my_linked_list.print_list()