FROM jupyter/minimal-notebook:latest

USER root

RUN apt-get update \
 && apt-get install  -yq --no-install-recommends \
    libgl1-mesa-glx \
    libfontconfig1 \
    libxrender1 \
    libosmesa6 \
    git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
 

RUN conda install -y -c conda-forge -c cadquery -c set3mah microgen
RUN conda install -y -c conda-forge ipygany


RUN pip install jupyter_cadquery

USER jovyan
WORKDIR $HOME

COPY . ${HOME}
