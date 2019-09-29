#!/usr/bin/env python
import sys
import multiprocessing

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
        if int(fields[3]) > 2:
            app_data[fields[1]] = int(fields[3])
        else:
            sys.exit(0)

    return app_data


def get_score(data):
    sum_req = 0

    for app in data:
        sum_req = sum_req + data[app]

    score = CPUS*1000 -sum_req

    return score, sum_req

def split_apps(data):
    el_apps = {}
    an_apps = {}
    for key in data:
        if data[key] >= 400:
            an_apps[key] = data[key]
        else:
            el_apps[key] = data[key]

    return el_apps, an_apps


def calculate_shares(score, data):
    (elastic_apps, anelastic_apps) = split_apps(data)

    an_score, an_req = get_score(anelastic_apps)
    el_score, el_req = get_score(elastic_apps)

    if score >= 0:
        return score, data
    else:
        if an_score >= 0 and an_req != 0:
            return an_score, anelastic_apps
        elif an_score < 0:
            squeeze_apps(anelastic_apps, an_req)
            return 0, anelastic_apps
        elif an_req == 0:
            squeeze_apps(elastic_apps, el_req)
            return 0, elastic_apps


def squeeze_apps(apps, sum_req):
    for app in apps:
        apps[app] = apps[app]*(1000*CPUS)/sum_req

    return apps


def output_print(score, data):

        if score >=0:
               print  "score:1.0"
        else:
               print  "score:-1.0"

        for app in data:
            print "set_limit:"+app+":cpu.shares:"+format(data[app])

        return


def main():
    text = sys.stdin.readlines()
    # text = ['policy:BANKDB:cpu:1000\n', 'policy:webDB:cpu:1000\n', 'policy:myDB:cpu:2000\n', 'policy:something:cpu:500']
    input_string = prepare_input(text)
    # data = load_tabular_data('policy:SPAMBOT3:cpu:2000\npolicy:SPAMBOT30:cpu:2000\npolicy:SPAMBOT309:cpu:2000\n', separator=':')
    data = load_tabular_data(input_string, separator=':')

    score, sum_req = get_score(data)
    score, shares = calculate_shares(score, data)
    # print("score:1\nset_limit:red:cpu.shares:20")
    output_print(score, shares)
    sys.exit(0)


main()

