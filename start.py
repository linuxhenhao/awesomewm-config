#!/usr/bin/env python3
import subprocess
from multiprocessing import Process
from functools import partial
import logging
import time

logging.basicConfig(level=logging.DEBUG)
# program in format ('binary_name', 'args', 'pgrep -f's match str')
# if match str is '', using the 'binary_name' instead
PROGRAMS = [('xcompmgr', None, ''),
            ('volumeicon', None, ''),
            # ('/usr/bin/ss-local', '-c /etc/shadowsocks.json', ''),
            ('lxpolkit', None, ''),
            # ('kupfer', '--no-splash', ''),
            ('fcitx', None, ''),
            ('copyq', None, ''),
            ('wicd-client', '-t', 'wicd-client.py'),
            ]

def run_in_process(argsList):
    def run_command(argsList):
        try:
            output = subprocess.check_output(argsList)
        except Exception as e:
            print(e)
            return
        print(output)

    print('preparing to run in process {}'.format(argsList))
    p = Process(target=partial(run_command, argsList))
    p.daemon = True
    p.start()
    print('running in process {}'.format(argsList))


def start():
    remain = True
    while remain:
        remain = False  # set remain to False before run programs
        for name, args, pattern in PROGRAMS:
            try:
                if(pattern == ''):
                    subprocess.check_output(('pgrep', '-f', name))
                else:
                    subprocess.check_output(('pgrep', '-f', pattern))
                # -f option for pgrep to grep both commands and args
                logging.debug('{} is running'.format(name))
            except:  # exception will be raised if no pid of name was found
                # run this program
                remain = True
                # if any of the programs need to be run, set remain to True
                logging.debug('{} is not running'.format(name))
                if args is not None:
                    argList = args.split(' ')
                    argList.insert(0, name)
                else:
                    # no args
                    argList = [name]
                print(argList)
                run_in_process(argList)
        time.sleep(1)
    logging.debug('startup finished')

start()
