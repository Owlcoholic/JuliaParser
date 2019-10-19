#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 1 Scanner - Python

import getopt, sys, enum

# prints usage heredoc
def usage():
	print('''
Usage: julia_lexer.py [ -o <OUTPUT_FILE> ] <SOURCE_FILE>...
Tokenizes SOURCE_FILE... and outputs a human readable list of tokens to the
standard output. Use option -o to output to OUTPUT_FILE.
'''[1:-1])

# returns True if lexeme is a single letter, or False otherwise
def is_id(lex):
	if lex.isalpha() and len(lex) == 1:
		return True
	return False

# returns True if lexeme is an integer literal, or False otherwise
def is_int(lex):
	try:
		int(lex)
		return True
	except ValueError:
		return False

# enum constants for each type of token
class TokenType(enum.Enum):
	INVAL       = 0
	ID          = 1
	INT         = 2
	OP_ASSIGN   = 3
	OP_LE       = 4
	OP_LT       = 5
	OP_GE       = 6
	OP_GT       = 7
	OP_EQ       = 8
	OP_NE       = 9
	OP_ADD      = 10
	OP_SUB      = 11
	OP_MUL      = 12
	OP_DIV      = 13
	OP_MOD      = 14
	OP_INV      = 15
	OP_EXP      = 16
	KEY_FUNC    = 17
	KEY_PRINT   = 18
	KEY_WHILE   = 19
	KEY_FOR     = 20
	KEY_IF      = 21
	KEY_ELSE    = 22
	KEY_END     = 23
	PAREN_OPEN  = 24
	PAREN_CLOSE = 25
	COLON       = 26

	# returns the name of the enum constant
	def __str__(self):
		return self.name

class Token:
	# init token object from the lexeme
	def __init__(self, lex):
		if is_id(lex):
			self.type = TokenType.ID.value
			self.id_name = lex
		elif is_int(lex):
			self.type = TokenType.INT.value
			self.int_val = int(lex)
		elif lex in '=':
			self.type = TokenType.OP_ASSIGN.value
		elif lex in '<=':
			self.type = TokenType.OP_LE.value
		elif lex in '<':
			self.type = TokenType.OP_LT.value
		elif lex in '>=':
			self.type = TokenType.OP_GE.value
		elif lex in '>':
			self.type = TokenType.OP_GT.value
		elif lex in '==':
			self.type = TokenType.OP_EQ.value
		elif lex in '!=':
			self.type = TokenType.OP_NE.value
		elif lex in '+':
			self.type = TokenType.OP_ADD.value
		elif lex in '-':
			self.type = TokenType.OP_SUB.value
		elif lex in '*':
			self.type = TokenType.OP_MUL.value
		elif lex in '/':
			self.type = TokenType.OP_DIV.value
		elif lex in '%':
			self.type = TokenType.OP_MOD.value
		elif lex in '\\':
			self.type = TokenType.OP_INV.value
		elif lex in '^':
			self.type = TokenType.OP_EXP.value
		elif lex in 'function':
			self.type = TokenType.KEY_FUNC.value
		elif lex in 'print':
			self.type = TokenType.KEY_PRINT.value
		elif lex in 'while':
			self.type = TokenType.KEY_WHILE.value
		elif lex in 'for':
			self.type = TokenType.KEY_FOR.value
		elif lex in 'if':
			self.type = TokenType.KEY_IF.value
		elif lex in 'else':
			self.type = TokenType.KEY_ELSE.value
		elif lex in 'end':
			self.type = TokenType.KEY_END.value
		elif lex in '(':
			self.type = TokenType.PAREN_OPEN.value
		elif lex in ')':
			self.type = TokenType.PAREN_CLOSE.value
		elif lex in ':':
			self.type = TokenType.COLON.value
		else:
			self.type = TokenType.INVAL.value
			self.inval_lex = lex

	# returns human readable token
	def __str__(self):
		s = '<' + str(TokenType(self.type))
		if self.type == TokenType.INVAL.value:
			s += '(' + self.inval_lex + ')'
		elif self.type == TokenType.ID.value:
			s += '(' + self.id_name + ')'
		elif self.type == TokenType.INT.value:
			s += '(' + str(self.int_val) + ')'
		return s + '>'

# creates list of tokens from the source code
def tokenize(src):
	tokens = []
	for lex in src.split():
		t = Token(lex)
		tokens.append(t)
	return tokens

def main():
	# get args
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'ho:')
	except getopt.GetoptError as err:
		print('ERROR: ' + str(err) + '\n')
		usage()
		sys.exit(1)

	# handle opts
	outfile = '\0'
	for o, a in opts:
		if o in ('-h'):
			usage()
			sys.exit(0)
		elif o in ('-o'):
			outfile = str(a)
		else:
			print('ERROR: invalid option\n')
			usage()
			sys.exit(1)

	# check for missing arg
	if not args:
		print('ERROR: missing argument\n')
		usage()
		sys.exit(1)

	# concat files into a string
	src = ''
	for a in args:
		try:
			f = open(a ,'r')
			src += f.read()
			f.close()
		except:
			print('ERROR: can not open file \'' + a + '\'')
			sys.exit(1)

	# create token list
	tokens = tokenize(src)

	# print token list
	if outfile != '\0':
		try:
			f = open(outfile, 'w+')
			print(*tokens, sep=' ', file=f)
			f.close()
		except:
			print('ERROR: can not write to file \'' + outfile + '\'')
			sys.exit(1)
	else:
		print(*tokens, sep=' ')

if __name__ == "__main__":
	main()
