
Download and install Python-3.3.2

    wget http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz
    tar zxvf Python-3.3.2.tgz
    cd Python-3.3.2
    ./configure
    make
    make install

Install git * git-flow
    sudo apt-get install git git-flow

Install virtualenv & pip
    sudo apt-get install virtualenv python-pip

Make virtualenv for TDD
    virtualenv --no-site-packages tddenv
    source tddenv/bin/activate
    pip install django==1.5.2
    pip install selenium
    pip install mock

