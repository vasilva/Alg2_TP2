#!/bin/bash

# Directory containing .tsp files
DATA_DIR="data"
echo "-----------------------------------"

# Iterate over each .tsp file in the data directory
for tsp_file in "$DATA_DIR"/*.tsp;
do
    # Run the main.py script with the current .tsp file
    # with a time limit of 30 minutes
    echo "Running $tsp_file with Branch and Bound"
    if timeout 30m python3 main.py "$tsp_file" bb ; then
        echo "$tsp_file Complete"
    else
        echo "$tsp_file Timed out"
    fi
    echo "-----------------------------------"
done