#Import datetime module
from datetime import datetime

# Function to parse a single line from the log file
def parse_log_line(line):
    # Split the line into timestamp, description, and PID parts
    time_str, desc, pid_str = line.strip().split(', ')

    # Convert the timestamp string into a datetime object
    timestamp = datetime.strptime(time_str, "%H:%M:%S")

    # Extract the PID number from the PID string
    pid = pid_str.split(': ')[1]
 
    # Extract the job name and status (started/ended) from the description
    job_name, status = desc.split(' ')[0], desc.split(' ')[1]

    # Return all the parsed components
    return pid, job_name, status, timestamp

# Function to monitor logs and report job durations
def monitor_logs(filename):

    # Dictionary to store job details keyed by PID
    jobs = {}

    # Open the log file for reading
    with open(filename, 'r') as file:
        # Process each line in the file
        for line in file:
            # Parse the line to extract job details
            pid, job_name, status, timestamp = parse_log_line(line)
  
            # If this PID is not already tracked, initialize its entry
            if pid not in jobs:
                jobs[pid] = {'name': job_name}

            # Store the start or end time based on the status
            if status == "started":
               jobs[pid]['start'] = timestamp
            elif status == "ended":
               jobs[pid]['end'] = timestamp

    # Iterate over all tracked jobs
    for pid, info in jobs.items():
        # Only process jobs that have both start and end times
        if 'start' in info and 'end' in info:            
            # Calculate the duration in seconds
            duration = (info['end'] - info['start']).total_seconds()
 
            # Check if the duration exceeds the thresholds
            if duration > 600:
                print(f"ERROR: Job '{info['name']}' (PID: {pid}) took {int(duration)} seconds (over 10 minutes).")
            elif duration > 300:
                print(f"WARNING: Job '{info['name']}' (PID: {pid}) took {int(duration)} seconds (over 5 minutes).")

# Call the monitor_logs function with the log file name
monitor_logs("logs.log")
