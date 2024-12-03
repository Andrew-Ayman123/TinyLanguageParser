from node import createIfNode,createAssignNode,createReadNode,createWriteNode,createIDNode,createRepeatNode,createOpNode, Node

        
list_of_tokens = [
    ("read", "READ"),
    ("x", "IDENTIFIER"),
    (";", "SEMICOLON"),
    ("if", "IF"),
    ("0", "NUMBER"),
    ("<", "LESSTHAN"),
    ("x", "IDENTIFIER"),
    ("then", "THEN"),
    ("fact", "IDENTIFIER"),
    (":=", "ASSIGN"),
    (";", "SEMICOLON"),
    ("repeat", "REPEAT"),
    ("fact", "IDENTIFIER"),
    (":=", "ASSIGN"),
    ("fact", "IDENTIFIER"),
    ("*", "MULT"),
    ("x", "IDENTIFIER"),
    (";", "SEMICOLON"),
    ("x", "IDENTIFIER"),
    (":=", "ASSIGN"),
    ("x", "IDENTIFIER"),
    ("-", "MINUS"),
    ("1", "NUMBER"),
    ("until", "UNTIL"),
    ("x", "IDENTIFIER"),
    ("=", "EQUAL"),
    ("0", "NUMBER"),
    (";", "SEMICOLON"),
    ("write", "WRITE"),
    ("fact", "IDENTIFIER"),
    ("end", "END")
    ]
def is_empty(list):
        return len(list) == 0
   
def next_token():
        global c_token_index
        if c_token_index < len(list_of_tokens):
            token=list_of_tokens[c_token_index]
            c_token_index += 1
        return token
c_token_index = 0
#match function
def match(current_token_type, expected_token_type):
    
    return current_token_type == expected_token_type

def program():
    
    child=stmtSequence();
    if child !="ERROR":
        Node.addChild(child)
    else:
        return "ERROR"
    
    if c_token_index<len(list_of_tokens):
        return "ERROR"
     
    return Node 
  #statement{;statement}   
def stmtSequence():
    temp=statement();
    root=temp;
    #hena an check en statement di is valid
    #if temp.data!="ERROR":
        #root=temp
    #else:
        #return "ERROR"  
    while True:
        token_d=next_token()
        if is_empty(token_d):
            break
        #hena token_d 3ebara 3an value w type fa value betet5azen f token w type f token_type    
        token ,token_type=token_d 
        
        if token_type=="SEMICOLON":
            siblings= statement()
            temp.setNext(siblings)

        else:
            break
        
        return temp
    #statament -> if-stmt | repeat-stmt | assign-stmt |read-stmt |  write-stmt
def statement():
    token_d=next_token()
    
    token,token_type=token_d
    
    if token_type=="IF":
        tmp=if_stmt()
    elif token_type=="REPEAT":
        tmp=repeat_stmt()
        
    elif token_type=="READ":
        tmp=read_stmt()
    elif token_type=="WRITE":
        tmp=write_stmt()
    elif token_type=="IDENTIFIER":
        tmp=assign_stmt()
    else:
        return "ERROR"
    
    return tmp
#if -stmt → if exp then stmt-sequence end    
def if_stmt():
    node_tmp=createIfNode()
    
    token_d=next_token()
    token,token_type=token_d
    node_exp=exp()
    
    node_tmp.addChild(node_exp)
    
    if match(token_type,"THEN"):
        token_d=next_token()
        
        stmt_node=stmtSequence()
        node_tmp.addChild(stmt_node)
    else:
        return "ERROR"
    
    if match(token_type,"ELSE"):
        token_d=next_token()
        stmt_node=stmtSequence()
        node_tmp.addChild(stmt_node)
          
    if match(token_type,"END"):
        token_d=next_token()
    else: 
        return "ERROR"
    
    return node_tmp    
#exp -> simple-exp comparison-op simple-exp | simple-exp      
def exp():
      nodeComparisonOp =createOpNode("comparison")
      nodeSimpleExp1 = simple_exp()
      
      nodeComparisonOp.addChild(nodeSimpleExp1)
      token_d=next_token()
      token,token_type=token_d
      if token_type in["EQUAL","LESSTHAN"]:
          nodeComparisonOp.data=token
          
          token_d=next_token()
          nodeSimpleExp2=simple_exp()
          
          nodeComparisonOp.addChild(nodeSimpleExp2)
      return nodeComparisonOp
          
#simple-exp -> term {addop term}
def simple_exp():
    nodeTerm=term()
    token_d=next_token()
    token,token_type=token_d
    while ((token_d) and (match(token_type,"PLUS") or  match(token_type,"MINUS"))):
        nodeOp=createOpNode(token)
        
        nodeOp.addChild(nodeTerm)
        nodeTerm2=term()
        nodeOp.addChild(nodeTerm2)
        
        nodeTerm=nodeOp
     
    return nodeTerm                         
          
      
#term -> factor {mulop factor}
def term():
    nodefactor=factor()
    token_d=next_token()
    token,token_type=token_d
    while ((token_d) and (match(token_type,"MULT") or  match(token_type,"DIV"))):  
        mulop=createOpNode(token)
        
        mulop.addChild(nodefactor)
        
        nodeFactor=factor()
        
        mulop.addChild(nodeFactor)
        nodefactor=mulop
        
    return nodefactor   
        
          
 

# Placeholder functions for repeat, read, write, and assign statements
#repeat->stmt-sequence until exp
def repeat_stmt():
    r_node=createRepeatNode()
    token_d=next_token()
    token,token_type=token_d
    
    b_node=stmtSequence()
    r_node.addChild(b_node)
    if match(token_type,"UNTIL"):
        token_d=next_token()
        e_node=exp()
        r_node.addChild(e_node)
    else:
        return "ERROR"
    
    return r_node 
    
    
#read - > read identifer
def read_stmt():
    read_stmt =createReadNode()
    token_d=next_token()
    token,token_type=token_d
    if match(token_type,"IDENTIFIER"):
        read_stmt.addChild(createIDNode())
    else:
        return "ERROR"
    return read_stmt
#write -> write exp
def write_stmt():
    w_root=createWriteNode()
    token_d=next_token()
    expNode=exp()
    w_root.addChild(expNode)
    
    return w_root

#assignStmt -> Identifier := exp
def assign_stmt():
    assign_node=createAssignNode() 
    token_d=next_token
    token,token_type=token_d
    if match(token_type,"IDENTIFIER"):
        assign_node.addChild(createIDNode(token))
    else:
        return "ERROR"
    token_d=next_token()
    token,token_type=token_d
    if match(token_type,"ASSIGNMENT"):
        token_d=next_token()
        token,token_type=token_d
        exp_node=exp()
        assign_node.addChild(exp_node)
    else:
        return "ERROR"
    
    return assign_node

        
    


