import PySimpleGUI as sg

sg.theme('Black')

label_en={
    'record_btn':'Camera',
    'stop_btn': 'Stop',
    'exit_btn': 'Exit',
    'jogger_y+_btn': 'Y+',
    'jogger_y-_btn': 'Y-',
    'jogger_x-_btn': 'X-',
    'jogger_x+_btn': 'X+',
    'jogger_z+_btn': 'Z+',
    'jogger_z-_btn': 'Z-'
}

winLabel=label_en

camera_control = [sg.Column( [[sg.Button(winLabel['record_btn'], size=(10, 1), font='Helvetica 14'),
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

layout = [[sg.Text('Colony Picker', size=(40, 1), justification='center', font='Helvetica 20')],
          camera_control,
          jogger_layout + [sg.Image(filename='', key='image')]
          ]
          #[sg.TabGroup( [sg.Tab('Jogger',tab1_layout)],[sg.Tab('Calibration',tab2_layout)])]]

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


