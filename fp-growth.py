import itertools
from collections import defaultdict
import numpy as np


class Node:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None


def build(items, count, min_count):
    next = Node('', 1, None)
    table = defaultdict(int)

    for i, item in enumerate(items):
        for item1 in item:
            table[item1] += count[i]

    table1 = dict((item, count) for item, count in table.items() if count >= min_count)

    if len(table1) == 0:
        return None, None

    for item in table1:
        table1[item] = [table1[item], None]

    for i, items in enumerate(items):
        items2 = [item1 for item1 in items if item1 in table1]
        items2.sort(key=lambda ind: table1[ind][0], reverse=True)
        node = next
        for item1 in items2:
            node = update(item1, node, table1, count[i])

    return next, table1


def update(new, curr, table, count):  # fix
    if new in curr.children:
        curr.children[new].count += count
    else:
        curr.children[new] = Node(new, count, curr)
        update_table(new, curr.children[new], table)
    return curr.children[new]


def update_table(item, node, table):
    if table[item][1] is None:
        table[item][1] = node
    else:
        ptr = table[item][1]
        while ptr.next is not None:
            ptr = ptr.next
        ptr.next = node


def get_path(node, path):
    if node.parent is not None:
        path.append(node.item)
        get_path(node.parent, path)


def base(nodeName, table):
    bases = []
    count = []
    node = table[nodeName][1]
    while node is not None:
        path = []
        get_path(node, path)
        if len(path) > 1:
            bases.append(path[1:])
            count.append(node.count)
        node = node.next
    return bases, count


def rules(table, min_count, counts, item_count):
    sorted_list = [item[0] for item in sorted(list(table.items()), key=lambda p: p[1][0])]
    for item in sorted_list:
        new_freq = counts.copy()
        new_freq.add(item)
        item_count.append(new_freq)
        # cond_pattern_base, frequency = base(item, table)
        bases = []
        count = []
        node = table[item][1]
        while node is not None:
            path = []
            get_path(node, path)
            if len(path) > 1:
                bases.append(path[1:])
                count.append(node.count)
            node = node.next
        cond_tree, f_table = build(bases, count, min_count)
        if f_table is not None:
            rules(f_table, min_count, new_freq, item_count)


def associ(counts, items, conf):
    rules = []
    for item in counts:
        item1 = itertools.chain.from_iterable(itertools.combinations(item, i) for i in range(1, len(item)))
        # support = get_num(item, items)
        support = 0
        for item2 in items:
            if set(item).issubset(item2):
                support += 1
        for i in item1:
            support1 = 0
            for item2 in items:
                if set(i).issubset(item2):
                    support1 += 1
            if float(support / support1) > conf:
                rules.append([set(i), set(item.difference(i)), float(support / support1)])
    return rules


def printm(matrix):
    print(np.asmatrix(matrix))


def main():
    dataset = [['Bread', 'Milk'],
               ['Bread', 'Diaper', 'Beer', 'Eggs'],
               ['Milk', 'Diaper', 'Beer', 'Coke'],
               ['Bread', 'Milk', 'Diaper', 'Beer'],
               ['Bread', 'Milk', 'Diaper', 'Coke']]
    counts = len(dataset) * [1]
    min_count = 0.4 * len(dataset)

    tree, table = build(dataset, counts, min_count=0.4)

    counts = []
    rules(table, min_count, set(), counts)

    printm(associ(counts, dataset, conf=0.6))


main()
