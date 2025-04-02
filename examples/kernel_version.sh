#!/usr/bin/env bash
echo "Starting the python script...."
python ../bin/lcrun -i hosts.csv "uname -a"
echo "Finalizing the script"
echo "end"
