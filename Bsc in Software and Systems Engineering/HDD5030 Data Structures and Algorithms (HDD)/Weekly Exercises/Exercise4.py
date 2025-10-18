import re

class StackUnderflow(ValueError): pass
class SStack:
    def __init__(self): self._elems = []
    def is_empty(self): return self._elems == []
    def push(self, elem): self._elems.append(elem)
    def pop(self):
        if self._elems == []: raise StackUnderflow
        return self._elems.pop()

class QueueUnderflow(ValueError): pass
class SQueue:
    def __init__(self, init_len=8):
        self._len, self._elems, self._head, self._num = init_len, [0]*init_len, 0, 0
    def is_empty(self): return self._num == 0
    def dequeue(self):
        if self._num == 0: raise QueueUnderflow
        e = self._elems[self._head]
        self._head = (self._head+1) % self._len
        self._num -= 1
        return e
    def enqueue(self, elem):
        if self._num == self._len: self.__extend()
        idx = (self._head+self._num) % self._len
        self._elems[idx] = elem
        self._num += 1
    def __extend(self):
        old_len, new_elems = self._len, [0]*(self._len*2)
        for i in range(self._num):
            new_elems[i] = self._elems[(self._head+i) % old_len]
        self._elems, self._head, self._len = new_elems, 0, self._len*2

def check_html_tags(html):
    tag_pattern = re.compile(r"<(/?)(\w+)([^>]*)>")
    stack, self_closing = SStack(), {"br","img","hr","input","meta","link"}
    for match in tag_pattern.finditer(html):
        closing, tag, _ = match.groups(); tag = tag.lower()
        if closing:
            if stack.is_empty() or stack.pop()!=tag: return "Invalid HTML"
        elif tag not in self_closing and not _.strip().endswith("/"):
            stack.push(tag)
    return "Valid HTML" if stack.is_empty() else "Invalid HTML"

def decimal_to_binary(n):
    if n==0: return "0"
    q= SQueue()
    while n>0: q.enqueue(n%2); n//=2
    bits=[]
    while not q.is_empty(): bits.append(str(q.dequeue()))
    return "".join(reversed(bits))

if __name__=="__main__":
    choice=input("Main menu: \n1) HTML Checker \n2) Decimal to Binary \nWhat would you like to do? \n ")
    if choice=="1":
        html=input("Enter HTML string:\n")
        print(check_html_tags(html))
    elif choice=="2":
        n=int(input("Enter decimal number:\n"))
        print(decimal_to_binary(n))

# AI Statement: AI tools such as VS Code Copilot were used to assist and 
# manage error in the development of this code.