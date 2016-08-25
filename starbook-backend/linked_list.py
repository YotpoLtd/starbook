from node import Node


class LinkedList:
    def __init__(self):
        self.size = 0
        self.first = None
        self.last = None

    def push_first(self, new_node):
        self.size += 1
        if self.size == 1:
            self.first = new_node
            self.last = new_node
            new_node.prev = None
            new_node.next = None
            return

        new_node.next = self.first
        new_node.prev = None
        self.first.prev = new_node
        self.first = new_node

    def pop_last(self):
        if self.size == 0:
            return
        elif self.size == 1:
            self.size = 0
            pop = self.last
            pop.next = None
            pop.prev = None
            self.first = None
            self.last = None
            return pop

        self.size -= 1
        pop = self.last
        self.last = pop.prev
        pop.prev = None
        pop.next = None
        self.last.next = None
        return pop

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.first is node:
            self.first = node.next
        if self.last is node:
            self.last = node.prev

        node.next = None
        node.prev = None
        self.size -= 1

    def print(self):
        print('\n\nsize:{}\nforward:'.format(self.size))
        curr = self.first
        while curr:
            print('{}, '.format(curr.data), end='')
            curr = curr.next

        print('\nbackwards:')
        curr = self.last
        while curr:
            print('{}, '.format(curr.data), end='')
            curr = curr.prev

if __name__ == '__main__':
    ll = LinkedList()
    ll.pop_last()
    nodes = {}
    for i in range(5):
        name = 'node{}'.format(i)
        n = Node(name)
        nodes[name] = n
        n.data = 'data{}'.format(i)
        ll.push_first(n)
        ll.print()

    while len(nodes):
        name, node = nodes.popitem()
        ll.remove(node)
        ll.print()

