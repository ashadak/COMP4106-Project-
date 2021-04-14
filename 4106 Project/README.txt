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

The program will prompt the user with a window (First Setup) in which they can
enter the amount of rows and columns they want for the later test.

The user may enter a number between 1 and 10 for each row and column input. Once
that's done they have to press the 'Ok' button to proceed.

If the user doesn't enter an integer, they will receive a exception notice in the
terminal.

If the user enters integer values that are not between 1 and 10, the program will
automatically pass a value closest to the limit. (ei, 0 -> 1 or 32 -> 10)

The program will now prompt the user with a window (Second Setup) in which they
can setup the location and number of walls, as well as the agents' start and goal
states.

To set up walls, the user will first have to click the 'WALL' button then click on
any of the buttons with the label 'O'. The user will know they have succeeded once
the label becomes 'X' and the color turn grey. They can undo this by simply re-clicking
that button.

To set up agent start and goal states, the user will first have to click the 'AGENT'
button then click on any of the buttons with the label 'O' or 'X'. The first button
clicked will become a start state and the second a goal state. This can be repeated
to add multiple agents. The user will know they have succeeded once the label becomes
'S' or 'G', as well as the different colors for each agent. To undo this the user
will have to press the 'CLEAR AGENTS' button.

Once the user is done selecting walls and agent, they can press the 'FINALIZE' button
to start the search algorithm which will be illustrated in another window. 

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
