# Contains Python Hive SQL client for connecting to Spark Thfitserver

FROM jupyterhub/singleuser

USER root
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install wget git bzip2 gcc build-essential libsasl2-dev && \
    apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jovyan
RUN pip install --upgrade ipython-sql pyhive thrift sasl thrift_sasl pip pandas altair vega_datasets vega ipython-autotime
