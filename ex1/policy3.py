#!/usr/bin/env python
import sys
import multiprocessing
import os
import shutil
# import policy_test_case

CPUS = multiprocessing.cpu_count()


def prepare_input(text):
    input_string = ''
    for i in range(len(text)):
        input_string += input_string + text[i]

    return input_string


def load_tabular_data(inp, separator='\0'):
    app_data = {}
    lines = inp.split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            # skip empty lines and comments
            continue

        fields = line.split(separator)
        if fields[0] != 'policy' or fields[2] != 'cpu':
            print 'Wrong input keywords!'
            sys.exit(0)
        else:
            if int(fields[3]) > 2:
                app_data[fields[1]] = int(fields[3])
            else:
                print 'Wrong share request!'
                sys.exit(0)
    return app_data


def get_score(data):
    sum_req = 0

    for app in data:
        sum_req = sum_req + data[app]

    score = CPUS*1000 - sum_req
    return score, sum_req


def split_apps(data):
    total_el=0
    count_el=0
    for key in data:
        # if limit >= 300 we assume that application is anelastic
        if data[key] >= 300:
            pass
        else:
            count_el = count_el+1
            total_el = total_el + data[key]

    return count_el , total_el


def calculate_shares(data):
    count, total_el = split_apps(data)
    score, total = get_score(data)
    if score >= 0:

        print "score:1.0"
        
        if count == 0:

           for app in data:

               value=data[app]*1000*CPUS/total
               print "set_limit:"+app+":cpu.shares:"+format(value)
           


        else:
            
            for app in data:
               
                if data[app] >=300:
                     print "set_limit:"+app+":cpu.shares:"+format(data[app])
                else:
                     value=(1000*CPUS-total+total_el)/count
                     print "set_limit:"+app+":cpu.shares:"+format(value)
                
            
    else:
         print "score:-1.0"
         for app in data:
            print "set_limit:"+app+":cpu.shares:"+format(data[app])

    return




def main():

    text = sys.stdin.readlines()

    input_string = prepare_input(text)
    # data = load_tabular_data('policy:SPAMBOT3:cpu:2000\npolicy:SPAMBOT30:cpu:2000\npolicy:SPAMBOT309:cpu:2000\n', separator=':')
    data = load_tabular_data(input_string, separator=':')

    calculate_shares(data)
    sys.exit(0)


main()


