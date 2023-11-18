#!/bin/bash

# Change to the script directory
cd "$(dirname "$0")"

# Stage, commit, push, and pull changes
git add .
git commit -m "update"
git push
git pull

# Check if the venv folder exists or not
if [ ! -d "venv" ]; then
    echo "Creating venv folder..."
    python3 -m venv venv
    source venv/bin/activate
    # Install dependencies using pip
    pip install -r requirements.txt
fi

# Activate the virtual environment
source venv/bin/activate

# Run the main.py script
python3 main.py > outputServer.log

# Stage, commit, push, and pull changes again
git add .
git commit -m "update"
git push
git pull

# Deactivate the virtual environment
deactivate
