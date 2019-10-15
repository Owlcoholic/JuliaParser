#!/usr/bin/env python3

import sys
import enum

# returns True if lexeme is a single letter, or False otherwise
def is_id(lexeme):
	if lexeme.isalpha() and len(lexeme) == 1:
		return True
	return False

# returns True if lexeme is an integer literal, or False otherwise
def is_int(lexeme):
	try:
		int(lexeme)
		return True
	except ValueError:
		return False

class TokenType(enum.Enum):
	ID        = 1
	INT       = 2
	OP_ASSIGN = 3
	OP_LE     = 4
	OP_LT     = 5
	OP_GE     = 6
	OP_GT     = 7
	OP_EQ     = 8
	OP_NE     = 9
	OP_ADD    = 10
	OP_SUB    = 11
	OP_MUL    = 12
	OP_DIV    = 13
	INVAL     = 14

	def __str__(self):
		return self.name

class Token:
	# init Token from given lexeme
	def __init__(self, lexeme):
		self.lexeme = lexeme
		if is_id(lexeme):
			self.type = TokenType.ID.value
			self.id_name = lexeme
		elif is_int(lexeme):
			self.type = TokenType.INT.value
			self.int_val = int(lexeme)
		elif lexeme == "=":
			self.type = TokenType.OP_ASSIGN.value
		elif lexeme == "<=":
			self.type = TokenType.OP_LE.value
		elif lexeme == "<":
			self.type = TokenType.OP_LT.value
		elif lexeme == ">=":
			self.type = TokenType.OP_GE.value
		elif lexeme == ">":
			self.type = TokenType.OP_GT.value
		elif lexeme == "==":
			self.type = TokenType.OP_EQ.value
		elif lexeme == "~=":
			self.type = TokenType.OP_NE.value
		elif lexeme == "+":
			self.type = TokenType.OP_ADD.value
		elif lexeme == "-":
			self.type = TokenType.OP_SUB.value
		elif lexeme == "*":
			self.type = TokenType.OP_MUL.value
		elif lexeme == "/":
			self.type = TokenType.OP_DIV.value
		else:
			self.type = TokenType.INVAL.value

	def __str__(self):
		if self.type == TokenType.ID.value:
			return "<" + str(TokenType(self.type)) + ":" + self.id_name + ">"
		elif self.type == TokenType.INT.value:
			return "<" + str(TokenType(self.type)) + ":" + str(self.int_val) + ">"
		return "<" + str(TokenType(self.type)) + ">"

# generates a list of tokens from the source code
def tokenize(src):
	tokens = []
	for lexeme in src.split():
		t = Token(lexeme)
		tokens.append(t)
	return tokens

# Usage: julia_lexer.py <FILE>...
def main():
	# exit on missing args
	if len(sys.argv) <= 1:
		print("missing argument(s)")
		sys.exit(1)

	# concat all files to a single string
	src = ""
	for i, arg in enumerate(sys.argv[1:]):
		try:
			f = open(arg ,"r")
			src += f.read()
			f.close()
		except:
			print("can't open file \'" + arg + "\'")
			sys.exit(1)

	# create Token list
	tokens = tokenize(src)

	# print list for testing
	print(*tokens, sep='\n')
  
  sys.exit(0)

if __name__ == "__main__":
	main()
