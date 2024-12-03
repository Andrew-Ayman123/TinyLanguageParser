from node import createIfNode,createAssignNode,createReadNode,createWriteNode,createIDNode,createRepeatNode,createOpNode, Node

        
list_of_tokens = [
    ("read", "READ"),
    ("x", "IDENTIFIER"),
    (";", "SEMICOLON"),
    ("if", "IF"),
    ("<", "LESSTHAN"),
    ("then", "THEN"),
    ("repeat", "REPEAT"),
    (":=", "ASSIGN"),
    ("*", "MULT"),
    ("-", "MINUS"),
    ("until", "UNTIL"),
    ("=", "EQUAL"),
    ("write", "WRITE"),
    ("end", "END")
    ]
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
        #global c_token_index
        #if c_token_index < len(list_of_tokens):
        if list_of_tokens:
            #token=list_of_tokens[c_token_index]
            #token=list_of_tokens.pop(0)
            list_of_tokens.pop(0)
            #c_token_index += 1
            #return token
        #return None
#c_token_index = 0
#match function
def match(current_token_type, expected_token_type):
    
    return current_token_type == expected_token_type

def program():
    
    child=stmtSequence()
    if child !="ERROR":
        return child
    else:
        return "ERROR" 
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
        if is_empty(list_of_tokens()):
            break
        #hena token_d 3ebara 3an value w type fa value betet5azen f token w type f token_type    
        token,token_type=list_of_tokens[0] 
        
        if list_of_tokens and  token_type=="SEMICOLON":
            list_of_tokens.pop(0)
            siblings= statement()
            temp.setNext(siblings)
        else:
            break
        
    return root
    #statament -> if-stmt | repeat-stmt | assign-stmt |read-stmt |  write-stmt
def statement():
    #token_d=next_token()
    
    #token,token_type=list_of_tokens[0]
    
    if peek_Type()=="IF":
        tmp=if_stmt()
    elif peek_Type()=="REPEAT":
        tmp=repeat_stmt()
    elif peek_Type()=="READ":
        tmp=read_stmt()
    elif peek_Type()=="WRITE":
        tmp=write_stmt()
    elif peek_Type()=="IDENTIFIER":
        tmp=assign_stmt()
    else:
        return "ERROR"
    
    return tmp
#if -stmt → if exp then stmt-sequence end    
def if_stmt():
    node_tmp=createIfNode()
    
    #token_d=next_token()
    #token,token_type=token_d
    next_token()
    #token_type=peek_Type()
    node_exp=exp()
    
    node_tmp.addChild(node_exp)
    
    if match(peek_Type(),"THEN"):
       # if list_of_tokens:
            #token_d=next_token()
        next_token()
        
        stmt_node=stmtSequence()
        node_tmp.addChild(stmt_node)
    else:
        return "ERROR"
    
    if match(peek_Type(),"ELSE"):
        #token_d=next_token()
        next_token()
        stmt_node=stmtSequence()
        node_tmp.addChild(stmt_node)
          
    if match(peek_Type(),"END"):
        #token_d=next_token()
        next_token()
    else: 
        return "ERROR"
    
    return node_tmp    
#exp -> simple-exp comparison-op simple-exp | simple-exp      
def exp():
      nodeComparisonOp =createOpNode("comparison")
      nodeSimpleExp1 = simple_exp()
      
      nodeComparisonOp.addChild(nodeSimpleExp1)
      #token_d=next_token()
      token_type=peek_Type()
      if token_type in["EQUAL","LESSTHAN"]:
          nodeComparisonOp.data=peek_Value()
          
          next_token()
          nodeSimpleExp2=simple_exp()
          
          nodeComparisonOp.addChild(nodeSimpleExp2)
      return nodeComparisonOp
          
#simple-exp -> term {addop term}
def simple_exp():
    nodeTerm=term()
    #token_d=next_token()
    token_type=peek_Type()
    while ((list_of_tokens) and (match(token_type,"PLUS") or  match(token_type,"MINUS"))):
        nodeOp=createOpNode(peek_Value())
        
        nodeOp.addChild(nodeTerm)
        next_token()
        nodeTerm2=term()
        nodeOp.addChild(nodeTerm2)
        
        nodeTerm=nodeOp
     
    return nodeTerm                         
          
      
#term -> factor {mulop factor}
def term():
    nodefactor=factor()
    #token_d=next_token()
    token_type=peek_Type()
    while ((list_of_tokens) and (match(token_type,"MULT") or  match(token_type,"DIV"))):  
        mulop=createOpNode(peek_Value())
        
        mulop.addChild(nodefactor)
        next_token()
        nodeFactor=factor()
        
        mulop.addChild(nodeFactor)
        nodefactor=mulop
        
    return nodefactor   
        
def factor():
    
    node_temp = None

    # Check the type of the current token
    token_type = peek_Type()
    if token_type == "OPENBRACKET":
        next_token()
        node_exp = exp()
        node_temp = node_exp
        if match(peek_Type(), "CLOSEDBRACKET"):
            next_token()  
    elif token_type == "NUMBER" or token_type == "IDENTIFIER":
        node_temp = createIDNode(peek_Value())
        next_token()  
    else:
        return "ERROR"

    # Return the node or error
    return node_temp


# Placeholder functions for repeat, read, write, and assign statements
#repeat->stmt-sequence until exp
def repeat_stmt():
    r_node=createRepeatNode()
    #token_d=next_token()
    next_token()
    #token,token_type=token_d
    token_type=peek_Type()
    
    b_node=stmtSequence()
    r_node.addChild(b_node)
    if match(token_type,"UNTIL"):
        #token_d=next_token()
        next_token()
        e_node=exp()
        r_node.addChild(e_node)
    else:
        return "ERROR"
    
    return r_node 
    
    
#read - > read identifer
def read_stmt():
    read_stmt =createReadNode()
    #token_d=next_token()
    next_token()
    #token,token_type=token_d
    token_type=peek_Type()
    if match(token_type,"IDENTIFIER"):
        read_stmt.addChild(createIDNode(peek_Value()))
        next_token()
    else:
        return "ERROR"
    return read_stmt
#write -> write exp
def write_stmt():
    w_root=createWriteNode()
    #token_d=next_token()
    next_token()
    expNode=exp()
    w_root.addChild(expNode)
    
    return w_root

#assignStmt -> Identifier := exp
def assign_stmt():
    assign_node=createAssignNode("assign") 
    #token_d=next_token
    #token,token_type=token_d
    token_type=peek_Type()
    if match(token_type,"IDENTIFIER"):
        #assign_node.addChild(createIDNode(peek_Value()))
        assign_node.data = createIDNode(peek_Value())
        next_token()
    
        #return "ERROR"
        #token_d=next_token()
        #token,token_type=token_d
        token_type=peek_Type()
        if match(token_type,"ASSIGN"):
            #token_d=next_token()
            next_token()
            #token,token_type=token_d
            exp_node=exp()
            assign_node.addChild(exp_node)
        else:
            return "ERROR"
    else:
        return "ERROR"
    return assign_node

        
    


