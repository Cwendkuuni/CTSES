#!/bin/bash

# Model and scenario configuration
MODEL="mistral"
SCENARIO="scenario1"

# Setup iteration flag directory
FLAG_DIR="iteration_flags_${MODEL}_${SCENARIO}"
mkdir -p "$FLAG_DIR"
rm -f "$FLAG_DIR"/*

# Total number of iterations
NUM_ITERATIONS=3

# List of scripts to execute in parallel
SCRIPTS=(
    "${MODEL}-${SCENARIO}-part1.py"
    "${MODEL}-${SCENARIO}-part2.py"
    "${MODEL}-${SCENARIO}-part3.py"
)

# Function to run all scripts in parallel
run_scripts() {
    for script in "${SCRIPTS[@]}"; do
        echo "[START] Running $script"
        python3 "$script" &
    done
}

# Function to wait for all scripts to finish for one iteration
check_iteration_completion() {
    local iteration=$1
    local expected=${#SCRIPTS[@]}
    while true; do
        local completed
        completed=$(ls "$FLAG_DIR"/iteration_"${iteration}"_*.flag 2>/dev/null | wc -l)
        if [ "$completed" -eq "$expected" ]; then
            echo "[OK] Iteration $iteration completed for ${MODEL} ${SCENARIO}"
            touch "iteration_${iteration}_completed_${MODEL}_${SCENARIO}.txt"
            break
        else
            echo "[WAIT] Iteration $iteration not yet complete (${completed}/${expected})"
            sleep 30
        fi
    done
}

# Start all scripts
run_scripts

# Check for completion of each iteration
for ((i = 1; i <= NUM_ITERATIONS; i++)); do
    check_iteration_completion "$i"
done

# Wait for background jobs to finish
wait

# Final marker
touch "all_iterations_completed_${MODEL}_${SCENARIO}.txt"
echo "[DONE] All iterations completed for ${MODEL} ${SCENARIO}"
