#!/bin/bash

#echo $1

while read line
do
  echo "$line"
done < "${1:-/dev/stdin}"