#!/bin/bash

## catch the exit code & apply logic accordingly
function finish() {
  rv=$?
  echo "The error code received is $rv"
  if [ $rv -eq 137 ]; then
    echo "It's a manual kill, attempting another run or whatever"
  elif [ $rv -eq 0 ]; then
    echo "Exited smoothly"
  else
    echo "Non 0 & 137 exit codes"
    exit $rv
  fi
}

# Set up the trap to call 'finish' when the script exits
trap finish EXIT

# Find the process ID of bot.py
pids=$(pgrep -fi 'python3 bot.py')

if [ -n "$pids" ]; then
  echo "Killing the previous process(es)"
  kill -9 $pids
else
  echo "No previous process exists."
fi

# Start the new process
nohup python3 bot.py > bot.log 2>&1 &