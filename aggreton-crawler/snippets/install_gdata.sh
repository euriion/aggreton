#!/bin/bash

wget https://gdata-python-client.googlecode.com/files/gdata-2.0.15.tar.gz
tar xvfz gdata-2.0.15.tar.gz

cd gdata-2.0.15
sudo python setup.py install
cd ..
rm -Rf gdata-2.0.15

