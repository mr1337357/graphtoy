import sys
OPERATORS = set(['+', '-', '*', '/', '(', ')', '^'])  # set of operators
PRIORITY = {'+':1, '-':1, '*':2, '/':2, '^':3} # dictionary having priorities 

class math_function():
    def __init__(self,expression='x',debug=False):
        self.expression=self.infix_to_postfix(expression)
        self.debug=debug
    
    def infix_to_postfix(self,expression):
        stack = [] # initially stack empty
        output = '' # initially output empty
        token=''
        for ch in expression:
            if ch not in OPERATORS:  # if an operand then put it directly in postfix expression
                token += ch
            else:
                if len(token) > 0:
                    output+=token+' '
                    token=''
                if ch=='(':  # else operators should be put in stack
                    stack.append('(')
                elif ch==')':
                    while stack and stack[-1]!= '(':
                        output+=stack.pop()
                    stack.pop()
                else:
                    while stack and stack[-1]!='(' and PRIORITY[ch]<=PRIORITY[stack[-1]]:
                        output+=stack.pop()
                    stack.append(ch)
        if len(token) > 0:
            output+=token
        while stack:
            output+=stack.pop()
        print(output)
        return output
        
    def evaluate(self,**kwargs):
        stack = []
        acc = 0
        num = 0
        for ch in self.expression:
            if self.debug:
                sys.stderr.write('before:\n')
                sys.stderr.write('   {}\n'.format(stack))
                sys.stderr.write('   ch: "{}"\n'.format(ch))
            if ch.isnumeric():
                num = 1
                acc*=10
                acc+=int(ch)
            elif ch in kwargs:
                num = 1
                acc = kwargs[ch]  
            else:
                if num:
                    num = 0
                    stack.append(acc)
                    acc = 0
                if ch == '*':
                    stack.append(stack.pop()*stack.pop())
                elif ch == '/':
                    den = stack.pop()
                    numer = stack.pop()
                    stack.append(numer/den)
                elif ch == '+':
                    stack.append(stack.pop()+stack.pop())
                elif ch == '-':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b-a)
                elif ch == '^':
                    exp = stack.pop()
                    base = stack.pop()
                    stack.append(base**exp)
            if self.debug:
                sys.stderr.write('after:\n')
                sys.stderr.write('   num: {}\n'.format(num))
                sys.stderr.write('   {}\n\n'.format(stack))
     
            #print(stack)
        return stack.pop()
        
    def __repr__(self):
        return self.expression
        
if __name__ == '__main__':
    f = math_function('x^3-2*x^2',debug=True)
    print(f.evaluate(x=5))