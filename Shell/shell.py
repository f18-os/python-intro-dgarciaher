#! /usr/bin/env python3

import os, sys, time, re

userInput = input('$')

pid = os.fork()

if pid < 0:
	os.write(2, ('Fork failed').encode())
	sys.exit(1)

elif pid == 0:
	if '>' in userInput:
		intputArray= userInput.split('>')
		os.close(1)
		sys.stdout = open(intputArray[1].strip(), "w")
		fd = sys.stdout.fileno()
		os.set_inheritable(fd,True)

		parent = intputArray[0].split()

		for dir in re.split(":", os.environ['PATH']):
			program = "%s/%s" % (dir, parent[0])
			try:
				os.execve(program, parent, os.environ)
			except FileNotFoundError:
				pass

		os.write(2, ("Child:    Error: Could not exec %s\n" % parent[0]).encode())
		sys.exit(1)
	elif '<' in userInput:
		intputArray= userInput.split('<')
		os.close(0)
		sys.stdin = open(intputArray[1].strip(), "r")
		fd = sys.stdin.fileno()
		os.set_inheritable(fd,True)

		parent = intputArray[0].split()
		print (parent)
		for dir in re.split(":", os.environ['PATH']):
				program = "%s/%s" % (dir, parent[0])
				try:
					os.execve(program, parent, os.environ)
				except FileNotFoundError:
					pass

		os.write(2, ("Child:    Error: Could not exec %s\n" % parent[0]).encode())
		sys.exit(1)

	else:
		parent = userInput.split()
		for dir in re.split(":", os.environ['PATH']):
				program = "%s/%s" % (dir, parent[0])
				try:
					os.execve(program, parent, os.environ)
				except FileNotFoundError:
					pass

		os.write(2, ("Child:    Error: Could not exec %s\n" % parent[0]).encode())
		sys.exit(1)

else:
	pid: os.wait()  