
Download and install Python-3.3.2

    wget http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz
    tar zxvf Python-3.3.2.tgz
    cd Python-3.3.2
    ./configure
    make
    make install

Install git & git-flow

    sudo apt-get install git
    sudo apt-get install git-flow

Install pip

    sudo apt-get install python-pip

Install virtualenv

        sudo apt-get install virtualenv (or pip install virtualenv)

Make virtualenv for TDD

    virtualenv --no-site-packages tddenv
    source tddenv/bin/activate
    pip install django==1.5.2
    pip install selenium
    pip install mock

Use git-flow

    mkdir kuiba
    git flow init

You can create a new repo on you github name kuiba, then add remote to you local

    git remote add origin git@github.com:ryanduan/kuiba.git

I use ssh.

You can visit [gitflow](https://github.com/nvie/gitflow) to know git-flow

And then, use travis-ci

    vim .travis.yml

Input:

    language: python
    python:
      - "2.7"
      - "3.3"
    env:
      - DJANGO_VERSION=1.5.2
    # command to install dependencies
    install:
      - "pip install ."
      - pip install -q Django==$DJANGO_VERSION
      - python setup.py -q install
    # command to run tests
    script: nosetests
