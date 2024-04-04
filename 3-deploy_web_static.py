#!/usr/bin/python3
""" 3 - deploy_web_static.py """

from fabric.api import env, local, run
from datetime import datetime

# Define the Fabric environment variables
env.user = 'your_username'
env.key_filename = 'path_to_your_ssh_key'
env.hosts = ['54.173.104.114', '34.227.94.64']

def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive
    Returns: Path to the created archive if successful, None otherwise
    """
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = 'versions/web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(archive_name))
        return archive_name
    except Exception as e:
        print("An error occurred while creating the archive:", e)
        return None

def do_deploy(archive_path):
    """
    Deploys the archive to the web servers
    Args:
        archive_path: Path to the archive to be deployed
    Returns: True if successful, False otherwise
    """
    if archive_path is None:
        return False
    try:
        archive_name = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/{}'.format(archive_name.split('.')[0])
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf {} -C {}'.format(archive_path, archive_folder))
        run('rm {}'.format(archive_path))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))
        print("New version deployed!")
        return True
    except Exception as e:
        print("An error occurred while deploying the archive:", e)
        return False

def deploy():
    """
    Orchestrates the deployment process
    Returns: True if deployment successful, False otherwise
    """
    archive_path = do_pack()
    if not archive_path:
        print("No archive created. Deployment aborted.")
        return False
    return do_deploy(archive_path)
