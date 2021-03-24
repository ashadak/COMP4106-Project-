import sys
import PySimpleGUI as sg
import time

# Recipe for getting keys, one at a time as they are released
# If want to use the space bar, then be sure and disable the "default focus"
"""
layout = [[sg.Text("Press a key or scroll mouse")],
          [sg.Text("", size=(18, 1), key='text')],
          [sg.Button("OK", key='OK')]]

window = sg.Window("Keyboard Test", layout,
                   return_keyboard_events=True, use_default_focus=False)

# ---===--- Loop taking in user input --- #
while True:
    event, values = window.read()
    text_elem = window['text']
    if event in ("OK", None):
        print(event, "exiting")
        break
    if len(event) == 1:
        text_elem.update(value='%s - %s' % (event, ord(event)))
    if event is not None:
        text_elem.update(event)
        print(event)


window.close()
"""

# Timer
"""
def time_as_int():
    return int(round(time.time() * 100))


# ----------------  Create Form  ----------------
sg.theme('Black')

layout = [[sg.Text('')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 20),
                justification='center', key='text')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
           sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]

window = sg.Window('Running Timer', layout,
                   no_titlebar=True,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0))

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

while True:
    # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
    else:
        event, values = window.read()
    # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
    if event == '-RESET-':
        paused_time = start_time = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
        # Change button's text
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')

    # --------- Display timer in window --------
    window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))
window.close()
"""
# Demo program 1

sg.theme('DarkAmber')  # No gray windows please!

# STEP 1 define the layout
layout = [
            [sg.Text('This is a very basic PySimpleGUI layout')],
            [sg.Input()],
            [sg.Button('Button'), sg.Button('Exit')]
         ]

#STEP 2 - create the window
window = sg.Window('My new window', layout, grab_anywhere=True)

# STEP3 - the event loop
while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'Button':
      print('You pressed the button')
window.close()
