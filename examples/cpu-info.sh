#!/usr/bin/env bash
echo "Starting the python script...."
python ../bin/lcrun -i hosts.csv -i hosts "lscpu"
echo "Finalizing the script"
echo "end"
