#!/usr/bin/env python

import sys
import os
import shutil


def create(app_name,folder):

    file_path="/sys/fs/cgroup/cpu/"+folder+"/"+app_name+""

    if not os.path.isdir(file_path): 
      os.makedirs(file_path)

    return

def remove(app_name,folder):

    file_path="/sys/fs/cgroup/cpu/"+folder+"/"+app_name+""

    if os.path.isdir(file_path):
        shutil.rmtree(file_path, ignore_errors=True)

    return

def add(app_name,pid,folder):

    file_path="/sys/fs/cgroup/cpu/"+folder+"/"+app_name+"/tasks"  
    with open(file_path,"w") as myfile:
        myfile.write(pid)
    return

def set_limit(app_name,val,folder):

    file_path="/sys/fs/cgroup/cpu/"+folder+"/"+app_name+"/cpu.shares"   
    with open(file_path,"w") as myfile:
        myfile.write(val)
 
    return

def main():
 
    # read input whose form is -> create|remove:<monitor>:cpu:<application_name>
    # or add:<monitor>:cpu:<application_name>:<process id>
    # or set_limit:<monitor>:cpu:<application_name>:cpu.shares:<value>
    lines = raw_input()

    # split input 
    argc = lines.split(":")

    # argc[0]= create | remove | add | set_limit
    # argc[1]= <monitor>
    # argc[2]= cpu
    # argc[3]= <application name>
    # argc[4]= add-> <process id> | set_limit -> cpu.shares
    # argc[5]= set_limit -> <value>
    
    if argc[0] == 'create':
	create(argc[3],argc[1])

    elif argc[0] == 'add':
        add(argc[3],argc[4],argc[1])
 
    elif argc[0] == 'remove':
        remove(argc[3],argc[1])
 
    elif argc[0]== 'set_limit':
         set_limit(argc[3],argc[5],argc[1])
    else :
         print "Not appropriate input given ! -> ERROR "


if __name__ == "__main__":
     main()
