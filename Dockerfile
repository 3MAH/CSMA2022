FROM jupyter/base-notebook:python-3.9.7

USER root
RUN apt-get update \
 && apt-get install  -yq --no-install-recommends \
    libgl1-mesa-glx \
    libfontconfig1 \
    libxrender1 \
    libosmesa6 \
    xvfb \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
# USER jovyan


RUN conda install -y -c conda-forge -c cadquery -c set3mah microgen simcoon fedoo

RUN conda install -y -c conda-forge ipygany ipyvtklink


RUN pip install jupyter_cadquery pyvista piglet pyvirtualdisplay

COPY . ${HOME}

WORKDIR $HOME

# allow jupyterlab for ipyvtk
ENV JUPYTER_ENABLE_LAB=yes
ENV PYVISTA_USE_IPYVTK=true
