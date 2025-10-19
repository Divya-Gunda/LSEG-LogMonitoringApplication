#!/bin/bash

LOG_FILE="logs.log"

# Function to convert timestamp (HH:MM:SS) to total seconds since start of the day
timestamp_to_seconds() {
  local timestamp=$1
  local hour=$(echo $timestamp | cut -d: -f1)
  local minute=$(echo $timestamp | cut -d: -f2)
  local second=$(echo $timestamp | cut -d: -f3)
  echo $((hour * 3600 + minute * 60 + second))
}

# Declare an associative array to store start times of jobs
declare -A job_start_times

# Read through each line in the log file
while IFS=, read -r timestamp description pid; do
  
  # Extract time stamp, description and action

  timestamp=$(echo $timestamp | xargs)
  action=$(echo $description | awk '{print $2}')
  job_desc=$(echo $description | awk '{print $1}')
  pid=$(echo $pid | awk '{print $NF}')

  
  if [[ $action == "started" ]]; then
    job_start_times[$pid]=$(timestamp_to_seconds "$timestamp")
  elif [[ $action == "ended" && -n ${job_start_times[$pid]} ]]; then
    start_time=${job_start_times[$pid]}
    end_time=$(timestamp_to_seconds "$timestamp")
    duration=$((end_time - start_time))
    
    # Check if the duration exceeds the thresholds
    if ((duration > 600)); then
      echo "ERROR: Job '$job_desc' (PID: $pid) took $duration seconds (over 10 minutes)"
    elif ((duration > 300)); then
      echo "WARNING: Job '$job_desc' (PID: $pid) took $duration seconds (over 5 minutes)"
    fi
    
    # Clean up the start time after processing the job
    unset job_start_times[$pid]
  fi

done < "$LOG_FILE"
