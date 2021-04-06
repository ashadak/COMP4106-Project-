from world import *
from visualize import *
import astar

# a = World(6,10, [(2,1),(1,2)] )
a = World(5,10)

vis = Visualize(a)

#a.add_agents([(1,1,2,2)]) #, (1,0,2,3)
#a.add_blocks([(2,1),(1,2),(1,3),(1,4),(4,1),(3,1),(2,3),(3,3),(3,4)] )

a.add_agents([(0,9,4,1),(4,1,0,9)])
a.add_blocks([(3,0),(3,1),(3,2),(3,3),(3,4),(1,6),(1,7),(1,8),(1,9)])

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(1000)

path = astar.find_path(a.get_nbor_cells,
              a.a_cpos[1],
              a.a_goal[1],
              lambda cell: 1,
              lambda cell: not a.is_blocked( cell[0], cell[1] ) )

print(path[0])
next_steps = a.path_to_next_steps(1, path[0])

print(next_steps)

for step in next_steps:
    a.agent_next_step(1, step)
    vis.canvas.update()
    vis.canvas.after(1000)

print(a.cells)
vis.canvas.after(3000)
