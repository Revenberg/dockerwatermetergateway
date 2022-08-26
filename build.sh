#!/bin/bash

# version 2022-08-26 15:20

cd /home/pi/dockerwatermetergatewayexporter

if [ -n "$1" ]; then
  ex=$1
else
  rc=$(git remote show origin |  grep "local out of date" | wc -l)
  if [ $rc -ne "0" ]; then
    ex=true
  else
    ex=false
  fi
fi

if [ $ex == true ]; then
    git pull
    chmod +x build.sh

    docker image build -t revenberg/watermetergatewayexporter:latest .

    #docker push revenberg/watermetergatewayexporter:latest

    # testing: 

    echo "==========================================================="
    echo "=                                                         ="
    echo "= docker-conmponse revenberg/watermetergatewayexporter up ="
    echo "=                                                         ="
    echo "==========================================================="
fi

cd -