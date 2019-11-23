#!/bin/bash

# Assume ra_cli is in current dir
DIRS=`ls -d ./rustc-perf/collector/benchmarks/*/`

for D in $DIRS
do
    echo "run analysis-stats on $D"
    ./ra_cli analysis-stats $D
done
