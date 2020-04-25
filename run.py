from os import system
from datetime import datetime
import time

while 1:
	print("time: ", datetime.now())
	sleep = 5 - datetime.now().minute % 5
	if sleep == 5:
		system('python main2.py')
		time.sleep(sleep * 60)
	else:
		time.sleep(sleep * 60)