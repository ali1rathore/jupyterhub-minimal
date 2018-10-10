# jupyterhub-minimal
The fastest way to setup a (highly insecure) jupyterhub instance

# Installation : Ubuntu 18.04

Start with a new Ubuntu instance logged in as user "ubuntu".  All we need is docker and conda to get us started.

The following command will install docker, conda, and build the docker image for the users

```bash
wget -qO - https://raw.githubusercontent.com/ali1rathore/jupyterhub-minimal/master/install.sh | bash
```

# Now set the following environment variables

1. The password that all users will use to login

```bash
export JUPYTERHUB_DUMMY_SECRET=<your super secret password>
```

2. The name of the admins who can manage users

```bash
export JUPYTERHUB_ADMINS=admin,admin2
```

3. [Optional] The location to persist users' home directories

```bash
export JUPYTER_VOLUMES_DIR=/home/ubuntu/jupyterhub_users
```

> The default path is `/tmp/jupyterhub_volumes'

4. [Optional] Location of sample notebooks.

```bash
export SAMPLES_NOTEBOOK_DIR=<path/to/your/samples>
```

5. [Optional] The name of the singleuser Docker image

```bash
export SINGLEUSER_IMAGE=<your custom docker image>
```

> The default Docker image is `jupyterhub/singleuser`

# Start JupyterHub

```
sudo PATH=$PATH:/opt/conda/bin JUPYTERHUB_DUMMY_SECRET=<your-super-secret> JUPYTERHUB_ADMINS=admin1,admin2 SINGLEUSER_IMAGE=singleuser /opt/conda/bin/jupyterhub -f jupyterhub_config.py
```

Now connect to port 8000 to login to JupyterHub
