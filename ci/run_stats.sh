#!/bin/bash

# ignore rustc-perf Cargo workspace
if test -f ./rustc-perf/Cargo.toml; then
    mv ./rustc-perf/Cargo.toml ./rustc-perf/Cargo.toml.bk
fi

# Variables

RA_LSP_SERVER=./ra_lsp_server/ra_lsp_server
# COMMIT=$(cat ./ra_lsp_server/commit)
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
    echo $(cat ./ra_lsp_server/commit)
    echo $(cat ./ra_lsp_server/commit_time)

    # Assume ra_lsp_server is in current dir
    local DIRS=`ls -d ./rustc-perf/collector/benchmarks/*/`

    for D in $DIRS
    do
        if [[ "$(is_white_listed $D)" == "True" ]]; then
            echo "run analysis-stats on $D"
            echo "====START===="
            $RA_LSP_SERVER analysis-stats -q $D 2>&1
            echo "====END===="
        fi
    done
}

run_stats | tee $OUTPUT_FILE