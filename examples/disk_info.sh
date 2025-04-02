#!/usr/bin/env bash
echo "Starting the python script...."
python ../bin/lcrun -i hosts.csv "df -H"
echo "Finalizing the script"
echo "end"
