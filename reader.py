from imutils.video import VideoStream
from pyzbar import pyzbar
import cv2 as cv
import imutils
import time

# Initialization parameters
latestCode = []  # list for latest codes
running = True
logs = dict()

# Function to load stream
stream = VideoStream('213').start()
if stream.grabbed == 0:
    log={'ERROR':'Can not get stream'}
    running = False
    raise ConnectionError('No connect')
time.sleep(1)
cv.namedWindow('QR code reader', cv.WINDOW_NORMAL)


# address = VideoStream('rtsp://admin:AdminNLT!1@192.168.254.18:554/ch1-s1?tcp').start()
def detection(latestValue):
    for value in latestValue:
        latestCode.append(value)
    print(latestCode)
    while cv.waitKey(10) != 27:
        # grab a frame from a video stream
        frame = stream.read()
        if frame is None:
            logs = {'ERROR': 'Can not get frames'}
            running = False
            break
        # initialization QR-codes from frame
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            # take the coordinate of QR-code
            (x, y, w, h) = barcode.rect
            # Draw the bounding box
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # convert bytes object barcodes into utf-8
            barcodeData = barcode.data.decode("utf-8")
            # take a type detected object
            barcodeType = barcode.type

            # draw the barcodeData and barcodeType
            # text = "{} ({})".format(barcodeData, barcodeType)
            text = f'{barcodeData} ({barcodeType})'

            # put text on the bounding box
            cv.putText(frame, text, (x, y - 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
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
                print(latestCode)
                # take a picture of the code
                # img = frame[y:y + h, x:x + w]
                # take a log of the detected code
                # log = {'Detected': f'QR-code:{latestCode[-1]}'}
                break

        cv.imshow('QR code reader', frame)
    # Function to stop stream
    cv.destroyAllWindows()
    stream.stop()
    return latestCode[-1]


detection(['1234', '3324', '4321', '5678', '8809'])
