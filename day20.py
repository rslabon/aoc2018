class Node:
    def __init__(self):
        self.value = ""
        self.children = []

    def leaf(self):
        if len(self.children) == 0:
            return [self]

        result = []
        for child in self.children:
            result += child.leaf()

        return result

    def __repr__(self):
        return f"Node({self.value})"


def parse_node(pattern, current, parent):
    while pattern:
        if pattern[0] in ["E", "W", "S", "N"]:
            direction = pattern.pop(0)
            current.value += direction
        elif pattern and pattern[0] == '(':
            pattern.pop(0)
            child = Node()
            current.children.append(child)
            parse_node(pattern, child, current)
            if pattern and pattern[0] != ')':
                leafs = current.leaf()
                for leaf in leafs:
                    n = Node()
                    leaf.children.append(n)
                    parse_node(pattern[:], n, leaf)
                return
        elif pattern and pattern[0] == '|':
            pattern.pop(0)
            sibling = Node()
            parent.children.append(sibling)
            current = sibling
        elif pattern and pattern[0] == ')':
            pattern.pop(0)
            return


grid = set()
pattern = "NENNEEEENN(E|(W|)|S|E)"
root = Node()
parse_node(list(pattern), root, None)
print(root)
