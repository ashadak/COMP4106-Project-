import numpy as np

from macros import *
from visualize import *

# class to make the map or grid layout for our agents
class World:
    def __init__(self, h, w, blocks = None, agent_points = None):
        # h and w are the height and width of the grid.
        self.h = h
        self.w = w
        # this is our grid.
        self.cells = np.zeros((h, w), dtype=int)
        # visualize is the class that will visual the objects
        self.visualize = None
        # this adds impassable objects to the grid.
        self.add_blocks(blocks)

        # dict of agents current position
        self.a_cpos = dict()
        # dict of agents goal
        self.a_goal = dict()
        # dict of time, y and x results
        self.tyx_res = dict()

    #if any xy points are out of bounds, bring them in bounds.
    def xy_fix(self, x,y):
        if(x<0): x=0
        if(x>self.w-1): x=self.w-1
        if(y<0): y=0
        if(y>self.h-1): y=self.h-1
        return(x, y)

    #check if x and y are in bounds
    def is_validpos(self, y, x):
        if x < 0 or x > self.w - 1 or y < 0 or y > self.h - 1:
            return False
        else:
            return True

    #check is cell is a block
    def is_blocked(self, y, x):
        if not self.is_validpos(y, x): return True
        if (self.cells[y][x] == IS_BLOCK): return True
        return False

    #Add a block to the grid.
    def add_blocks(self, blocks):
        if blocks:
            for block in blocks:
                blockx, blocky = self.xy_fix(block[1], block[0])
                if (not self.is_blocked(blocky, blockx)):
                    self.cells[blocky][blockx] = IS_BLOCK

    '''
    agent_points - (sy, sx, gy, gx)
        -- start and goal positions for each agent
    '''
    def add_agents(self, agent_points):
        if agent_points:
            print(agent_points)
            # Replace list of tuples with a dict lookup for better performance
            for (sy, sx, gy, gx) in agent_points:
                all_agents = len(self.a_cpos.keys())
                # if the start and goal positions are not blocks.
                if (not self.is_blocked(sy, sx) and not self.is_blocked(gy, gx)):
                    # if the start goal has weight 0. ie not an agent already
                    # we add the agent starting position to the dict of starting positions
                    # and we add the agents goal position to the dict of goal positions
                    # and we put the key value for the agent in the starting position
                    if (self.cells[sy][sx] == UNOCCUPIED):
                        self.a_cpos[all_agents + 1] = (sy, sx)
                        self.a_goal[all_agents + 1] = (gy, gx)
                        self.cells[sy][sx] = all_agents + 1
                    else:
                        raise Exception('Cell has already been occupied!')
                else:
                    raise Exception('Failure! agent index: ' + str(all_agents + 1))
                    return False
            return True
        return False


    def path_to_next_steps(self, a_index, path):
        #List of steps the agent wants to take to get to goal.
        #nexty, nextx is the agent position at a particualr point in time.
        next_steps = []
        cy, cx = self.a_cpos[a_index]
        for step in path:
            nexty, nextx = step[len(step) - 2], step[len(step) - 1]
            if (nextx - cx == 1): next_step = Next_step.RIGHT
            elif (nextx - cx == -1): next_step = Next_step.LEFT
            elif (nexty - cy == 1): next_step = Next_step.DOWN
            elif (nexty - cy == -1): next_step = Next_step.UP
            else: next_step = Next_step.WAIT
            # print('ToAction: ', cy, cx, ty, tx, tt, action)
            next_steps.append(next_step)
            cy, cx = nexty, nextx
        return next_steps

    def get_nbor_cells(self, cell_pos):
        nbor_cells = []
        #check if we're dealing with t, y, x or just y, x
        if(len(cell_pos) == 3):
            #cell_pos has time, y coordinate and x coordinate
            t, y, x = cell_pos[0], cell_pos[1], cell_pos[2]
            if (t > MAX_STEPS):
                print('cell = ', cell_pos)
                raise EnvironmentError #Error with our grid layout/problem space
            if (x > 0):
                nbor_cells.append((t+1, y, x-1))
            if(x < self.w - 1):
                nbor_cells.append((t+1, y, x+1))
            if(y > 0):
                nbor_cells.append((t+1, y-1, x))
            if(y < self.h - 1):
                nbor_cells.append((t+1, y+1, x))
            nbor_cells.append((t+1, y, x))
        elif(len(cell_pos) == 2):
            y, x = cell_pos[0], cell_pos[1]
            if(x > 0):
                nbor_cells.append((y, x-1))
            if(x < self.w - 1):
                nbor_cells.append((y, x+1))
            if(y > 0):
                nbor_cells.append((y-1, x))
            if(y < self.h - 1):
                nbor_cells.append((y+1, x))
            nbor_cells.append((y, x))
        return nbor_cells

    def check_nbors(self, y, x):
        """
        return the neighbors of a given cell
        returns an array [right, up, left, down, wait]
        """
        nbors = np.ones(5, dtype=int) * INVALID #set all neighbors to -999
        # x, y = self.xy_fix(x, y)
        if (x > 0):
            nbors[Next_step.LEFT] = self.cells[y][x - 1]
        if (x < self.w - 1):
            nbors[Next_step.RIGHT] = self.cells[y][x+1]
        if (y > 0):
            nbors[Next_step.UP] = self.cells[y-1][x]
        if (y < self.h - 1):
            nbors[Next_step.DOWN] = self.cells[y+1][x]
        nbors[Next_step.WAIT] = self.cells[y][x]
        return nbors

    def agent_next_step(self, a_index, next_step):
        #check if the agent exists
        if (a_index in self.a_cpos):
            y, x = self.a_cpos[a_index]
        else:
            raise Exception('Agent ' + str(a_index) + ' does not exist!')
        oldy, oldx = y, x
        nbors = self.check_nbors(y, x)
        #print('next step: ', a_index, y, x, nbors, next_step)
        if (nbors[next_step] == UNOCCUPIED):
            #int(True) = 1 so this code will either be 1 - 0 or 0 - 1
            y += int(next_step == Next_step.DOWN) - int(next_step == Next_step.UP)
            x += int(next_step == Next_step.RIGHT) - int(next_step == Next_step.LEFT)
            #Now change the current position of the agent
            self.a_cpos[a_index] = (y, x)
            self.cells[oldy][oldx] = UNOCCUPIED
            self.cells[y][x] = a_index
            if (self.visualize):
                self.visualize.update_agent_vis(a_index)
        elif (next_step == Next_step.WAIT):
            return -1
        else:
            raise Exception('Cell is not unoccupied! : (' + str(y) + ',' + str(x) + ') --> ' + str(next_step))
        if self.a_cpos[a_index] == self.a_goal[a_index]:
            #The agent has reached it's goal
            return 0
        return -1

    #Helper function to determine wether a cell is passable of if an agent blocks it
    def passable(self, cell, constraints):
        rn = False
        if (len(cell) == 3):
            t, y, x = cell[0], cell[1], cell[2]
            if (self.is_blocked(y,x)):
                rn = False
            elif (t > tLIMIT):
                rn = False
            elif (bool(constraints)):
                if (cell in constraints):
                    rn = False
                else:
                    rn = True
            else:
                rn = True
            return rn
        elif (len(cell) == 2):
            y, x = cell[0], cell[1]
            if (self.is_blocked(y,x)):
                rn = False
            elif (bool(constraints)):
                if (cell in constraints):
                    rn = False
                else:
                    rn = True
            else:
                rn = True
            return rn

    #This heuristic takes into account how much time it take for an agent to
    #reach it's goal. the lower time, the better, but contraints raise the time.
    def tyx_heuristic(self, a, b):
        yx_distance = abs(a[1] - b[1]) + abs(a[2] + b[2])
        if (a[0] == ANY_TIME or b[0] == ANY_TIME):
            t_distance = yx_distance/WAIT_FACTOR
        else:
            t_distance = (abs(a[2] - b[2])) * int(yx_distance > 0)
        return yx_distance + t_distance/WAIT_FACTOR

    def get_size(self):
        return (self.h, self.w)

    def get_agents(self):
        return self.a_cpos.keys()
