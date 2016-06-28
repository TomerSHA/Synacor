
# Constants
import sys

VAR_SIZE = 32768

import operator
dops = {"+": operator.add,
       "*": operator.mul,
       "%": operator.mod}

clamp = lambda n, maxn: max(min(maxn, n), 0)


operate = lambda n, m, opchar : ((dops[opchar])(n,m))%VAR_SIZE



from collections import deque

class Stack(deque):
    push = deque.append

    def top(self):
        return self[-1]

MEMORY_SIZE = 32768

Class Memory:
  def __init__(self):
    self.stack = Stack(),
    self.reg == { "a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"g":g,"h":h,},
    self.mem =  [MEMORY_SIZE]



Class Machine:
    def __init__(self, code):
      self.ips = 0
      self.mem = Memory(),
      self.return_addr =  stack(),
      self.code=code,

      self.dispmap == {
        "0":self.halt,
        "1":self.set,
        "2":self.push,
        "3":self.pop,
        "4":self.eq,
        "5":self.gt,
        "6":self.jmp,
        "7":self.jt,
        "8":self.jf,
        "9":self.add,
        "10":self.mul,
        "11":self.mod,
        "12":self.andg,
        "13":self.org,
        "14":self.notg,
        "15":self.rmem,
        "16":self.wmem,
        "17":self.call,
        "18":self.ret,
        "19":self.out,
        "20":self.ing,
        "21":self.noop,
    }

    #memory operations shortcuts
    def pop(self):
        return self.mem.stack.pop()
    def push(self,a):
        self.mem.stack.push(a)
    def greg(self,a):
        return self.mem.reg[a]
    def sreg(self,a,b):
        self.mem.reg[a]=b
    def ssreg(self,a,b):
        self.mem.reg[a]=self.mem.reg[b]
    #Operations:
    #binary
    def duo-operate(self,a,b,c,op):
        self.sreg(a,operate(self.greg(b),self.greg(c),op)


    #OP 0
    def halt(self):
        self.ips = len(self.code)
    #OP 1
    def set(self,a,b):
        self.ssreg(a,b)
    #OP 2
    def push(self,a):
        self.push(self.greg(a))
    #OP 3
    def pop(self,a):
        self.sreg(a,self.pop())
    #OP 4
    def eq(self,a,b,c):
        self.sreg(a,int(self.greg(b)==self.greg(c))
    #OP 5
    def gt(self,a,b,c):
        self.sreg(a,int(self.greg(b)>self.greg(c))
    #OP 6
    def jmp(self,a):
    #OP 7
    def jf(self,a,b):
        if self.greg(a)==0:
            self.jmp(self.greg(b))
    #OP 8
    def jt(self,a,b):
        if self.greg(a)!=0:
            self.jmp(self.greg(b))
    #OP 9
    def add(self,a,b,c):
        self.duo-operate(a,b,c,"+")
    #OP 10
    def mul(self,a,b,c):
        self.duo-operate(a,b,c,"*")
    #OP 11
    def mod(self,a,b,c):
        self.duo-operate(a,b,c,"%")
    #OP 12
    def andg(self,a,b,c):
        self.sreg(a,self.greg(b) & self.greg(c))
    #OP 13
    def org(self,a,b,c):
        self.sreg(a,self.greg(b) | self.greg(c))
    #OP 14
    def notg(self,a,b):
        self.sreg(a,)   #TODO
    #OP 15
    def rmem(self,a,b):
        self.sreg(a, self.mem.mem[self.greg(b)])
    #OP 16
    def wmem(self,a,b):
        self.mem.mem[self.greg(a)] = self.greg(b)
    #OP 17
    def call(self,a):

    #OP 18
    def ret(self):

    #OP 19
    def out(self,a):
        print chr(self.greg(a))
    #OP 20
    def ing(self,a):
        c = sys.stdin.read(1)
        self.sreg(a,ord(c))
    #OP 21
    def noop(self):


    # Dispatcher:
    def run(self):
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)
        ADD WRITE


    def dispatch(self, op):
        if op in self.dispatch_map:
            self.dispatch_map[op]()
        elif isinstance(op, int):
            # push numbers on the data stack
            self.push(op)
        elif isinstance(op, str) and op[0]==op[-1]=='"':
            # push quoted strings on the data stack
            self.push(op[1:-1])
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)
