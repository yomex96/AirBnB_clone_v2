#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["54.173.104.114", "34.227.94.64"]


def do_clean(number=0):
    """do_clean"""
    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    archives = sorted(os.listdir("versions"))
    for i in range(number):
        archives.pop()

    with lcd("versions"):
        for a in archives:
            local("rm ./{}".format(a))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        for a in archives:
            if "web_static_" in a:
                archives = a
        for i in range(number):
            archives.pop()
        for a in archives:
            run("rm -rf ./{}".format(a))
