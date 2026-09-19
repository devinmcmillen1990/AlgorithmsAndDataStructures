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


    def set_value(self, index, value):
        if index > self.length or index < 0:
            return False
        node = self.get(index)
        node.value = value
        return True


    def insert(self, index, value):
        if index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1) # Grab node before index
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1
        return True


    def remove(self, index):
        if index > self.length or index < 0:
            return False
        if index == 0:
            head = self.head
            self.head = head.next if head is not None else None
            return True
        if index == self.length:
            new_tail = self.get(self.length - 1)
            self.tail = new_tail
            return True
        temp = self.get(index - 1)
        temp.next = temp.next.next
        return True
        


    def reverse(self):
        pass


    def print_list(self):
        current = self.head
        to_print = []
        while current is not None:
            to_print.append(current.value)
            current = current.next
        print(to_print)


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
print(f'search(0)   -> {my_linked_list.search(0)[0]}')

print()

print(f'Linked List: Get')
print(f'get(0)      -> {my_linked_list.get(0).value}')
print(f'get(1)      -> {my_linked_list.get(1).value}')
print(f'get(2)      -> {my_linked_list.get(2).value}')
print(f'get(3)      -> {my_linked_list.get(3).value}')
print(f'get(4)      -> {my_linked_list.get(4).value}')
print(f'get(5)      -> {my_linked_list.get(5)}')

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

print()

print(f'Linked List: Insert')
print(f'insert(0, 1)')
my_linked_list.insert(0, 1)
print(f'insert(1, 2)')
my_linked_list.insert(1, 2)
print(f'insert(0, 0)')
my_linked_list.insert(0, 0)
print(f'insert(3,4)')
my_linked_list.insert(3, 4)
my_linked_list.print_list()

print()

print(f'Linked List: Remove')
my_linked_list.print_list()
print(f'remove(3)')
my_linked_list.remove(3)
my_linked_list.print_list()
print(f'remove(2)')
my_linked_list.remove(2)
my_linked_list.print_list()
print(f'remove(1)')
my_linked_list.remove(1)
my_linked_list.print_list()
print(f'remove(0)')
my_linked_list.remove(0)
my_linked_list.print_list()

print()

my_linked_list.insert(0, 1)
my_linked_list.insert(1, 2)
my_linked_list.insert(0, 0)
my_linked_list.insert(3, 4)
print(f'Linked List: Remove')
my_linked_list.print_list()
print(f'remove(0)')
my_linked_list.remove(0)
my_linked_list.print_list()
print(f'remove(0)')
my_linked_list.remove(0)
my_linked_list.print_list()
print(f'remove(0)')
my_linked_list.remove(0)
my_linked_list.print_list()
print(f'remove(0)')
my_linked_list.remove(0)
my_linked_list.print_list()
