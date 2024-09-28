#!/bin/bash
for script_file in $(ls *.txt); do
    script_name=$(basename $script_file)
    echo "Running MG5 simulation for $script_name..."
../../../MG5_aMC_v3_4_2/bin/mg5_aMC $script_name
done
