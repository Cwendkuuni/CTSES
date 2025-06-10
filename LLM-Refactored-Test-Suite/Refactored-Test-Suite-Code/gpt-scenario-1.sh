#!/bin/bash

# Model and scenario configuration
MODEL="gpt"        # Options: gpt, mistral
SCENARIO="scenario1"  # Options: scenario1, scenario2, scenario3

# Setup flag directory
FLAG_DIR="iteration_flags_${MODEL}_${SCENARIO}"
mkdir -p "$FLAG_DIR"
rm -f "$FLAG_DIR"/*

# Number of total iterations
NUM_ITERATIONS=3

# List of script parts (adjust as needed)
SCRIPTS=(
    "${MODEL}-${SCENARIO}-part1.py"
    "${MODEL}-${SCENARIO}-part2.py"
    "${MODEL}-${SCENARIO}-part3.py"
)

# Function to launch all scripts in parallel
run_scripts() {
    for script in "${SCRIPTS[@]}"; do
        echo "[START] Executing $script"
        python3 "$script" &
    done
}

# Function to check completion of a given iteration
check_iteration_completion() {
    local iteration=$1
    local expected=${#SCRIPTS[@]}
    while true; do
        local count
        count=$(ls "$FLAG_DIR"/iteration_"${iteration}"_*.flag 2>/dev/null | wc -l)
        if [ "$count" -eq "$expected" ]; then
            echo "[OK] Iteration $iteration completed for ${MODEL} ${SCENARIO}"
            touch "iteration_${iteration}_completed_${MODEL}_${SCENARIO}.txt"
            break
        else
            echo "[WAIT] Iteration $iteration not yet complete (${count}/${expected})"
            sleep 30
        fi
    done
}

# Run all scripts once
run_scripts

# Monitor each iteration's completion
for ((i = 1; i <= NUM_ITERATIONS; i++)); do
    check_iteration_completion "$i"
done

# Wait for all background jobs to finish
wait

# Final completion marker
touch "all_iterations_completed_${MODEL}_${SCENARIO}.txt"
echo "[DONE] All iterations completed for ${MODEL} ${SCENARIO}"
