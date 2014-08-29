#!/vpy/buildout/bin/py27
import os
import sys
import argparse
import subprocess

import futures


WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORKING_DIR)
sys.path.append(WORKING_DIR)


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port',
                    help='ssh connection port number')
parser.add_argument('-m', '--machine', required=True,
                    help='user and machine name without the id, ex: user@machine')
parser.add_argument('-i', '--included', required=True,
                    help='list of machine ids')
parser.add_argument('-e', '--excluded',
                    help='list of machine ids excluded')
parser.add_argument('-c', '--command', required=True,
                    help='shell command')
arguments = parser.parse_args()
#user = arguments.user
port = arguments.port
machine = arguments.machine

included = arguments.included
excluded = arguments.excluded
command = arguments.command


first_id, last_id = included.split('-')
excluded_list = excluded.split(',') if excluded else []

id_list = [id for id in map(str, range(int(first_id), int(last_id) + 1)) if id not in excluded_list]

machines = [''.join((machine, i)) for i in id_list]
machines = set(tuple([(machine, command) for machine in machines]))


def run_child(arg_tuple):
    try:
        if port:
            output, error = subprocess.Popen(['ssh', '-p', port, arg_tuple[0], arg_tuple[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        else:
            output, error = subprocess.Popen(['ssh', arg_tuple[0], arg_tuple[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        result = ''.join((output, error))
    except Exception as ex:
        result = ''.join(('Unknown exception: {0}'.format(ex), '\n\n', result))
    return str(result)


def run(arg_tuple):
    try:
        result = run_child(arg_tuple)
    except Exception as ex:
        print str(ex)
    return ''.join(('============================================ ', arg_tuple[0], ' ====================================', '\n', result))


with futures.ProcessPoolExecutor(max_workers=50) as executor:
    for result in executor.map(run, machines):
        print (result)
