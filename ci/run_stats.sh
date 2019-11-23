#!/bin/bash

WHITE_LIST=(
    'cargo'
    'clap-rs'
    'cranelift-codegen'
    'futures'
    'helloworld'
    'html5ever' 
    'syn'
    'hyper'
)

is_white_listed () {
    for F in ${WHITE_LIST[@]}
    do
        if [[ $1 == *"$F"* ]]; then
            echo "True"
            return 0
        fi
    done
}

# Assume ra_cli is in current dir
DIRS=`ls -d ./rustc-perf/collector/benchmarks/*/`

for D in $DIRS
do
    if [[ "$(is_white_listed $D)" == "True" ]]; then
        echo "run analysis-stats on $D"
        ./ra_cli/ra_cli analysis-stats $D
    fi
done
