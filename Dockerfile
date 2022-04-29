FROM jupyter/minimal-notebook:latest

USER root

RUN apt-get update -y && \
    apt install --no-install-recommends libgl1-mesa-glx -y && \
    rm -rf /var/lib/apt/lists/*
    
USER $NB_UID

RUN conda install -c conda-forge -c cadquery -c set3mah microgen simcoon fedoo -y

RUN pip install jupyter_cadquery pyvista ipyvtklink

# RUN conda install -c conda-forge ipyvtklink 

COPY . ${HOME}
