import PySimpleGUI as sg
import time
#from os.path import getsize

def time_as_int():
    return int(round(time.time() * 100))


speed = 1
start_time = time.time()
seconds = 0.05

path_start = [25, 25]
path_end = [300, 25]

layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), background_color='white', enable_events=True, key='graph')],
[sg.Text("", size=(8, 2), font=('Helvetica', 20), key='text')],
[sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]
# graph (0,0) coordinate is on the bottom left

window = sg.Window('Graph test', layout, finalize=True)

graph = window['graph']         # type: sg.Graph
circle = graph.DrawCircle((path_start[0], path_start[1]), 10, fill_color='red', line_color='black')    # ((x, y), d, inside color, outline color)
#line = graph.draw_line((path_start[0], path_start[1]), (path_end[0], path_end[1]), width = 5)       # ((x, y), (endx, endy), width)
line = None


while True:
    event, values = window.read(timeout=0)
    text_elem = window['text']

    circle_loc_x = graph.GetBoundingBox(circle)[0][0] + 11
    circle_loc_y = graph.GetBoundingBox(circle)[0][1] - 11

    # print(circle_loc_x , "-", circle_loc_y)

    current_time = time.time()
    elapsed_time = current_time - start_time

    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
    if (elapsed_time > seconds) & (circle_loc_x <= 300):
        graph.MoveFigure(circle, speed, 0)
        text_elem.update(value='%d - %d' % (circle_loc_x, circle_loc_y))
        if line is not None:
            graph.DeleteFigure(line)
        # line = graph.draw_line((path_end[0], path_end[1]), (circle_loc_x, circle_loc_y), width = 5)
        line = graph.DrawLine((circle_loc_x, circle_loc_y), (path_end[0], path_end[1]), width = 5)

        start_time = time.time()



window.close()
