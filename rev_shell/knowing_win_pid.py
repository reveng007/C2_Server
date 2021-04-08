'''
python system and process utilities
Documentation: https://psutil.readthedocs.io/en/latest/
'''
import psutil

def getting_info(prf_list):

	#Storing process name in form of list
	process_list = []

	#Interating over running processes
	for proc in psutil.process_iter():

		try:
			proc_info = proc.as_dict(attrs=['pid','name'])

			''' 
			Checking for running processes,
			and extracting corresponding name and pid.
			'''

			for ps_name in prf_list:

				if ps_name.lower() in proc_info['name'].lower():
					process_list.append(proc_info)

		except (psutil.NoSuchProcess, psutil.AccessDenied):
			pass

	return process_list
