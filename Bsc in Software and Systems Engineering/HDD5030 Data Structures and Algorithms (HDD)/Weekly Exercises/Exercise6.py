class ExprNode:
    """Expression tree node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def tokenize(expression):
    """Convert infix expression string to tokens"""
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            j = i
            while j < len(expression) and expression[j].isdigit():
                j += 1
            tokens.append(expression[i:j])
            i = j
        elif expression[i] in '+-*/()':
            tokens.append(expression[i])
            i += 1
        else:
            i += 1
    return tokens

def precedence(op):
    """Get operator precedence"""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def build_tree_from_infix(expression):
    """Build expression tree from infix expression using two stacks"""
    tokens = tokenize(expression)
    
    op_stack = []
    node_stack = []
    
    for token in tokens:
        if token.isdigit():
            node_stack.append(ExprNode(token))
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                op = op_stack.pop()
                right = node_stack.pop()
                left = node_stack.pop()
                node = ExprNode(op)
                node.left = left
                node.right = right
                node_stack.append(node)
            op_stack.pop()
        else:
            while (op_stack and op_stack[-1] != '(' and 
                   precedence(token) <= precedence(op_stack[-1])):
                op = op_stack.pop()
                right = node_stack.pop()
                left = node_stack.pop()
                node = ExprNode(op)
                node.left = left
                node.right = right
                node_stack.append(node)
            op_stack.append(token)
    
    while op_stack:
        op = op_stack.pop()
        right = node_stack.pop()
        left = node_stack.pop()
        node = ExprNode(op)
        node.left = left
        node.right = right
        node_stack.append(node)
    
    return node_stack[0] if node_stack else None

def postorder_nonrecursive(root):
    """Generate postfix expression using non-recursive postorder traversal"""
    if not root:
        return []
    
    result = []
    stack = []
    last_visited = None
    current = root
    
    while current or stack:
        if current:
            stack.append(current)
            current = current.left
        else:
            peek_node = stack[-1]
            if peek_node.right and last_visited != peek_node.right:
                current = peek_node.right
            else:
                result.append(peek_node.value)
                last_visited = stack.pop()
    
    return result

def evaluate_postfix(postfix_tokens):
    """Evaluate postfix expression using stack"""
    stack = []
    
    for token in postfix_tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            right = stack.pop()
            left = stack.pop()
            
            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                result = left / right 
            
            stack.append(result)
    
    return stack[0] if stack else 0

if __name__ == "__main__":
    expr = "3 + 2*(1+4*5-6/3) - 2"
    print("Infix Expression:", expr)
    
    root = build_tree_from_infix(expr)
    
    postfix = postorder_nonrecursive(root)
    print("Postfix Expression:", ' '.join(postfix))
    
    result = evaluate_postfix(postfix)
    print("Result =", result)
    
    print("\n--- Additional Test Cases ---")
    test_cases = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "10 - 6 / 2",
        "2 * (3 + 4 * (5 - 2))"
    ]
    
    for test_expr in test_cases:
        print(f"\nInfix: {test_expr}")
        root_test = build_tree_from_infix(test_expr)
        postfix_test = postorder_nonrecursive(root_test)
        result_test = evaluate_postfix(postfix_test)
        print(f"Postfix: {' '.join(postfix_test)}")
        print(f"Result: {result_test}")