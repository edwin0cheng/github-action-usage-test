#!/bin/bash

# Assume ra_cli is in current dir
DIRS=`ls -d ./rustc-perf/collector/benchmarks/*/`

for D in $DIRS
do
    ./ra_cli analysis-stats $D
done

