# $language = "python"
# $interface = "1.0"
import random
import re
import time
import datetime
import string


def main():

	run = 1
	
	while run:
		
		sleeptime = 30
		
		a = [1,2]
		
		for i in a[::1]:
		
			text_tx = 'BB_add_cmds 2 ' + str(i) + ' 0 0 0' + '\r\n'
			
			crt.Screen.Send(text_tx)
			
			if (crt.Screen.WaitForString('Lock=0x0',sleeptime)):
			
				crt.Dialog.MessageBox(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  unlock!","session",32|3)
				
				run = 0
				
			#time.sleep(sleeptime)
	
main()