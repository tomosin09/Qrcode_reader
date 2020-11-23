from imutils.video import VideoStream
from pyzbar import pyzbar
import cv2 as cv
import imutils
import time

# Initialization parameters
latestCode = []  # list for latest codes


# Function to load stream
stream = VideoStream('rtsp://admin:AdminNLT!1@192.168.254.18:554/ch1-s1?tcp').start()
if stream.grabbed == 0:
    running = False
    log = {'level': 'Error',
           'message': 'Can not get stream'}
    raise ConnectionError('No connect')
running = True
time.sleep(1)


# address = VideoStream('rtsp://admin:AdminNLT!1@192.168.254.18:554/ch1-s1?tcp').start()
def detection(latestValue):
    for value in latestValue:
        latestCode.append(value)
    print(latestCode)
    # Bool to exit from the loop
    retLog = False
    while cv.waitKey(10) != 27:
        # grab a frame from a video stream
        frame = stream.read()
        if frame is None:
            log = {'level': 'Error',
                   'message': 'Can not get frame'}
            running = False
            break
        # initialization QR-codes from frame
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            # take the coordinate of QR-code
            (x, y, w, h) = barcode.rect
            # convert bytes object barcodes into utf-8
            barcodeData = barcode.data.decode("utf-8")
            # take a type detected object
            # barcodeType = barcode.type
            # we need boolean function for determine
            # when to add QR-code
            haveRep = False
            # If for any code of the latestCode array there is such a code
            # that it will be equal to the detected code, then break
            for code in latestCode:
                if code == barcodeData:
                    haveRep = True
                    break
            # else the code will be added to the array
            if haveRep is False:

                # list inside the loop needs to be limited to 5 places
                if len(latestCode) >= 5:
                    del (latestCode[0])
                latestCode.append(barcodeData)
                retLog = True
                running = True
                # take a picture of the code
                img = frame[y:y + h, x:x + w]
                # take a log of the detected code
                log = {'level': 'Detected',
                       'message': f'QR-code {latestCode[-1]}'}
                break

        if retLog is True:
            break
    stream.stop()
    return img, latestCode, log, running


img, codes, log, running = detection(['1234', '3324', '4321', '5678', '8809'])
print(img, codes, log, running)
