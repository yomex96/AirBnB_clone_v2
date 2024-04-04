#!/usr/bin/python3
import os
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['54.173.104.114', '34.227.94.64']

def create_archive_name():
    """Generates a unique name for the archive."""
    current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"versions/web_static_{current_time}.tgz"

def create_archive():
    """Creates a tar gzipped archive of the directory web_static."""
    archive_name = create_archive_name()
    if not os.path.exists("versions"):
        os.makedirs("versions")
    if local(f"tar -cvzf {archive_name} web_static").failed:
        return None
    return archive_name

def distribute_archive(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    release_folder = f"/data/web_static/releases/{file_name.split('.')[0]}"
    if put(archive_path, f"/tmp/{file_name}").failed:
        return False
    commands = [
        f"rm -rf {release_folder}",
        f"mkdir -p {release_folder}",
        f"tar -xzf /tmp/{file_name} -C {release_folder}",
        f"rm /tmp/{file_name}",
        f"mv {release_folder}/web_static/* {release_folder}/",
        f"rm -rf {release_folder}/web_static",
        "rm -rf /data/web_static/current",
        f"ln -s {release_folder}/ /data/web_static/current"
    ]
    for command in commands:
        if run(command).failed:
            return False
    return True

def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = create_archive()
    if not archive_path:
        return False
    return distribute_archive(archive_path)

