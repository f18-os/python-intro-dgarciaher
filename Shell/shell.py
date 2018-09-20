#! /usr/bin/env python3

import os, sys, time, re

while True:

	wd = os.getcwd().split("/")		# gets current working directory and splits it by forward slash

	if "PS1" in os.environ:
		os.write(1, (os.environ["PS1"]).encode())			# writes path it is currenly on
	else:
		os.write(1, (wd[(len(wd)-1)] + '$').encode())		# writes path if previous method does not work

	try :
		userInput = input().split()		# checks for EOF when C^D is pressed by user
	except EOFError:
		sys.exit(1)


	if userInput == [] :		# continues the loop if user presses enter
		continue

	if 'exit' in userInput :	# terminates if user enters exit
		break

	if 'cd' in userInput :		# changes directories
		change = userInput
		os.chdir(change[1])
		continue


	pid = os.fork()

	if pid < 0:
		os.write(2, ('Fork failed').encode())		# checks fork error
		sys.exit(1)

	elif pid == 0:		# is child
		if '>' in userInput:
			intputArray= userInput.split('>')				# checks for > symbol and executes command
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
		elif '<' in userInput:									# checks for < symbol and executes command
			intputArray= userInput.split('<')
			os.close(0)
			sys.stdin = open(intputArray[1].strip(), "r")
			fd = sys.stdin.fileno()
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

		else:
			if userInput[-1] == "&":		# checks if there's an & for the sleep command
				#sleep logic
				userInput = userInput[0:-1]
				parent = userInput
				if "/" in parent[0]:			# checks for commands such as cat in a path
					program = parent[0]
					try:
						os.execve(program, parent, os.environ)
					except FileNotFoundError:
						pass
				else :
					for dir in re.split(":", os.environ['PATH']):
						program = "%s/%s" % (dir, parent[0])
						try:
							os.execve(program, parent, os.environ)
						except FileNotFoundError:
							pass

				os.write(2, ("Child:    Error: Could not exec %s\n" % parent[0]).encode())
				sys.exit(1)
			else:
				parent = userInput
				for dir in re.split(":", os.environ['PATH']):		# executes commands that do not fit in any of the above conditions
						program = "%s/%s" % (dir, parent[0])
						try:
							os.execve(program, parent, os.environ)
						except FileNotFoundError:
							pass

				os.write(2, ("Child:    Error: Could not exec %s\n" % parent[0]).encode())
				sys.exit(1)				
	else:
		if not '&' in userInput:	# waits in the case of sleep command
		 	os.wait()