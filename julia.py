#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 3 Interpreter - Python

import sys
from tok import tokenize
from par import Par


def err(msg):
	print('julia.py: ' + msg)
	print('Usage: julia.py <FILE>')
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
