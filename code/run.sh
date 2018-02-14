# Run the full analysis script in parallel using gnu-parallel
NUM_STRATEGIES=221
MAX_INDEX=$(($NUM_STRATEGIES - 1))
parallel --jobs 20 "python fullAnalysis.py {1}" ::: $(seq 0 $MAX_INDEX)
