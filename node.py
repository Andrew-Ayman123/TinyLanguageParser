class Node:
    def __init__(self, data="", isSqare=True) -> None:
        self.children: list[Node] = []
        self.next: Node = None  # showing the next stattment
        self.is_square: bool = isSqare
        self.data: str = data

    def addChild(self, child: "Node"):
        self.children.append(child)

    def setNext(self, next: "Node"):
        self.next = next


########### Functions to create specific nodes ##############


'''Takes as input the identifier of the variable being read and returns a node representing the read statement'''
def createReadNode(identifier: str) -> Node:
    node = Node(f"read({identifier})", True)
    return node

'''Takes as input the identifier of the variable being assigned returns a node representing the assign statement'''
def createAssignNode(identifier: str) -> Node:
    node = Node(f"assign({identifier})", True)
    return node

'''Creates a node representing the write statement'''
def createWriteNode() -> Node:
    node = Node("write", True)
    return node

'''Creates a node representing the if statement'''
def createIfNode() -> Node:
    node = Node("if", True)
    return node

'''Creates a node representing the repeat statement'''
def createRepeatNode() -> Node:
    node = Node("repeat", True)
    return node

'''Take as input the operator involved in an OP and returns a node representing the operator'''
def createOpNode(operator: str) -> Node:
    node = Node(f"op({operator})", False)
    return node

'''Takes as input the identifier of the variable involved in an OP returns a node representing the variable'''
def createIDNode(identifier: str) -> Node:
    node = Node(f"id({identifier})", False)
    return node

'''Takes as input the value of the constant involved in an OP returns a node representing the constant'''
def createConstNode(value: str) -> Node:
    node = Node(f"const({value})", False)
    return node
