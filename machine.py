
# Constants
import sys
import logging


logging.basicConfig(filename='lol.log',level=logging.DEBUG)
VAR_SIZE = 32768
FILENAME = 'challenge.bin'

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

class Memory:
  def __init__(self):
	self.stack = Stack(),
	self.reg = [],
	self.mem =  [MEMORY_SIZE]



class Machine:
	def __init__(self, code):
	  self.ips = 0
	  self.mem = Memory(),
	  self.return_addr =  Stack(),
	  self.code=code,
	  self.nopp = 0,
	  self.output = "",

	  self.dispatch_map_length = {
		"0":0,
		"1":1,
		"2":1,
		"3":0,
		"4":3,
		"5":3,
		"6":1,
		"7":2,
		"8":3,
		"9":3,
		"10":3,
		"11":3,
		"12":2,
		"13":2,
		"14":1,
		"15":2,
		"16":2,
		"17":1,
		"18":0,
		"19":1,
		"20":1,
		"21":0,
	  }

	  self.dispatch_map = {
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
	def duo_operate(self,a,b,c,op):
		self.sreg(a,operate(self.greg(b),self.greg(c),op))

	#OP 0
	def halt(self):
		self.ips = len(self.code)
	#OP 1
	def set(self,a):
		self.ssreg(a[0],a[1])
	#OP 2
	def push(self,a):
		self.push(self.greg(a[0]))
	#OP 3
	def pop(self,a):
		self.sreg(a[0],self.pop())
	#OP 4
	def eq(self,a):
		self.sreg(a[0],int(self.greg(a[1])==self.greg(a[2])))
	#OP 5
	def gt(self,a):
		self.sreg(a[0],int(self.greg(a[1])>self.greg(a[2])))
	#OP 6
	def jmp(self,a):
		location = self.greg(a[0])
		if location >= 0 and location < len(self.code):
			self.ips = location
	#OP 7
	def jf(self,a):
		if self.greg(a[0])==0:
			self.jmp(self.greg(a[1]))
	#OP 8
	def jt(self,a):
		if self.greg(a[0])!=0:
			self.jmp(self.greg(a[1]))
	#OP 9
	def add(self,a):
		self.duo_operate(a[0],a[1],a[2],"+")
	#OP 10
	def mul(self,a):
		self.duo_operate(a[0],a[1],a[2],"*")
	#OP 11
	def mod(self,a):
		self.duo_operate(a[0],a[1],a[2],"%")
	#OP 12
	def andg(self,a):
		self.sreg(a[0],self.greg(a[1]) & self.greg(a[2]))
	#OP 13
	def org(self,a):
		self.sreg(a[0],self.greg(a[1]) | self.greg(a[2]))
	#OP 14
	def notg(self,a):
		self.sreg(a[0],)   #TODO
	#OP 15
	def rmem(self,a):
		self.sreg(a[0], self.mem.mem[self.greg(a[1])])
	#OP 16
	def wmem(self,a):
		self.mem.mem[self.greg(a[0])] = self.greg(a[1])
	#OP 17
	def call(self,a):
		self.return_addr.push(self.ips)
		jmp(a)
	#OP 18
	def ret(self):
		addr = self.return_addr.pop()
		if addr >=0 and addr < len(self.code):
			ips = addr
	#OP 19
	def out(self,b):
		a=b[0]
		logging.info("out " + str(a) + " " + chr(self.grep(a)))
		print chr(self.greg(a))
		self.output += chr(self.greg(a))
	#OP 20
	def ing(self,a):
		logging.info("in")
		c = sys.stdin.read(1)
		self.sreg(a[0],ord(c))
	#OP 21
	def noop(self):
		self.nopp+=1


	# Dispatcher:
	def run(self):
		while self.ips < len(self.code):
			opcode = self.code[self.ips]
			self.ips += 1
			if op in self.dispatch_map:
				length = dispatch_map_length[op]
				if length == 0:
					self.dispatch_map[op]()
				else:
					args = {self.code[self.ips]}
					self.ips+=1
					for i in range(1,length):
						args.append(self.code[self.ips])
						self.ips+=1
					self.dispatch_map[op](args)
			else:
				raise RuntimeError("Unknown opcode: '%s'" % op)


	def dispatch(self, op):
		if op in self.dispatch_map:
			length = dispatch_map_length[op]
			for i in range(0,length):

			self.dispatch_map[op]()
		elif isinstance(op, int):
			# push numbers on the data stack
			self.push(op)
		elif isinstance(op, str) and op[0]==op[-1]=='"':
			# push quoted strings on the data stack
			self.push(op[1:-1])
		else:
			raise RuntimeError("Unknown opcode: '%s'" % op)

def main():
	code = open(FILENAME,'rb').read()
	tomerMachine = Machine(code)
	tomerMachine.run()

if __name__ == '__main__':
	main()
