#!/bin/bash

# remove boot2root container if it exists
docker rm -f boot2root
cd sources
docker build -t boot2root .
cd .. 
docker system prune -f 
docker run --name boot2root --hostname vhc_b2r_koth -v `pwd`/monitor/king.txt:/root/king.txt -d -p 80:5000 boot2root