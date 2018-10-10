# jupyterhub-minimal
The fastest way to setup a (highly insecure) jupyterhub instance

# Installation : Ubuntu 18.04

Start with a new Ubuntu instance logged in as user "ubuntu".  All we need is docker and conda to get us started.

You can copy the following into the host's terminal.

```bash
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# add the docker-ce repository and install docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce -y

# install conda and jupyterhub dependancies
sudo mkdir /opt/conda
sudo chown -R ubuntu /opt/conda

wget -q https://repo.continuum.io/miniconda/Miniconda3-4.5.1-Linux-x86_64.sh -O /tmp/miniconda.sh  && \
    echo '0c28787e3126238df24c5d4858bd0744 */tmp/miniconda.sh' | md5sum -c - && \
    bash /tmp/miniconda.sh -f -b -p /opt/conda && \
    /opt/conda/bin/conda install --yes -c conda-forge \
      python=3.6 sqlalchemy tornado jinja2 traitlets requests pip pycurl \
      nodejs configurable-http-proxy jupyterhub notebook && \
    /opt/conda/bin/pip install --upgrade pip dockerspawner jupyterhub-dummyauthenticator && \
    rm /tmp/miniconda.sh

export PATH=$PATH:/opt/conda/bin

# Now build the docker image that users will use. This command will build a container from the Dockerfile in this repo
export SINGLEUSER_IMAGE=singleuser
sudo docker build -t singleuser https://raw.githubusercontent.com/ali1rathore/jupyterhub-minimal/master/Dockerfile

# Download the jupyterhub configuration file (jupyterhub_config.py) from this repo
wget https://raw.githubusercontent.com/ali1rathore/jupyterhub-minimal/master/jupyterhub_config.py

# remove iptable filters (OMG!please dont ever do this!)
sudo iptables -F
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
export PATH=$PATH:/opt/conda/bin
jupyterhub -f jupyterhub_config.py
```

Now connect to port 8000 to login to JupyterHub
