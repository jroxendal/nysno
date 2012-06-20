#!/bin/bash

if [ ! -d ./build ]; then
    mkdir ./build
fi
export PATH=$PATH:/usr/local/bin:/usr/local/Cellar/ruby/1.9.2-p290/bin
/usr/local/bin/coffee --output ./build --compile ./src	
haml index.haml -t html5 -E utf-8 -q > build/index.html
#scss -E utf-8 style.scss > build/style.css
compass compile
