from macros import *
from world import *
from visualize import *
import astar
import multi_astar
import random
import math

def get_m_astar_path(world, start, goal, constraints):
    return_path = multi_astar.find_path(world.get_nbor_cells,
              start,
              goal,
              constraints,
              world.tyx_heuristic,
              lambda cell, constraints: world.passable(cell, constraints))
    return return_path

def get_astar_path(world, start, goal):
    return_path, pathcost = astar.find_path(world.get_nbor_cells, start, goal, world.passable)
    return return_path, pathcost

#Take a path with (y, x) points and converts it to (t, y, x)
def path_spacetime_conv(path_yx, start_time = 0):
    path_tyx = []
    current_time = start_time
    for step_yx in path_yx:
        step_tyx = (current_time, step_yx[0], step_yx[1])
        path_tyx.append(step_tyx)
        current_time = current_time + 1
    return (current_time - start_time), path_tyx

#Takes a single cell with (y, x) and converts it to (t, y, x)
def cell_spacetime_conv(cell, t):
    return ((t, cell[0], cell[1]))

#Returns the longest path out of all the agents
def get_max_pathlen(agents, full_path):
    max_pathlen = 0
    for agent in agents:
        pathlen = len(full_path[agent])
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen
    return max_pathlen

#Adds padding to the paths with less length than max_pathlen
def path_equalize(agents, full_path, max_pathlen = -1):
    if(max_pathlen < 0):
        max_pathlen = get_maxpathlen(agents, full_path)
    for agent in agents:
        path = full_path[agent]
        last_step = path[-1]
        for step in range(len(path), max_pathlen + TWAIT):
            path.append((step, last_step[1], last_step[2]))
        full_path[agent] = path
    return full_path

#Adds one to the timer for a given step
def tplusone(step):
    return ((step[0]+1, step[1], step[2]))

#Finds all the conflicts and stores them in the conflict database.
def get_conflicts(agents, full_path, conflicts_db = None):
    tyx_map = dict()
    if (not bool(conflicts_db)):
        conflicts_db = dict()
    #the shuffle makes it so the order of the agents doesn't matter.
    random.shuffle(list(agents))
    for agent in agents:
        if (agent not in conflicts_db):
            conflicts_db[agent] = set()
        if (full_path[agent]):
            pathlen = len(full_path[agent])
            for t, tstep in enumerate(full_path[agent]):
                #twosteps stores the current step for 2 ticks
                twosteps = [tstep]
                if (t > 0 ): twosteps.append(tplusone(full_path[agent][t]))
                for step in twosteps:
                    #if this step is not in the map, then the agent is taking
                    #the first step and is adding it to the map
                    if (step not in tyx_map):
                        tyx_map[step] = agent
                    else:
                        #if this step is already in the map, then it's occupied by another
                        #agent. So we avoid this cell by updateing the conflict database
                        otheragent = tyx_map[step]
                        if (step not in conflicts_db[agent] and agent!=otheragent):
                            conflicts_db[agent].update({step})
                            if (t > 0): conflicts_db[agent].update({tplusone(full_path[agent][t])})
    return conflicts_db


def search(agents, world):
    print("in search")
    full_path = dict()
    pathcost = dict()
    agent_goal = dict()
    max_pathlen = 0
    restart_loop = False

    #find the optimal path for each agent using a star
    for agent in agents:
        start = world.a_cpos[agent]
        goal = world.a_goal[agent]
        full_path_yx, pathcost[agent] = get_astar_path(world, start, goal)
        pathlen, full_path[agent] = path_spacetime_conv(full_path_yx)
        if pathlen > max_pathlen:
            max_pathlen = pathlen

    #Find the conflicts associated with those optimal paths.
    conflicts_db = get_conflicts(agents, full_path)

    iter_count = 1
    picked_agents = []
    while(True):
        max_pathlen = get_max_pathlen(agents, full_path)
        #Make all the paths have the same lenght.
        full_path = path_equalize(agents, full_path, max_pathlen)

        #not all agents need to change their paths. therfore, we only pick half
        #the agents that will mvoe around the other agents.
        if (iter_count % 2 == 1): #flips between 0 and 1
            picked_agents = []
            total_agents = len(agents)
            random.shuffle(list(agents))
            list_agents = list(agents)
            picked_agents = list_agents[math.floor(total_agents/2):]
        else:
            temp_picked_agents = []
            for agent in agents:
                if agent not in picked_agents:
                    temp_picked_agents.append(agent)
            picked_agents = temp_picked_agents

        #if the program is stuck, this if statement will restart the conflict_base_search
        if (restart_loop):
            restart_loop = False
            print('\n\nThe program is stuck!\nForce Restart is required!\n\n')
            something = input('Press 1 + <Enter> to continue...')
            for agent in agents:
                conflicts_db[agent] = set()
                start = world.a_cpos[agent]
                goal = world.a_goal[agent]
                full_path_yx, pathcost[agent] = get_astar_path(world, start, goal)
                pathlen, full_path[agent] = path_spacetime_conv(full_path_yx)
                max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen

        conflicts_db = get_conflicts(agents, full_path, conflicts_db)

        #Now we have to find new paths for the picked agents
        for agent in picked_agents:
            if (agent in conflicts_db):
                constraints = conflicts_db[agent]
                constraints.update({})
                if (bool(constraints)):
                    start = cell_spacetime_conv(world.a_cpos[agent], 0)
                    goal = cell_spacetime_conv(world.a_goal[agent], SOMETIME)
                    print('Agent',agent,': S',start, ' G', goal, '\n\t  C', constraints, '\n\t  OP', full_path[agent])
                    new_path, new_pathlen = get_m_astar_path(world, start, goal, constraints)
                    if (new_path):
                        full_path[agent] = new_path
                    else:
                        full_path[agent] = [start]
                        restart_loop = True
                    print('Agent',agent,': S',start, ' G', goal, '\n\t  C', constraints, '\n\t  New Path', new_path, 'Length: ', new_pathlen)

        if not restart_loop:
            full_path = path_equalize(agents, full_path, SOMETIME)
            conflicts_db = get_conflicts(agents, full_path, conflicts_db)

        break_loop = True
        #if there are still conflicts, repeat the search.
        for agent in agents:
            unbroken_conflicts = []
            constraints = conflicts_db[agent]
            for step in full_path[agent]:
                if (step in constraints):
                    unbroken_conflicts.append(step)
            if (unbroken_conflicts):
                print('## A', agent, 'UC:', unbroken_conflicts)
                print('Yes, there are conflicts!')
                break_loop = False

            goal = cell_spacetime_conv(world.a_goal[agent], SOMETIME)
            #If the goal doesn't equal the last step in multi_astar path then it
            #loops inf for many problem. This if statement fixes the off by 1 error
            if goal != full_path[agent][-1]:
                goal = goal = cell_spacetime_conv(world.a_goal[agent], SOMETIME-1)
            #if it's still not equal, then the loop will restart
            if (full_path[agent][-1] != goal):
                break_loop = False
        iter_count = iter_count + 1

        if (break_loop and not restart_loop):
            print('Loop break!')
            break

    for agent in agents:
        print('\nAgent ', agent, ' cost:',pathcost[agent], ' Path -- ', full_path[agent])

    for agent in agents:
        if agent in conflicts_db:
            print('\nAgent ', agent, ' Conflicts -- ', conflicts_db[agent])

    return full_path
