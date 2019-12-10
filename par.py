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

	# exit with error message and context
	def __err(self, pos, msg):
		print('ERROR: ' + msg + ' @ ...', *self.toks[pos - 4:pos + 5], '...', sep=' ')
		sys.exit(1)

	def exec(self):
		# reset assigned variable memory
		self.mem = {}

		# verify beginning function
		if len(self.toks) <= 0 or self.toks[0].type != TokType.KEY_FUNC.value:
			self.__err(0, 'expected function keyword')
		if len(self.toks) <= 1 or self.toks[1].type != TokType.ID.value:
			self.__err(1, 'expected identifier')
		if len(self.toks) <= 2 or self.toks[2].type != TokType.PAREN_OPEN.value:
			self.__err(2, 'expected (')
		if len(self.toks) <= 3 or self.toks[3].type != TokType.PAREN_CLOSE.value:
			self.__err(3, 'expected )')

		pos = self.__parse_block(4, True)
		if pos >= len(self.toks) or self.toks[pos].type != TokType.KEY_END.value:
			self.__err(pos, 'expected end keyword')

	def __parse_block(self, pos, is_exec):
		pos = self.__parse_stmt(pos, is_exec)

		# recurse if another statement follows
		if pos < len(self.toks) and self.toks[pos].type in (TokType.ID.value, \
				TokType.KEY_IF.value, \
				TokType.KEY_WHILE.value, \
				TokType.KEY_FOR.value, \
				TokType.KEY_PRINT.value):
			pos = self.__parse_block(pos, is_exec)
		return pos

	def __parse_stmt(self, pos, is_exec):
		if pos >= len(self.toks):
			self.__err(pos, 'expected statement')

		# determine type of statement from first token
		if self.toks[pos].type == TokType.ID.value:
			return self.__parse_stmt_assign(pos, is_exec)
		elif self.toks[pos].type == TokType.KEY_IF.value:
			return self.__parse_stmt_if(pos, is_exec)
		elif self.toks[pos].type == TokType.KEY_WHILE.value:
			return self.__parse_stmt_while(pos, is_exec)
		elif self.toks[pos].type == TokType.KEY_FOR.value:
			return self.__parse_stmt_for(pos, is_exec)
		elif self.toks[pos].type == TokType.KEY_PRINT.value:
			return self.__parse_stmt_print(pos, is_exec)
		else:
			self.__err(pos, 'expected statement')

	def __parse_stmt_assign(self, pos, is_exec):
		if pos + 1 >= len(self.toks) or self.toks[pos + 1].type != TokType.OP_ASSIGN.value:
			self.__err(pos + 1, 'expected assignment operator')
		id = self.toks[pos].lex
		stack = []
		pos = self.__parse_arith(pos + 2, stack)
		if is_exec:
			self.mem[id] = int(stack.pop())

		return pos

	def __parse_stmt_if(self, pos, is_exec):
		stack = []
		pos = self.__parse_bool(pos + 1, stack)
		cond = stack.pop()
		pos = self.__parse_block(pos, cond and is_exec)
		if self.toks[pos].type != TokType.KEY_ELSE.value:
			self.__err(pos, 'expected else keyword')

		pos = self.__parse_block(pos + 1, not cond and is_exec)
		if pos >= len(self.toks) or self.toks[pos].type != TokType.KEY_END.value:
			self.__err(pos, 'expected end keyword')

		return pos + 1

	def __parse_stmt_while(self, pos, is_exec):
		cond_pos = pos + 1
		while True:
			stack = []
			pos = self.__parse_bool(cond_pos, stack)
			cond = stack.pop() and is_exec
			pos = self.__parse_block(pos, cond)
			if not cond:
				break

		if pos >= len(self.toks) or self.toks[pos].type != TokType.KEY_END.value:
			self.__err(pos, 'expected end keyword')

		return pos + 1

	def __parse_stmt_print(self, pos, is_exec):
		if pos + 1 >= len(self.toks) or self.toks[pos + 1].type != TokType.PAREN_OPEN.value:
			self.__err(pos + 1, 'expected (')
		stack = []
		pos = self.__parse_arith(pos + 2, stack)
		if is_exec:
			print(stack.pop())
		if pos >= len(self.toks) or self.toks[pos].type != TokType.PAREN_CLOSE.value:
			self.__err(pos, 'expected )')
		return pos + 1

	def __parse_bool(self, pos, stack):
		# parse relative operator followed by arith operators/operands
		expr = []
		try:
			if not self.toks[pos].is_rel_op():
				self.__err(pos, 'expected relative operator')
			expr.append(self.toks[pos])
			pos += 1
			while self.toks[pos].is_arith_op() or \
					self.toks[pos].type == TokType.INT.value or \
					(self.toks[pos].type == TokType.ID.value and \
					self.toks[pos + 1].type != TokType.OP_ASSIGN.value):
				expr.append(self.toks[pos])
				pos += 1
		except IndexError:
			self.__err(pos, 'unexpected end of expression')
		if not expr:
			self.__err(pos, 'expected boolean expression')

		# eval prefix bool expression
		for t in reversed(expr):
			if t.type == TokType.ID.value:
				if not t.lex in self.mem:
					self.__err(pos, 'uninitilized identifier \'' + t.lex + '\'')
				stack.append(self.mem[t.lex])
			elif t.type == TokType.INT.value:
				stack.append(int(t.lex))
			else:
				if len(stack) < 2:
					self.__err(pos, 'invalid boolean expression')
				stack.append(Par.__eval(t, stack.pop(), stack.pop()))
		if len(stack) != 1:
			self.__err(pos, 'invalid boolean expression')
		return pos

	def __parse_arith(self, pos, stack):
		# parse arith operators/operands
		expr = []
		try:
			while self.toks[pos].is_arith_op() or \
					self.toks[pos].type == TokType.INT.value or \
					(self.toks[pos].type == TokType.ID.value and \
					self.toks[pos + 1].type != TokType.OP_ASSIGN.value):
				expr.append(self.toks[pos])
				pos += 1
		except IndexError:
			self.__err(pos, 'unexpected end of expression')
		if not expr:
			self.__err(pos, 'expected arithmetic expression')

		# eval prefix arith expression
		for t in reversed(expr):
			if t.type == TokType.ID.value:
				if not t.lex in self.mem:
					self.__err(pos, 'uninitilized identifier \'' + t.lex + '\'')
				stack.append(self.mem[t.lex])
			elif t.type == TokType.INT.value:
				stack.append(int(t.lex))
			else:
				if len(stack) < 2:
					self.__err(pos, 'invalid arithmetic expression')
				stack.append(Par.__eval(t, stack.pop(), stack.pop()))
		if len(stack) != 1:
			self.__err(pos, 'invalid arithmetic expression')
		return pos

	@staticmethod
	def __eval(tok, x, y):
		if tok.type == TokType.OP_LE.value:
			return x <= y
		elif tok.type == TokType.OP_LT.value:
			return x < y
		elif tok.type == TokType.OP_GE.value:
			return x >= y
		elif tok.type == TokType.OP_GT.value:
			return x > y
		elif tok.type == TokType.OP_EQ.value:
			return x == y
		elif tok.type == TokType.OP_NE.value:
			return y != x
		elif tok.type == TokType.OP_ADD.value:
			return x + y
		elif tok.type == TokType.OP_SUB.value:
			return x - y
		elif tok.type == TokType.OP_MUL.value:
			return x * y
		elif tok.type == TokType.OP_DIV.value:
			return x // y
		elif tok.type == TokType.OP_MOD.value:
			return x % y
		elif tok.type == TokType.OP_INV.value:
			return y // x
		elif tok.type == TokType.OP_EXP.value:
			return x ** y
		else:
			raise Exception('expected operator')
			return False
