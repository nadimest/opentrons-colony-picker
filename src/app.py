from views.mainWindow import window
import imgTools.videoHandler as videoHandler
import calib.locations as locations

def main():

    camera=None
    recording=False
    colonies=locations.coloniesCache()

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
            window.updateImage(videoHandler.blankImage(640,480,0))

        elif state['graph_click_release']:
            point= window.getGraphPixel()
            #print(x,y)
            colonies.add(point)

        if recording:
            img = camera.read()
            img= videoHandler.overlayCircles(img,colonies.elements)

            window.updateImage(videoHandler.encodePng(img))

main()