#!/usr/bin/env python

import sys, os

def create(str):
 	path = os.path.expanduser("/sys/fs/cgroup/cpu/"+ str[1]+"/"+str[3])
 	if not os.path.exists(path):
 		os.makedirs(path)

def remove(str):
 	path = os.path.expanduser("/sys/fs/cgroup/cpu/"+ str[1]+"/"+str[3])
 	os.removedirs(path)

def add(str):
 	path = os.path.expanduser("/sys/fs/cgroup/cpu/"+ str[1]+"/"+str[3])
 	f = open(path+"/tasks","w+")
 	f.write(str[4])
 	f.close()

def set_limit(str):
 	path = os.path.expanduser("/sys/fs/cgroup/cpu/"+ str[1]+"/"+str[3])
 	f = open(path+"/cpu.shares","w+")
 	f.write(str[5])
 	f.close()

def main():
 	while true:
 	try:
 		input = raw_input()
 		str = input.split(":")
 		if (str[0] == "create"):
 			create(str)
 		elif (str[0] == "remove"):
 			remove(str)
 		elif str[0] == "add":
 			add(str)
 		elif str[0] == "set_limit":
 			set_limit(str)
 		else:
 			print "Error"
 	except(EOFError):
 		break
if __name__ == "__main__":
     main()

