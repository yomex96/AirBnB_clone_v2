#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import tarfile
import os.path
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ["54.173.104.114", "34.227.94.64"]
env.key_filename = "~/id_rsa"


def do_pack():
    """Creates a tar gzipped archive of the directory web_static."""
    target_dir = os.path.join(os.getcwd(), "versions")
    os.makedirs(target_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = f"web_static_{timestamp}.tgz"
    with tarfile.open(os.path.join(target_dir, archive_name), "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))
    return os.path.join(target_dir, archive_name)


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        archive_name = os.path.basename(archive_path)
        release_folder = f"/data/web_static/releases/{archive_name.split('.')[0]}"
        put(archive_path, "/tmp/")
        sudo(f"mkdir -p {release_folder}")
        sudo(f"tar -xzf /tmp/{archive_name} -C {release_folder}")
        sudo(f"rm /tmp/{archive_name}")
        sudo(f"mv {release_folder}/web_static/* {release_folder}/")
        sudo(f"rm -rf {release_folder}/web_static")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {release_folder}/ /data/web_static/current")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def create_deploy_local():
    """Creates and deploys locally a new version."""
    archive_path = do_pack()
    if not archive_path:
        return False
    release_folder = os.path.join("/data/web_static/releases", os.path.basename(archive_path).split('.')[0])
    try:
        os.makedirs(release_folder)
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=release_folder)
        os.remove(archive_path)
        current_symlink = "/data/web_static/current"
        if os.path.islink(current_symlink):
            os.unlink(current_symlink)
        os.symlink(release_folder, current_symlink)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def create_deploy_local_with_html():
    """Creates and deploys locally a new version with my_index.html inside."""
    archive_path = do_pack()
    if not archive_path:
        return False
    release_folder = os.path.join("/data/web_static/releases", os.path.basename(archive_path).split('.')[0])
    try:
        os.makedirs(release_folder)
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=release_folder)
        html_content = "<html><head></head><body>New version with my_index.html inside</body></html>"
        with open(os.path.join(release_folder, "my_index.html"), "w") as f:
            f.write(html_content)
        os.remove(archive_path)
        current_symlink = "/data/web_static/current"
        if os.path.islink(current_symlink):
            os.unlink(current_symlink)
        os.symlink(release_folder, current_symlink)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

