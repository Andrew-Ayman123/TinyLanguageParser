class Node:
  def __init__(self,data="") -> None:
    self.children:list[Node]=[]
    self.next:Node=None # showing the next stattment
    self.is_square:bool=True
    self.data:str=data

def generate_structure()->Node:
  # Create the root node
  root = Node("read\n(x)")

  # Create child nodes for the root node
  op_node = Node("op\n<-")
  op_node.is_square=False
  assign_node = Node("assign\n(fact)")
  root.children.append(op_node)
  root.children.append(assign_node)

  # Create child nodes for the op_node
  const_node1 = Node("const\n(0)")
  id_node1 = Node("id\n(x)")
  op_node.children.append(const_node1)
  op_node.children.append(id_node1)

  # Create child nodes for the assign_node
  const_node2 = Node("const\n(1)")
  assign_node.children.append(const_node2)

  # Create a repeat node and connect it to the assign_node
  repeat_node = Node("repeat")
  assign_node.next = repeat_node

  # Create child nodes for the repeat_node
  assign_node2 = Node("assign\n(x)")
  op_node2 = Node("op\n=")
  op_node2.is_square=False
  repeat_node.children.append(assign_node2)
  repeat_node.children.append(op_node2)

  # Create child nodes for the op_node2
  id_node2 = Node("id\n(x)")
  const_node3 = Node("const\n(1)")
  op_node2.children.append(id_node2)
  op_node2.children.append(const_node3)

  # Create a write node and connect it to the repeat_node
  write_node = Node("write")
  repeat_node.next = write_node

  # Create child nodes for the write_node
  id_node3 = Node("id\n(fact)")
  write_node.children.append(id_node3)
  return root