from itertools import repeat

from node import *

list_of_tokens = [
    ("read", "READ"),

]
counter = 0

def is_empty(list):
    return len(list) == 0


def peek_Type():
    if list_of_tokens:
        return list_of_tokens[0][1]
    return None


def peek_Value():
    if list_of_tokens:
        return list_of_tokens[0][0]
    return None


def next_token():
    if list_of_tokens:
        return list_of_tokens[0]


def match(expected_token_type):
    global counter
    if not list_of_tokens:
        return createErrorNode("Error, expected " + expected_token_type + " but got nothing"+" at line number "+str(counter))
    if list_of_tokens[0][1] == expected_token_type:
        list_of_tokens.pop(0)
        counter+=1
        return True
    else:
        return createErrorNode("Error, expected " + expected_token_type + " but got " + list_of_tokens[0][1] + " at line number "+str(counter))


def program():
    child = stmtSequence()
    if child != "ERROR":
        return child
    else:
        return "ERROR"
        # statement{;statement}


def stmtSequence():
    root = statement()
    temp = root
    token_type = peek_Type()
    while token_type == "SEMICOLON":
        match_result = match("SEMICOLON")
        if match_result != True:
            return match_result
        new_stmt = statement()
        temp.setNext(new_stmt)
        temp = new_stmt
        token_type = peek_Type()
    return root
    # statament -> if-stmt | repeat-stmt | assign-stmt |read-stmt |  write-stmt


def statement():
    if peek_Type() == "IF":
        tmp = if_stmt()
    elif peek_Type() == "REPEAT":
        tmp = repeat_stmt()
    elif peek_Type() == "READ":
        tmp = read_stmt()
    elif peek_Type() == "WRITE":
        tmp = write_stmt()
    elif peek_Type() == "IDENTIFIER":
        tmp = assign_stmt()
    else:
        return "ERROR"

    return tmp


# if -stmt → if exp then stmt-sequence end
def if_stmt():
    match_result = match("IF")
    if match_result != True:
        return match_result
    if_node = createIfNode()
    exp_node = exp()
    if_node.addChild(exp_node)
    match_result = match("THEN")
    if match_result != True:
        return match_result
    stmt_node = stmtSequence()
    if_node.addChild(stmt_node)

    if peek_Type() == "ELSE":
        match_result = match("ELSE")
        if match_result != True:
            return match_result
        stmt_node = stmtSequence()
        if_node.addChild(stmt_node)

    match_result = match("END")
    if match_result != True:
        return match_result

    return if_node


# comparison-op -> = | <
def comparison_op():
    token_t = peek_Type()
    token_val = peek_Value()
    match_result = match(token_t)
    if match_result != True:
        return match_result
    op_node = createOpNode(token_val)
    return op_node


# simple-exp -> term {addop term}
def simple_exp():
    temp = term()
    nodeTerm = temp
    # token_d=next_token()
    token_type = peek_Type()
    while token_type == "PLUS" or token_type == "MINUS":
        nodeOp = addop()
        nodeOp.addChild(temp)
        nodeTerm2 = term()
        nodeOp.addChild(nodeTerm2)
        token_type = peek_Type()
        temp = nodeOp

    nodeTerm = temp
    return nodeTerm


# addop -> + | -
def addop():
    token_t = peek_Type()
    token_val = peek_Value()
    match_result = match(token_t)
    if match_result != True:
        return match_result
    op_node = createOpNode(token_val)
    return op_node


# term -> factor {mulop factor}
def term():
    node_factor = factor()
    token_type = peek_Type()
    while token_type == "MULT" or token_type == "DIV":
        nodeOp = mulop()
        nodeOp.addChild(node_factor)
        nodeTerm2 = factor()
        nodeOp.addChild(nodeTerm2)
        token_type = peek_Type()
        node_factor = nodeOp

    return node_factor


# mulop -> * | /
def mulop():
    token_t = peek_Type()
    token_val = peek_Value()
    match_result = match(token_t)
    if match_result != True:
        return match_result
    op_node = createOpNode(token_val)
    return op_node


def factor():
    node_temp = None

    # Check the type of the current token
    token_type = peek_Type()
    token_val = peek_Value()

    if token_type == "OPENBRACKET":
        match_result = match(token_type)
        if match_result != True:
            return match_result
        node_exp = exp()
        node_temp = node_exp
        match_result = match("CLOSEBRACKET")
        if match_result != True:
            return match_result

    elif token_type == "NUMBER":
        match_result = match(token_type)
        if match_result != True:
            return match_result
        node_temp = createConstNode(token_val)
    elif token_type == "IDENTIFIER":
        match_result = match(token_type)
        if match_result != True:
            return match_result
        node_temp = createIDNode(token_val)
    else:
        return createErrorNode("ERROR, expected NUMBER, IDENTIFIER or OPENBRACKET but got " + token_type)
    return node_temp


# repeat->stmt-sequence until exp
def repeat_stmt():
    match_result = match("REPEAT")
    if match_result != True:
        return match_result
    r_node = createRepeatNode()
    stmt_node = stmtSequence()
    r_node.addChild(stmt_node)
    match_result = match("UNTIL")
    if match_result != True:
        return match_result
    exp_node = exp()
    r_node.addChild(exp_node)

    return r_node


# read - > read identifer
def read_stmt():
    match_result = match("READ")
    if match_result != True:
        return match_result
    identifier = peek_Value()
    match_result = match("IDENTIFIER")
    if match_result != True:
        return match_result
    read_node = createReadNode(identifier)

    return read_node


# write -> write exp
def write_stmt():
    match_result = match("WRITE")
    if match_result != True:
        return match_result
    w_root = createWriteNode()
    expNode = exp()
    w_root.addChild(expNode)

    return w_root


# assignStmt -> Identifier := exp
def assign_stmt():
    token, token_t = next_token()
    match_result = match("IDENTIFIER")
    if match_result != True:
        return match_result
    assign_node = createAssignNode(token)

    match_result = match("ASSIGN")
    if match_result != True:
        return match_result
    exp_node = exp()
    assign_node.addChild(exp_node)

    return assign_node


# exp -> simple-exp comparison-op simple-exp | simple-exp
def exp():
    temp_node = simple_exp()
    root_node = temp_node
    if (peek_Type() in ["EQUAL", "LESSTHAN"]):
        root_node = comparison_op()
        root_node.addChild(temp_node)
        temp_node = simple_exp()
        root_node.addChild(temp_node)

    return root_node


def contains_errors(node: Node):
    if node.isError:
        return node.data
    for child in node.children:
        result = contains_errors(child)
        if result:
            return result
    if node.next:
        result = contains_errors(node.next)
        if result:
            return result

    return False
