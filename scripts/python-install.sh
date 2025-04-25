#!/bin/bash

set -e

PYTHON_VERSION=3.12.2
PYTHON_SRC_DIR="Python-$PYTHON_VERSION"
PYTHON_TAR="Python-$PYTHON_VERSION.tgz"

echo "🧹 Removing existing Python 3.12 if present..."

sudo rm -f /usr/local/bin/python3.12
sudo rm -f /usr/local/bin/pip3.12
sudo rm -rf /usr/local/lib/python3.12
sudo rm -rf /usr/local/include/python3.12
sudo rm -rf /usr/local/share/man/man1/python3.12.1
sudo rm -rf ~/.local/lib/python3.12
sudo rm -rf ~/.pyenv/versions/3.12.*

echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libncurses5-dev \
  libncursesw5-dev \
  libreadline-dev \
  libsqlite3-dev \
  libgdbm-dev \
  libdb5.3-dev \
  libbz2-dev \
  libexpat1-dev \
  liblzma-dev \
  tk-dev \
  uuid-dev \
  libffi-dev \
  wget \
  curl

echo "Downloading Python $PYTHON_VERSION..."
cd /tmp
rm -rf $PYTHON_SRC_DIR $PYTHON_TAR
wget https://www.python.org/ftp/python/$PYTHON_VERSION/$PYTHON_TAR
tar -xf $PYTHON_TAR

echo "Building Python $PYTHON_VERSION from source..."
cd $PYTHON_SRC_DIR
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall

echo "Python $PYTHON_VERSION installed as python3.12"