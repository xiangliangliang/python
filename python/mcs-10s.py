# $language = "python"
# $interface = "1.0"
import random
import re
import time
import datetime
import string


def main():

	while 1:
		
		sleeptime = 10
		
		a = [1,2]
		
		for i in a[::1]:
			text_tx = 'BB_add_cmds 2 ' + str(i) + ' 0 0 0' + '\r\n'
			crt.Screen.Send(text_tx)
			time.sleep(sleeptime)
	
main()