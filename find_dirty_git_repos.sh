#!/bin/bash

RED_START="\e[0;31m"
GREEN_START="\e[0;32m"
COLOR_END="\e[00m"

dir=$1

pushd . > /dev/null

if [ "$dir" ]; then
    cd $dir > /dev/null
fi

echo
echo -e The following repositories have ${RED_START}uncommitted${COLOR_END} or ${GREEN_START}unpushed${COLOR_END} changes:

for d in `find . -maxdepth 3 -name .git`; do
    pushd . > /dev/null 
    cd $d > /dev/null
    cd .. > /dev/null
    status0=`git status --porcelain` 
    status1=`git status --porcelain -b`
    if [ "$status0" ]; then  
        echo -e ${RED_START}${PWD}${COLOR_END} 
    elif [[ $status1 == *"ahead"* ]]; then 
        echo -e ${GREEN_START}${PWD}${COLOR_END} 
    fi
    popd > /dev/null 
done

popd > /dev/null 
echo
