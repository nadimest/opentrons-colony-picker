from views.mainWindow import window
import imgTools.videoHandler as videoHandler

def main():

    camera=None
    recording=False

    while True:
        state = window.readState()

        if state['exit_btn']:
            return

        elif state['record_btn']:
            camera=videoHandler.Camera()
            recording = True

        elif state['stop_btn']:
            if camera:
                camera.stop()
            recording = False
            window.updateImage(videoHandler.blankImage(100,1,0))

        if recording:
            img = camera.read()
            window.updateImage(videoHandler.encodePng(img))

main()