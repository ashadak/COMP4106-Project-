from world import *
from visualize import *
import astar

a = World(5,10)

vis = Visualize(a)

a.add_agents( [ (1,1,2,2) ] ) #, (1,0,2,3)
a.add_blocks( [ (2,1),(1,2),(1,3),(1,4),(3,1),(4,1),(2,3),(3,3),(3,4) ] )

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(1000)

path = astar.find_path(a.get_nbor_cells,
              a.a_cpos[1],
              a.a_goal[1],
              lambda cell: not a.is_blocked( cell[0], cell[1] ) )

print(path[0])
actions = a.path_to_next_steps(1, path[0])

print(actions)

for action in actions:
    a.agent_next_step(1, action)
    vis.canvas.update()
    vis.canvas.after(1000)

print(a.cells)
vis.canvas.after(3000)
