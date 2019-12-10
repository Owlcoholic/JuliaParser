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

	def exec(self):
		self.mem = {}
		self.__expect(0, TokType.KEY_FUNC.value)
		self.__expect(1, TokType.ID.value)
		self.__expect(2, TokType.PAREN_OPEN.value)
		self.__expect(3, TokType.PAREN_CLOSE.value)
		self.__expect(self.__parse_block(4, True), TokType.KEY_END.value)

	def __parse_block(self, pos, is_exec):
		pos = self.__parse_stmt(pos, is_exec)
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

		self.__err(pos, 'expected statement')

	def __parse_stmt_assign(self, pos, is_exec):
		self.__expect(pos, TokType.ID.value)
		self.__expect(pos + 1, TokType.OP_ASSIGN.value)
		id = self.toks[pos].lex
		stack = []
		pos = self.__parse_expr_arith(pos + 2, stack, is_exec)
		if is_exec:
			self.mem[id] = int(stack.pop())

		return pos

	def __parse_stmt_if(self, pos, is_exec):
		self.__expect(pos, TokType.KEY_IF.value)
		stack = []
		pos = self.__parse_expr_bool(pos + 1, stack, is_exec)
		cond = is_exec and stack[0]
		pos = self.__parse_block(pos, cond)
		self.__expect(pos, TokType.KEY_ELSE.value)
		pos = self.__parse_block(pos + 1, not cond and is_exec)
		self.__expect(pos, TokType.KEY_END.value)
		return pos + 1

	def __parse_stmt_while(self, pos, is_exec):
		self.__expect(pos, TokType.KEY_WHILE.value)
		bool_pos = pos + 1
		while True:
			stack = []
			pos = self.__parse_expr_bool(bool_pos, stack, is_exec)
			cond = is_exec and stack[0]
			pos = self.__parse_block(pos, cond)
			if not cond:
				break

		self.__expect(pos, TokType.KEY_END.value)
		return pos + 1

	def __parse_stmt_for(self, pos, is_exec):
		self.__expect(pos, TokType.KEY_FOR.value)
		self.__expect(pos + 1, TokType.ID.value)
		id = self.toks[pos + 1].lex
		pos = self.__parse_stmt_assign(pos + 1, is_exec)
		self.__expect(pos, TokType.COLON.value)
		stack = []
		pos = self.__parse_expr_arith(pos + 1, stack, is_exec)
		block_pos = pos
		while True:
			cond = is_exec and (self.mem[id] <= stack[0])
			pos = self.__parse_block(block_pos, cond)
			self.mem[id] += 1
			if not cond:
				break

		self.__expect(pos, TokType.KEY_END.value)
		return pos + 1

	def __parse_stmt_print(self, pos, is_exec):
		self.__expect(pos, TokType.KEY_PRINT.value)
		self.__expect(pos + 1, TokType.PAREN_OPEN.value)
		stack = []
		pos = self.__parse_expr_arith(pos + 2, stack, is_exec)
		self.__expect(pos, TokType.PAREN_CLOSE.value)
		if is_exec:
			print(stack[0])

		return pos + 1

	def __parse_expr_bool(self, pos, stack, is_exec):
		expr = []
		try:
			if not self.toks[pos].is_rel_op():
				self.__err(pos, 'expected boolean expression')
			expr.append(self.toks[pos])
			pos += 1
			while self.toks[pos].is_bin_op() or \
					self.toks[pos].type == TokType.INT.value or \
					(self.toks[pos].type == TokType.ID.value and \
					self.toks[pos + 1].type != TokType.OP_ASSIGN.value):
				expr.append(self.toks[pos])
				pos += 1
		except IndexError:
			self.__err(pos, 'unexpected end of file')

		if is_exec:
			self.__eval_expr(pos, stack, expr)

		return pos

	def __parse_expr_arith(self, pos, stack, is_exec):
		expr = []
		try:
			while self.toks[pos].is_bin_op() or \
					self.toks[pos].type == TokType.INT.value or \
					(self.toks[pos].type == TokType.ID.value and \
					self.toks[pos + 1].type != TokType.OP_ASSIGN.value):
				expr.append(self.toks[pos])
				pos += 1
		except IndexError:
			self.__err(pos, 'unexpected end of file')

		if not expr:
			self.__err(pos, 'expected arithmetic expression')

		if is_exec:
			self.__eval_expr(pos, stack, expr)

		return pos

	def __eval_expr(self, pos, stack, expr):
		for t in reversed(expr):
			if t.type == TokType.ID.value:
				if not t.lex in self.mem:
					self.__err(pos, 'uninitilized identifier \'' + t.lex + '\'')

				stack.append(self.mem[t.lex])
			elif t.type == TokType.INT.value:
				stack.append(int(t.lex))
			else:
				if len(stack) < 2:
					self.__err(pos, 'invalid expression')

				x = stack.pop()
				y = stack.pop()
				if t.type == TokType.OP_LE.value:
					stack.append(x <= y)
				elif t.type == TokType.OP_LT.value:
					stack.append(x < y)
				elif t.type == TokType.OP_GE.value:
					stack.append(x >= y)
				elif t.type == TokType.OP_GT.value:
					stack.append(x > y)
				elif t.type == TokType.OP_EQ.value:
					stack.append(x == y)
				elif t.type == TokType.OP_NE.value:
					stack.append(y != x)
				elif t.type == TokType.OP_ADD.value:
					stack.append(x + y)
				elif t.type == TokType.OP_SUB.value:
					stack.append(x - y)
				elif t.type == TokType.OP_MUL.value:
					stack.append(x * y)
				elif t.type == TokType.OP_DIV.value:
					stack.append(x // y)
				elif t.type == TokType.OP_MOD.value:
					stack.append(x % y)
				elif t.type == TokType.OP_INV.value:
					stack.append(y // x)
				elif t.type == TokType.OP_EXP.value:
					stack.append(x ** y)
				else:
					self.__err(pos, 'invalid expression')

		if len(stack) != 1:
			self.__err(pos, 'invalid expression')

	def __err(self, pos, msg):
		print('ERROR: ' + msg + ' @ ...', *self.toks[pos: pos + 2], '...', sep=' ')
		sys.exit(1)

	def __expect(self, pos, type):
		if pos >= len(self.toks) or self.toks[pos].type != type:
			self.__err(pos, 'expected token ' + TokType(type).name)
