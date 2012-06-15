#!/bin/bash

if [ ! -d ./build ]; then
    mkdir ./build
fi
export PATH=$PATH:/usr/local/bin
#echo "Compiling coffee script files..."
/usr/local/bin/coffee --output ./build --compile ./src	

#echo "Done..."