#!/bin/bash

source /opt/conda/etc/profile.d/conda.sh

export CONDA_ENV_DIR="/home/pfred/env"

# installing python and R packages
if [ ! -d $CONDA_ENV_DIR ];
then
    conda create -y -p $CONDA_ENV_DIR --file "./conda_requirements.txt"
fi
conda activate $CONDA_ENV_DIR

# installing ensembl_rest (not available in conda channels)
pip install ensembl_rest

# setting up environment variables
cat /home/pfred/setup_env.sh >> ~/.bashrc
source ~/.bashrc

if [ ! -d $BOWTIE_HOME ];
then
    echo "Downloading bowtie..."

    cd $PFRED_HOME/scripts
    for letter in "a b c d"
    do
        wget https://github.com/pfred/pfred-docker/releases/download/v1.0-alpha/bowtie.tar.gz.parta$letter
    done

    cat bowtie.tar.gz.parta* > bowtie.tar.gz
    rm bowtie.tar.gz.parta*

    tar -xvf bowtie.tar.gz
    rm bowtie.tar.gz
fi

if [ ! -d $RUN_DIR ];
then
    mkdir $RUN_DIR
fi

# symlink to do things correctly
cd /usr/local/bin
ln -s $BOWTIE
for filename in $SCRIPTS_DIR/*.sh $SCRIPTS_DIR/*.py $SCRIPTS_DIR/*.pl $SCRIPTS_DIR/*.pm;
do
    chmod +x $filename
    ln -s $filename
done
