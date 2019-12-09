# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 3 Interpreter - Python

import sys
from tok import Tok, TokType

class Par:

	def __init__(self, toks):
		self.toks = toks

	def __err(self, pos, msg):
		print('ERROR: ' + msg + ' @ ...', *self.toks[pos - 4:pos], \
				'<' + str(self.toks[pos]) + '>', \
				*self.toks[pos + 1:pos + 5], '...', sep=' ')
		sys.exit(1)

	def __parse_prog(self):
		self.mem = {}
		try:
			if self.toks[0].type != TokType.KEY_FUNC.value:
				self.__err(0, 'expected function keyword')
			if self.toks[1].type != TokType.ID.value:
				self.__err(1, 'expected identifier')
			if self.toks[2].type != TokType.PAREN_OPEN.value:
				self.__err(2, 'expected (')
			if self.toks[3].type != TokType.PAREN_CLOSE.value:
				self.__err(3, 'expected )')
		except IndexError:
			self.err

		pos = self.__parse_block(4)
		if self.toks[pos].type != TokType.KEY_END.value:
			self.__err(pos, 'expected end keyword')

	def __parse_block(self, pos):
		pos = self.__parse_stmt(pos)
		if self.toks[pos].type in (TokType.ID.value, \
				TokType.KEY_IF.value, \
				TokType.KEY_WHILE.value, \
				TokType.KEY_FOR.value, \
				TokType.KEY_PRINT.value):
			pos = self.__parse_block(pos)
		return pos

	def __parse_stmt(self, pos):
		if self.toks[pos].type == TokType.ID.value:
			return self.__parse_stmt_assign(pos)
		elif self.toks[pos].type == TokType.KEY_IF.value:
			return self.__parse_stmt_if(pos)
		elif self.toks[pos].type == TokType.KEY_WHILE.value:
			return self.__parse_stmt_while(pos)
		elif self.toks[pos].type == TokType.KEY_FOR.value:
			return self.__parse_stmt_for(pos)
		elif self.toks[pos].type == TokType.KEY_PRINT.value:
			return self.__parse_stmt_print(pos)
		else:
			self.__err(pos, 'expected statement opening')

	def __parse_stmt_assign(self, pos):
		if self.toks[pos + 1].type != TokType.OP_ASSIGN.value:
			self.__err(pos + 1, 'expected assignment operator')
		id = self.toks[pos].lex
		pos += 2
		stack = []
		pos = self.__parse_arith(pos, stack)
		self.mem[id] = stack.pop()
		return pos

	#def __parse_stmt_if(self, pos):

	#def __parse_stmt_while(self, pos):

	#def __parse_stmt_for(self, pos):

	def __parse_stmt_print(self, pos):
		if self.toks[pos + 1].type != TokType.PAREN_OPEN.value:
			self.__err(pos + 1, 'expected (')
		stack = []
		pos += 2
		pos = self.__parse_arith(pos, stack)
		if self.toks[pos].type != TokType.PAREN_CLOSE.value:
			self.__err(pos, 'expected )')
		print(stack.pop())
		return pos + 1

	def __parse_arith(self, pos, stack):
		expr = []
		while self.toks[pos].is_arith_op() or \
				self.toks[pos].type == TokType.INT.value or \
				(self.toks[pos].type == TokType.ID.value and \
				self.toks[pos + 1].type != TokType.OP_ASSIGN.value):
			expr.append(self.toks[pos])
			pos += 1
		if not expr:
			self.__err(pos, 'expected arithmetic expression')
		for t in reversed(expr):
			if t.type == TokType.ID.value:
				if not t.lex in self.mem:
					self.__err(pos, 'uninitilized identifier \'' + t.lex + '\'')
				stack.append(self.mem[t.lex])
			elif t.type == TokType.INT.value:
				stack.append(int(t.lex))
			elif t.is_arith_op():
				if len(stack) < 2:
					self.__err(pos, 'invalid arithmetic expression')
				x = stack.pop()
				y = stack.pop()
				if t.type == TokType.OP_ADD.value:
					stack.append(x + y)
				elif t.type == TokType.OP_SUB.value:
					stack.append(x + y)
				elif t.type == TokType.OP_MUL.value:
					stack.append(x * y)
				elif t.type == TokType.OP_DIV.value:
					stack.append(x / y)
				elif t.type == TokType.OP_MOD.value:
					stack.append(x % y)
				elif t.type == TokType.OP_INV.value:
					stack.append(y / x)
				elif t.type == TokType.OP_EXP.value:
					stack.append(x ** y)
			else:
				self.__err(pos, 'expected arithmetic expression')
		return pos

	def exec(self):
		self.__parse_prog()
