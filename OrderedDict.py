class Link:
    __slots__ = 'prev', 'next', 'key'


class OrderedDict:
    def __init__(self):
        self.root = Link()
        self.map = {}
        self._node_map = {}
        self.root.next = self.root
        self.root.prev = self.root

    def __setitem__(self, key, value):
        if key in self._node_map:
            self.map[key] = value
        else:
            root = self.root
            last = root.prev
            link = Link()
            link.prev, link.next, link.key = last, root, key
            last.next = link
            root.prev = link
            self._node_map[key] = link
            self.map[key] = value

    def __getitem__(self, item):
        return self.map[item]

    def __delitem__(self, key):
        del self.map[key]
        link = self._node_map.pop(key)
        link_prev, link_next = link.prev, link.next
        link_prev.next, link_next.prev = link_next, link_prev
        link.prev, link.next = None, None

    def pop(self):
        """
        LIFO
        :return:
        """
        if not self._node_map:
            raise KeyError('dict is empty')
        root = self.root
        link = root.prev
        link_prev = link.prev
        link_prev.next = root
        root.prev = link_prev
        link.prev, link.next = None, None
        self._node_map.pop(link.key)
        return self.map.pop(link.key)

    def __iter__(self):
        root = self.root
        curr = root.next
        while curr != root:
            yield curr.key
            curr = curr.next

    def values(self):
        root = self.root
        curr = root.next
        while curr != root:
            yield self.map[curr.key]
            curr = curr.next

    def __str__(self):
        root = self.root
        curr = root.next
        out = []
        while curr != root:
            out.append((curr.key, self.map[curr.key]))
            curr = curr.next
        return str(out)

    def __len__(self):
        return len(self.map)

if __name__ == '__main__':
    d = OrderedDict()
    d['a'] = '1'
    d['b'] = '2'
    d['c'] = '3'    
    print(d)