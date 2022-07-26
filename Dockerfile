FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

WORKDIR /workspaces/CEB
ENV PYTHONPATH=/workspaces/CEB

RUN mv /etc/apt/sources.list.d /etc/apt/_sources.list.d \
 && apt update \
 && apt install -y --no-install-recommends curl \
 && apt-key del 7fa2af80 \
 && curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb \
 && dpkg -i cuda-keyring_1.0-1_all.deb \
 && mv /etc/apt/_sources.list.d /etc/apt/sources.list.d

RUN apt update \
 && apt install -y --no-install-recommends \
      tmux \
      htop \
      git \
      ca-certificates \
      openssh-client \
      python3-pip \
      python3.8 \
      python3.8-distutils \
      libpython3.8-dev \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

RUN ln -f -s $(which python3.8) $(dirname $(which python3.8))/python3

COPY requirements.txt ./
RUN python3 -m pip install -U pip
RUN python3 -m pip install --prefer-binary -r requirements.txt
