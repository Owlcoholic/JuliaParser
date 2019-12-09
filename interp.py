#!/usr/bin/env python3

import sys
from tok import tokenize
from par import Par

def err(msg):
	print('ERROR: ' + msg)
	print('Usage: interp.py <FILE>')
	sys.exit(1)

def readsrc():
	if len(sys.argv) != 2:
		err('invalid number of arguments')
	try:
		f = open(sys.argv[1], 'r')
		src = f.read()
		f.close
	except:
		err('can not open file \'' + sys.argv[1] + '\'')
	return src

par = Par(tokenize(readsrc()))
par.exec()
