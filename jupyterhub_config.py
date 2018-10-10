import os, shutil

secret = os.environ.get("JUPYTERHUB_DUMMY_SECRET")
if not secret:
    raise Exception("Please set the JUPYTERHUB_DUMMY_SECRET environment variable.  This will be the password used by all users")

admins = os.environ.get("JUPYTERHUB_ADMINS") or ''
if not admins:
    raise Exception("Please set the JUPYTERHUB_ADMINS environment variable. This is a comma seperated list of usernames who will have admin access")

c.Authenticator.admin_users = set(admins.split(','))

c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
c.DummyAuthenticator.password = secret

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ.get('SINGLEUSER_IMAGE') or 'jupyterhub/singleuser'
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# spawn with Docker
# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]


# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

jupyter_volumes_dir = os.environ.get("JUPYTER_VOLUMES_DIR") or '/tmp/jupyter_volumes'
if not os.path.exists(jupyter_volumes_dir):
    os.mkdir(jupyter_volumes_dir,0o777)

def copyDirectory(src, dest):
        try:
            shutil.copytree(src, dest)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

def copy_samples_hook(spawner):
    username = spawner.user.name
    user_volume_dir = os.path.join(jupyter_volumes_dir,username)

    if not os.path.exists(user_volume_dir):
        os.mkdir(user_volume_dir,0o777)

        samples_notebook_dir = os.environ.get("SAMPLES_NOTEBOOK_DIR")
        if samples_notebook_dir:
            print("Copying {samples} to {user}".format(samples=samples_notebook_dir,user=user_volume_dir))
            copyDirectory(samples_notebook_dir,os.path.join(user_volume_dir,'samples'))

c.Spawner.pre_spawn_hook = copy_samples_hook

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {jupyter_volumes_dir + '/{username}': {"bind":notebook_dir,"mode":"rw"}}
