# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 3 Interpreter - Python

from enum import Enum, auto


# returns Tok list from space delimited source code
def tokenize(src):
	toks = []
	for lex in src.split():
		t = Tok(lex)
		toks.append(t)

	return toks


class TokType(Enum):

	ID          = auto()
	INT         = auto()
	OP_ASSIGN   = auto()
	OP_LE       = auto()
	OP_LT       = auto()
	OP_GE       = auto()
	OP_GT       = auto()
	OP_EQ       = auto()
	OP_NE       = auto()
	OP_ADD      = auto()
	OP_SUB      = auto()
	OP_MUL      = auto()
	OP_DIV      = auto()
	OP_MOD      = auto()
	OP_INV      = auto()
	OP_EXP      = auto()
	KEY_FUNC    = auto()
	KEY_IF      = auto()
	KEY_ELSE    = auto()
	KEY_WHILE   = auto()
	KEY_FOR     = auto()
	KEY_END     = auto()
	KEY_PRINT   = auto()
	PAREN_OPEN  = auto()
	PAREN_CLOSE = auto()
	COLON       = auto()
	INVAL       = auto()


class Tok:

	@staticmethod
	def __is_id(lex):
		if lex.isalpha() and len(lex) == 1:
			return True

		return False

	@staticmethod
	def __is_int(lex):
		try:
			int(lex)
			return True
		except:
			return False

	def __init__(self, lex):
		self.lex = lex
		if Tok.__is_id(lex):
			self.type = TokType.ID.value
		elif Tok.__is_int(lex):
			self.type = TokType.INT.value
		elif lex == '=':
			self.type = TokType.OP_ASSIGN.value
		elif lex == '<=':
			self.type = TokType.OP_LE.value
		elif lex == '<':
			self.type = TokType.OP_LT.value
		elif lex == '>=':
			self.type = TokType.OP_GE.value
		elif lex == '>':
			self.type = TokType.OP_GT.value
		elif lex == '==':
			self.type = TokType.OP_EQ.value
		elif lex == '!=':
			self.type = TokType.OP_NE.value
		elif lex == '+':
			self.type = TokType.OP_ADD.value
		elif lex == '-':
			self.type = TokType.OP_SUB.value
		elif lex == '*':
			self.type = TokType.OP_MUL.value
		elif lex == '/':
			self.type = TokType.OP_DIV.value
		elif lex == '%':
			self.type = TokType.OP_MOD.value
		elif lex == '\\':
			self.type = TokType.OP_INV.value
		elif lex == '^':
			self.type = TokType.OP_EXP.value
		elif lex == 'function':
			self.type = TokType.KEY_FUNC.value
		elif lex == 'if':
			self.type = TokType.KEY_IF.value
		elif lex == 'else':
			self.type = TokType.KEY_ELSE.value
		elif lex == 'while':
			self.type = TokType.KEY_WHILE.value
		elif lex == 'for':
			self.type = TokType.KEY_FOR.value
		elif lex == 'end':
			self.type = TokType.KEY_END.value
		elif lex == 'print':
			self.type = TokType.KEY_PRINT.value
		elif lex == '(':
			self.type = TokType.PAREN_OPEN.value
		elif lex == ')':
			self.type = TokType.PAREN_CLOSE.value
		elif lex == ':':
			self.type = TokType.COLON.value
		else:
			self.type = TokType.INVAL.value

	def __str__(self):
		return self.lex

	def is_rel_op(self):
		if self.type in (TokType.OP_LE.value, TokType.OP_LT.value, \
				TokType.OP_GE.value, TokType.OP_GT.value, \
				TokType.OP_EQ.value, TokType.OP_NE.value):
			return True

		return False

	def is_bin_op(self):
		if self.type in (TokType.OP_ADD.value, \
				TokType.OP_SUB.value, \
				TokType.OP_MUL.value, \
				TokType.OP_DIV.value, \
				TokType.OP_MOD.value, \
				TokType.OP_INV.value, \
				TokType.OP_EXP.value):
			return True

		return False
