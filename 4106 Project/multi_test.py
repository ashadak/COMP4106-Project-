from world import *
from visualize import *
import multi_astar
import conflict_base_search as cbs

def get_m_astar_path(world, start, goal, constraints = None):
    ret_path = m_astar.find_path(world.get_nbor_cells,
              start,
              goal,
              lambda cell: 1,
              lambda cell, constraints : world.passable( cell, constraints ),
              world.yxt_dist_heuristic,
              constraints)
    return ret_path

#class that gives the user a prompt to enter desired row and column value
class firstSetup:

    def __init__(self):

        self.frame = Tk()
        self.frame.title("First Setup")
        self.canvas = Canvas(self.frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.pack(side=TOP)

        self.rowLabel = Label(self.canvas, text="Row:")
        self.rowInput = Entry(self.canvas)
        self.colLabel = Label(self.canvas, text="Column:")
        self.colInput = Entry(self.canvas)
        self.okButton = Button(self.canvas, text="Ok", command=self.next_setup)

        self.rowLabel.pack(side=LEFT)
        self.rowInput.pack(side=LEFT)
        self.colLabel.pack(side=LEFT)
        self.colInput.pack(side=LEFT)
        self.okButton.pack(side=BOTTOM)

    #checks if the user input values are valid
    #if not valid either it does nothing and lets the user enter a new input, or readjusts the values
    #else it calls the next window and destroys the current window
    def next_setup(self):

        try:
            rows = int(self.rowInput.get())
            cols = int(self.colInput.get())

            if rows > 10: rows = MAX_ROWS
            if rows < 1: rows = MIN_ROWS
            if cols > 10: cols = MAX_COLUMNS
            if cols < 1: cols = MIN_COLUMNS

            print("Row: " , rows , " Column: " , cols)

            s_setup = secondSetup(rows, cols, self.frame)
            self.frame.destroy()
            s_setup.frame.update()
            s_setup.frame.mainloop()

            return s_setup

        except ValueError:
            print("THE INPUT VALUES ARE NOT INTERGERS!")

#class that lets the user choose the location and number of blocks, as well as the agents' start and goal state
class secondSetup:

    def __init__(self, nrows, ncols, first_window):

        self.nrows = nrows
        self.ncols = ncols

        self.frame = Tk()
        self.frame.title("Second Setup")

        self.gridB = [[None for _ in range(ncols)] for _ in range(nrows)]
        self.blocks = []
        self.agents = []
        self.startS = []
        self.goalS = []
        self.start_or_goal = 0

        self.choosing_blocks = False
        self.choosing_agent = False

        #loop that creates and places buttons based on the users previous Row and Column input
        for row in range(nrows):
            for col in range(ncols):
                self.gridB[row][col] = Button(self.frame, text="O", bg="White", width = 4, height = 2,
                                                command=lambda i=row, j=col:self.agents_blocks(self.gridB[i][j], i, j))
                self.gridB[row][col].grid(row=row,column=col,sticky="NSEW")
                Grid.columnconfigure(self.frame,col,weight=1)

        self.blockButton = Button(self.frame, text="BLOCK", bg="White", command=lambda txt="block":self.switch_button(txt))
        self.agentButton = Button(self.frame, text="AGENT", bg="White", command=lambda txt="agent":self.switch_button(txt))
        self.clearButton = Button(self.frame, text="CLEAR AGENTS", bg="White", command=lambda  i=nrows, j=ncols:self.clear_agents(i,j))
        self.startButton = Button(self.frame, text="FINALIZE", bg="White", command=lambda window=first_window:self.finalize(window))

        self.blockButton.grid(columnspan=ncols,sticky="NSEW")
        self.agentButton.grid(columnspan=ncols,sticky="NSEW")
        self.clearButton.grid(columnspan=ncols,sticky="NSEW")
        self.startButton.grid(columnspan=ncols,sticky="NSEW")

    #method that sets the neutral buttons as a block or agent start/goal state
    def agents_blocks(self, button, i, j):

        #here is where the button is set as a block or back to a neutral state
        if self.choosing_blocks:
            if button.cget('text') == "O":
                button.configure(bg = "DarkGrey")
                button.configure(text = "X")
                self.blocks.append((i, j))

            elif button.cget('text') == "X":
                button.configure(bg = "White")
                button.configure(text = "O")
                self.blocks.remove((i, j))

        #here is where the button is set as an agent start or goal state
        if self.choosing_agent:
            if len(self.goalS) < MAX_AGENTS:
                if button.cget('text') == "O" or button.cget('text') == "X":
                    if button.cget('text') == "X": self.blocks.remove((i, j))

                    if self.start_or_goal == 0:
                        button.configure(text = "S")
                        self.startS.append((i, j))
                        button.configure(bg = COLORS[self.startS.index((i, j))])
                        self.start_or_goal = 1

                    elif self.start_or_goal == 1:
                        button.configure(text = "G")
                        self.goalS.append((i, j))
                        button.configure(bg = COLORS[self.goalS.index((i, j))])
                        self.start_or_goal = 0
            else: print("MAX NUMBER OF AGENTS REACHED!")

    #method to switch between selecting block or agent states
    def switch_button(self, bType):

        if bType == "block":
            self.choosing_blocks = True
            self.blockButton.configure(bg = "DarkGrey")
            self.choosing_agent = False
            self.agentButton.configure(bg = "White")

        if bType == "agent":
            self.choosing_agent = True
            self.agentButton.configure(bg = "DarkGrey")
            self.choosing_blocks = False
            self.blockButton.configure(bg = "White")

    #method to clear the locations or agents' start/goal states
    def clear_agents(self, i, j):
        self.startS.clear()
        self.goalS.clear()
        self.start_or_goal = 0
        for row in range(i):
            for col in range(j):
                if self.gridB[row][col].cget('text') != "X":
                    self.gridB[row][col].configure(bg = "White")
                    self.gridB[row][col].configure(text = "O")

    #method to call the search algorithm and illustate it in a new window
    def finalize(self,window):

        #pop of the agent without a goal state
        if ((len(self.startS) + len(self.goalS)) % 2) != 0:
            self.startS.pop()

        #append the start and goal states of each agents to an individual tuple
        for x in range(len(self.startS)):
            self.agents.append((self.startS[x][0], self.startS[x][1], self.goalS[x][0], self.goalS[x][1]))

        print("AGENTS = " , self.agents)
        print("BLOCKS = " , self.blocks, end='\n\n')

        a = World(self.nrows,self.ncols)

        a.add_agents(self.agents)
        a.add_blocks(self.blocks)

        #destroy 'Second Setup' window
        self.frame.destroy()

        vis = Visualize(a)

        vis.draw_world()
        vis.draw_agents()

        vis.canvas.pack()
        vis.canvas.update()
        vis.canvas.after(500)

        agents = a.get_agents()

        conflict = False

        path_maxlen = 0

        constraints = []

        path_seq = dict()

        path_seq = cbs.search(agents, a)

        action_seq = dict()

        for agent in agents:
            path_len = len(path_seq[agent])
            path_maxlen = path_len if (path_len > path_maxlen) else path_maxlen
            action_seq[agent] = a.path_to_next_steps(agent, path_seq[agent])

        for step in range(path_maxlen):
            for agent in agents:
                if( action_seq[agent] ):
                    action = action_seq[agent].pop(0)
                    a.agent_next_step(agent, action)
                    vis.canvas.update()
                    vis.canvas.after(150)
            vis.canvas.update()
            vis.canvas.after(500)

        vis.canvas.update()
        vis.canvas.after(5000,lambda: vis.frame.destroy())


f_setup = firstSetup()

f_setup.canvas.update()
f_setup.canvas.mainloop()

print(f_setup)

"""## Go around block. Wait aside for agent1 to pass
## Takes too long. Need better conflict handling
#a = World(6,10)
#a.add_blocks( [ (2,1),(1,2),(1,3),(1,4),(3,1),(2,3),(3,3),(3,4) ] )
#a.add_agents( [ (2,0,3,2), (1,1,2,2) ] )

## 2 agents. Narrow path with a open slot on the wall
## Waits too long. Need better conflict handling
#a = World(6,10)
#a.add_blocks( [ (1,0),(1,1),(1,2),(1,3),(2,4),(2,5),(1,6),(1,7),(1,8),(1,9),(0,9) ] )
#a.add_agents( [ (0,0,0,8), (0,2,0,7) ] )

## 2 agents. does work
#a = World(6,10)
#a.add_blocks( [ (4,0),(4,1),(4,2),(4,3),(4,4),(1,6),(1,7),(1,8),(1,9) ] )
#a.add_agents( [ (0,6,5,1), (5,3,0,9)] )

## 2 agents. doesn't work
#a = World(6,10)
#a.add_blocks( [ (4,0),(4,1),(4,2),(4,3),(4,4),(1,6),(1,7),(1,8),(1,9) ] )
#a.add_agents( [ (0,7,5,1), (5,3,0,9)] )

## 2 agents flipped positions. does work
#a = World(6,10)
#a.add_blocks( [ (4,0),(4,1),(4,2),(4,3),(4,4),(1,6),(1,7),(1,8),(1,9) ] )
#a.add_agents( [ (5,3,0,9), (0,7,5,1)] )

## maximum amount of agents. no blocks
#a.add_agents( [ (0,0,1,1), (1,1,2,2),(2,2,3,3),(3,3,4,4),(4,4,5,5),(3,6,3,8),(2,0,3,1)] )

## 3 agents. Single passable block. works
a = World(6,10)
#a.add_blocks( [ (4,0),(4,1),(4,2),(4,3),(2,4),(1,6),(1,7),(1,8),(1,9) ] )
#a.add_agents( [ (5,3,0,9), (0,7,5,1), (3,2,5,9) ] )

## 4 agents. Few rocks. More space to swerve around
## Need better conflict handling for an optimal path
#a = World(6,10)
a.add_blocks( [ (4,0),(4,1),(4,2),(1,7),(1,8),(1,9) ] )
a.add_agents( [ (0,7,5,1), (5,3,0,9), (0,3,5,9), (3,0,3,9) ] )


vis = Visualize(a)

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(500)

agents = a.get_agents()

conflict = False

path_maxlen = 0

constraints = []

path_seq = dict()

path_seq = cbs.search(agents, a)

action_seq = dict()

for agent in agents:
    path_len = len(path_seq[agent])
    path_maxlen = path_len if (path_len > path_maxlen) else path_maxlen
    action_seq[agent] = a.path_to_next_steps(agent, path_seq[agent])

for step in range(path_maxlen):
    for agent in agents:
        if( action_seq[agent] ):
            action = action_seq[agent].pop(0)
            a.agent_next_step(agent, action)
            vis.canvas.update()
            vis.canvas.after(150)
    vis.canvas.update()
    vis.canvas.after(500)

vis.canvas.update()
vis.canvas.after(5000)"""
