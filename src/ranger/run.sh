#!/bin/bash

# This is Ranger's run script
# This simple bash script takes care of the activation of the virtual environment and firing of the python program
# All done in one step!
# Configure this script to run on startup if you want the ranger program to be activated as soon as it is powered up.

# activate the virtual environment
echo "Ranger Run: Activating virtual environment..."
source "/home/tim/rvenv/bin/activate" # replace with the path to your virtual environment's activate script

# run the python program
echo "Ranger Run: Entering Python program..."
python3 "/home/tim/ranger/src/ranger/main.py" # replace with wherever you have Ranger's "main.py" file