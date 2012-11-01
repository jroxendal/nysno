#!/bin/bash

if [ ! -d ./build ]; then
    mkdir ./build
fi
export PATH=$PATH:/usr/local/bin:/usr/local/Cellar/ruby/1.9.2-p290/bin
/usr/local/bin/coffee --output ./build --compile ./src
haml src/index.haml -t html5  -q > build/index.html
compass compile > /dev/null
