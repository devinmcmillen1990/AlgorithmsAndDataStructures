class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

'''
print('Node 1')
node1 = Node(1)
print(f'Value       = {node1.value}')
print(f'Next        = {node1.next}')
print()

print('Node 2')
node2 = Node(2, node1)
print(f'Value       = {node2.value}')
print(f'Next        = {node2.next}')
print(f'Next.Value  = {node2.next.value}')
print()
'''