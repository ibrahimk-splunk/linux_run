#!/usr/bin/env bash
echo "Starting the python script...."
python ../bin/lcrun -i hosts.csv "cat /etc/*release"
echo "Finalizing the script"
echo "end"
