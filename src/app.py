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
            camera=videoHandler.Camera(RotateFlag=True)
            recording = True

        elif state['picture_btn']:
            if recording:
                camera.takePicture("picture.jpg")

        elif state['stop_btn']:
            if camera:
                camera.stop()
            recording = False
            window.updateImage(videoHandler.blankImage(640,480,0))

        elif state['graph_click_release']:
            point= window.getGraphPixel()
            overlap_distance=10
            if recording:
                point_overlapped= colonies.removeNearPoint(point,overlap_distance)
                if not point_overlapped:
                    colonies.add(point)

        if recording:
            img = camera.read()
            img= videoHandler.overlayCircles(img,colonies.elements)

            window.updateImage(videoHandler.encodePng(img))

main()
