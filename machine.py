
# Constants
import sys,os,struct
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
	  self.stack = Stack()
	  self.reg = [0 for i in xrange(8)]
	  self.mem =  [MEMORY_SIZE]


class Machine:
	def __init__(self):
		self.ips = 0
		self.mem = Memory()
		self.return_addr =  Stack()
		self.nopp = 0
		self.input_buf = None
		self.output = ""
		self.dispatch_map_length = [0,2,1,0,3,3,1,2,3,3,3,3,2,2,1,2,2,1,0,1,1,0]
		self.dispatch_map = [self.halt,self.set,self.push,self.pop,self.eq,self.gt,self.jmp,self.jt,self.jf,self.add,self.mul,self.mod,self.andg,
		self.org,self.notg,self.rmem,self.wmem,self.call,self.ret,self.out,self.ing,self.noop]


	#memory operations shortcuts
	def pop(self):
		return self.mem.stack.pop()
	def push(self,a):
		self.mem.stack.push(a)
	def greg(self,a):
		if a > len(self.mem.reg) or a < 0:
			raise Exception('index out of bounds greg ' + str(a))
		return self.mem.reg[a]
	def sreg(self,a,b):
		if a > len(self.mem.reg) or a < 0:
			raise Exception('index out of bounds sreg ' + str(a))
		self.mem.reg[a]=b
	def ssreg(self,a,b):
		if a > len(self.mem.reg) or a < 0:
			raise Exception('index out of bounds ssreg ' + str(a))
		self.mem.reg[a]=b
	#Operations:
	#binary
	def duo_operate(self,a,b,c,op):
		self.sreg(a,operate(self.greg(b),self.greg(c),op))

	#OP 0
	def halt(self):
		logging.info("halt")
		exit(0)
	#OP 1
	def set(self,a):
		logging.info("set")
		print a
		self.ssreg(a[0],a[1])
	#OP 2
	def push(self,a):
		logging.info("push " + str(a[0]))
		self.push(a[0])
	#OP 3
	def pop(self,a):
		logging.info("pop")
		self.sreg(a[0],self.pop())
	#OP 4
	def eq(self,a):
		logging.info("eq")
		self.sreg(a[0],int(self.greg(a[1])==self.greg(a[2])))
	#OP 5
	def gt(self,a):
		logging.info("gt")
		self.sreg(a[0],int(self.greg(a[1])>self.greg(a[2])))
	#OP 6
	def jmp(self,a):
		logging.info("jmp")
		location = a.pop()
		if location >= 0:
			self.ips = location
	#OP 7
	def jf(self,a):
		logging.info("jf")
		if a[0]==0:
			self.jmp([a[1]])
	#OP 8
	def jt(self,a):
		logging.info("jt")
		if a[0]!=0:
			self.jmp([a[1]])
	#OP 9
	def add(self,a):
		logging.info("add")
		self.duo_operate(a[0],a[1],a[2],"+")
	#OP 10
	def mul(self,a):
		logging.info("mul")
		self.duo_operate(a[0],a[1],a[2],"*")
	#OP 11
	def mod(self,a):
		logging.info("mod")
		self.duo_operate(a[0],a[1],a[2],"%")
	#OP 12
	def andg(self,a):
		logging.info("and")
		self.sreg(a[0],self.greg(a[1]) & self.greg(a[2]))
	#OP 13
	def org(self,a):
		logging.info("or")
		self.sreg(a[0],self.greg(a[1]) | self.greg(a[2]))
	#OP 14
	def notg(self,a):
		logging.info("not")
		self.sreg(a[0], self.greg(a[0] & 32767))   #TODO
	#OP 15
	def rmem(self,a):
		logging.info("rmem")
		self.sreg(a[0], self.mem.mem[self.greg(a[1])])
	#OP 16
	def wmem(self,a):
		logging.info("wmem")
		self.mem.mem[self.greg(a[0])] = self.greg(a[1])
	#OP 17
	def call(self,a):
		logging.info("call")
		self.return_addr.push(self.ips)
		jmp(a)
	#OP 18
	def ret(self):
		logging.info("ret")
		addr = self.return_addr.pop()
		if addr >=0:
			ips = addr
	#OP 19
	def out(self,b):
		logging.info("out")
		a=b[0]
		logging.info("out " + str(a))
		#print chr(self.greg(a))
		print chr(a),
	#OP 20
	def ing(self,a):
		logging.info("in")
		if input_buf is None:
			command = raw_input()
			self.input_buffer = (c for c in command)
		try:
			chary = self.input_buf.next()
		except StopIteration:
			self.input_buf = None  # Reset.
			chary = '\n'
		self.sreg(a[0],ord(c))
	#OP 21
	def noop(self):
		logging.info("noop")

	def run(self,code):
		logging.info("start running")
		logging.info('code len: ' + str(len(code)))
		while self.ips < len(code):
			opcode = code[self.ips]
			self.ips += 1
			if opcode in range(0,len(self.dispatch_map)):
				length = self.dispatch_map_length[opcode]
				if length == 0:
					self.dispatch_map[opcode]()
				else:
					args = [code[self.ips]]
					self.ips+=1
					for i in range(1,length):
						args.append(code[self.ips])
						self.ips+=1
					self.dispatch_map[opcode](args)



def main():
	size = os.path.getsize(FILENAME)
	inp = open(FILENAME,'rb')
	bytek = inp.read(2)
	code = []
	while size > 0:
		val = struct.unpack("h", bytek)
		code.append(val[0])
		size-= 2
		bytek = inp.read(2)
		if len(bytek) < 2:
			break
	tomerMachine = Machine()
	tomerMachine.run(code)

if __name__ == '__main__':
	main()
