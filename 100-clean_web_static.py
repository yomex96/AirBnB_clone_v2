#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['54.173.104.114', '34.227.94.64']


def do_clean(number=1):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.
            If number is 0 or 1, keeps only the most recent archive.
            If number is 2, keeps the most and second-most recent archives, etc.
    """
    number = max(int(number), 1)

    with cd("/data/web_static/releases"):
        archives = run("ls -tr | grep 'web_static_'").split()
        if len(archives) > number:
            to_delete = archives[:-number]
            run("rm -rf {}".format(" ".join(to_delete)))

    with lcd("versions"):
        local_archives = os.listdir(".")
        local_archives = [archive for archive in local_archives if "web_static_" in archive]
        if len(local_archives) > number:
            to_delete_local = sorted(local_archives)[:-number]
            [local("rm -rf {}".format(archive)) for archive in to_delete_local]

