#!/bin/bash

# ignore rustc-perf Cargo workspace
if test -f ./rustc-perf/Cargo.toml; then
    mv ./rustc-perf/Cargo.toml ./rustc-perf/Cargo.toml.bk
fi

# Variables

RA_CLI=./ra_cli/ra_cli
# COMMIT=$(cat ./ra_cli/commit)
# OUTPUT_FILE="output-$COMMIT.txt"
OUTPUT_FILE="ra-stats-output.txt"

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

run_stats () {
    echo $(cat ./ra_cli/commit)
    echo $(cat ./ra_cli/commit_time)

    # Assume ra_cli is in current dir
    local DIRS=`ls -d ./rustc-perf/collector/benchmarks/*/`

    for D in $DIRS
    do
        if [[ "$(is_white_listed $D)" == "True" ]]; then
            echo "run analysis-stats on $D"
            echo "====START===="
            $RA_CLI analysis-stats -q $D 2>&1
            echo "====END===="
        fi
    done
}

run_stats | tee $OUTPUT_FILE