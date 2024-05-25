#!/bin/bash

# remove boot2root container if it exists
docker rm -f boot2root
cd sources
docker build -t boot2root .
cd .. 
docker run --name boot2root -v `pwd`/monitor/king.txt:/root/king.txt -d -p 80:5000 boot2root