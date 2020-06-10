import PySimpleGUI as sg

sg.theme('Black')

label_en={
    'record_btn':'Camera',
    'picture_btn': 'Take Picture',
    'stop_btn': 'Stop',
    'exit_btn': 'Exit',
    'jogger_y+_btn': 'Y+',
    'jogger_y-_btn': 'Y-',
    'jogger_x-_btn': 'X-',
    'jogger_x+_btn': 'X+',
    'jogger_z+_btn': 'Z+',
    'jogger_z-_btn': 'Z-',
    'graph_click_release': 'graph+UP'
}

winLabel=label_en

''' Windows layout definition using PySimpleGUI '''

camera_control = [sg.Column( [[sg.Button(winLabel['record_btn'], size=(10, 1), font='Helvetica 14'),
                             sg.Button(winLabel['picture_btn'], size=(10, 1), font='Any 14'),
                             sg.Button(winLabel['stop_btn'], size=(10, 1), font='Any 14'),
                             sg.Button(winLabel['exit_btn'], size=(10, 1), font='Helvetica 14') ]],
                            justification="right",
                            element_justification="center")
                  ]

step_radio_buttons =[sg.Radio('0.1', "STEP"),
                     sg.Radio('1', "STEP", default=True),
                     sg.Radio('10', "STEP"),
                     sg.Radio('50', "STEP")
                     ]

jogger_layout = [sg.Column([[sg.Text('Step [mm]',justification='left')],
                            step_radio_buttons,
                            [sg.Button(winLabel['jogger_y+_btn'], size=(4, 1), font='Any 12') ],
                            [sg.Button(winLabel['jogger_x-_btn'], size=(4, 1), font='Any 12'), sg.Button(winLabel['jogger_x+_btn'], size=(4, 1), font='Any 12')],
                            [sg.Button(winLabel['jogger_y-_btn'], size=(4, 1), font='Any 12')],
                            [sg.Text('')],
                            [sg.Button(winLabel['jogger_z+_btn'], size=(4, 1), font='Any 12')],
                            [sg.Button(winLabel['jogger_z-_btn'], size=(4, 1), font='Any 12')]
                            ],
                           justification='left',
                           element_justification ='center')
                 ]

image_holder= [sg.Graph( canvas_size=(1920, 1080),
                         graph_bottom_left=(0, 600),
                         graph_top_right=(800, 0),
                         key="graph",
                         change_submits=True,
                         drag_submits=True
        )]

layout = [[sg.Text('Colony Picker', size=(40, 1), justification='center', font='Helvetica 20')],
          camera_control,
          image_holder #[sg.Image(filename='', key='image')]
          ]
          #[sg.TabGroup( [sg.Tab('Jogger',tab1_layout)],[sg.Tab('Calibration',tab2_layout)])]]

''' Windows class handling loops and events to detach PySimpleGUI specific methods from the main app '''

class mainWindow():

    def __init__(self,layout):
        self.win= sg.Window('Colony Picker',
                   layout, location=(400, 200))

        self.element=winLabel

        self.state = {
            'record_btn': 0,
            'picture_btn':0,
            'stop_btn': 0,
            'exit_btn': 0,
            'graph_click_release': 0
        }

        self.clickPos = (0,0)

    def readState(self):
        event, values = self.win.read(timeout=20)

        for key in self.state:
            self.state[key]= (self.element[key] == event)

        self.handleValues(values)

        if event!="__TIMEOUT__":
            print(event,values)

        return self.state

    def handleValues(self,values):

        self.clickPos= values['graph']

    def getGraphPixel(self):
        return self.clickPos[0],self.clickPos[1]

    def updateImage(self,img=None):

        self.win.Element('graph').DrawImage(data=img,location=(0,0))

window=mainWindow(layout)


