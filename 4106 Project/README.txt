Authors:

Alex Moncion - 101089225
Selema Gebremichael - 101044173
Ashad Khan - 101046422

Requirements:

numpy and tkinter

Instructions:

pip install numpy
sudo apt-get install python3-tk
python3 multu_test.py
Use the gui to place blocks and agents

Summary:

Implementation of MAPF with a visualizer. 
Use A* to find paths for each agent without considering other agents. 
Creates a table of all paths. 
Check all paths against the table for conflicts with other agents. When a conflict is found, add a constraint to the agent's path planning and re-plan.
To avoid agents passing right through each other, agents occupy a cell for 2 ticks instead of 1. 
This sometimes causes a delay, where one or more agents may end up waiting in their current cell although a path is clearly available.

Issues:

Problems with solving certain permutations. Either the agents crash into eachother, or the algorithm loops forever.
Better conflict handling is needed.
