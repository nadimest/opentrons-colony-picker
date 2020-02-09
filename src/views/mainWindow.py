import PySimpleGUI as sg

sg.theme('Black')

label_en={
    'record_btn':'Record',
    'stop_btn': 'Stop',
    'exit_btn': 'Exit'
}

winLabel=label_en

# define the window layout
layout = [[sg.Text('Colony Picker', size=(40, 1), justification='center', font='Helvetica 20')],
          [sg.Image(filename='', key='image')],
          [sg.Button(winLabel['record_btn'], size=(10, 1), font='Helvetica 14'),
           sg.Button(winLabel['stop_btn'], size=(10, 1), font='Any 14'),
           sg.Button(winLabel['exit_btn'], size=(10, 1), font='Helvetica 14'), ]]

# create the window and show it without the plot

class mainWindow():

    def __init__(self,layout):
        self.win= sg.Window('Colony Picker',
                   layout, location=(400, 200))

        self.element=winLabel

        self.state = {
            'record_btn': 0,
            'stop_btn': 0,
            'exit_btn': 0
        }

    def readState(self):
        event, values = self.win.read(timeout=20)

        for key in self.state:
            self.state[key]= (self.element[key] == event)


        return self.state

    def updateImage(self,img=None):

        self.win['image'].update(data=img)

window=mainWindow(layout)


