import sys, subprocess
import shlex, json
import os, json
import threading
import argparse, logging
from dataupload import NLSDataUpload

SHELL_STATUS_RUN=1
SHELL_STATUS_STOP=0

def commandline():

    # parser.add_option("-i", '--interval', dest='password', default='nls72NSN', help='node heartbeat intervaltime default is 240')
    return parser.parse_args()
###########

def tokenize(string):
    return shlex.split(string)

def execute(cmd_tokens):
    """execute the nls-log command"""
    pid=os.fork()
    if pid==0:
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid>0:
        while True:
            wpid, status=os.waitpid(pid,0)
            if os.WIFEXITED(status) or os.WISIGNALED(status):
                break
    return SHELL_STATUS_RUN


def shell_loop():
    status=SHELL_STATUS_RUN
    while status==SHELL_STATUS_RUN:
        sys.stdout.write('nls-conf>>')
        sys.stdout.flush()
        cmd=sys.stdin.readline()
        cmd = cmd.strip()
        if not cmd:
            continue
        if cmd == "clear":
            sys.stdout.write("\n"*100)
            sys.stdout.flush()
            continue
        if cmd == 'exit' or cmd=='quit':
            status = SHELL_STATUS_STOP
            os._exit(0)

        cc = tokenize(cmd)
        ccmd = cc[0].lower()
        if ccmd in ['?', '-h', '--help']:
            t = threading.Thread(target=nls_cmds.main,args=(cc, ) )
            t.start()
            t.join()
            continue

        # local cmds like vi/vim /emacs
        if ccmd in nls_cmds.LOCAL_CMDS:
            cmd_tokens = tokenize(cmd)
            t = threading.Thread(target=execute, args=(cc, ))
            t.start()
            t.join()
        elif ccmd in nls_cmds.CMDS:
            t = threading.Thread(target=nls_cmds.main,args=(cc, ))
            t.start()
            t.join()
            # the complex command like find . | grep 
        elif ccmd in nls_cmds.REMOTE_CMDS:
            cc = ["remote_cmd", "%s"%cmd]
            t = threading.Thread(target=nls_cmds.main, args=(cc, ) )
            t.start()
            t.join()
        else:
            print("%s is not the nls_log command!" % ccmd)

def main():
    try:
        opt, var = commandline()
    except SystemExit as e:
        os._exit(0)

    ### the logger config
    fh = logging.FileHandler(opt.logpath)

    if opt.debug:
        nls_cmds.logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    elif opt.warning:
        nls_cmds.logger.setLevel(logging.WARNING)
        fh.setLevel(logging.WARNING)
    else:
        nls_cmds.logger.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
    nls_cmds.logger.addHandler(fh)
    nls_cmds.polling_time = int(opt.interval)
    # enter the shell loop
    shell_loop()

if __name__=="__main__":
    main()
