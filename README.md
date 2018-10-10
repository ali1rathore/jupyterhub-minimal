# jupyterhub-minimal
The fastest way to setup a (highly insecure) jupyterhub instance

# Installation : Ubuntu 18.04

Start with a new Ubuntu instance logged in as user "ubuntu".  All we need is docker and conda to get us started.

The following command will install docker, conda, and build the docker image for the users

```bash
wget -qO - https://raw.githubusercontent.com/ali1rathore/jupyterhub-minimal/master/install.sh | bash
```

# Start JupyterHub

```
PATH=$PATH:/opt/conda/bin JUPYTERHUB_DUMMY_SECRET=<your-super-secret> JUPYTERHUB_ADMINS=admin1,admin2 SINGLEUSER_IMAGE=singleuser /opt/conda/bin/jupyterhub -f jupyterhub_config.py
```

Now connect to port 8000 to login to JupyterHub


# Configuration Variables:

Set these environment variables in the commandline to modify the default configuration.

1. JUPYTERHUB_DUMMY_SECRET: The password that all users will use to login

2. JUPYTERHUB_ADMINS: The name of the admins who can manage users

3. JUPYTER_VOLUMES_DIR=`/tmp/jupyterhub_volumes`: The location to persist users' home directories

4. SAMPLES_NOTEBOOK_DIR (optional): Location of sample notebooks.

5. SINGLEUSER_IMAGE=`jupyterhub/singleuser`: The name of the singleuser Docker image

# Troubleshooting

Sometimes Docker's usage if `iptables` may cause problems with connecting from your browser to JupyterHub or from a notebook to the Spark Thriftserver.  The following will disable iptables and restart Docker, which seems to work for now.

```bash
 sudo iptables -X
 sudo service docker restart
 ```
 
 Now start JupyterHub
