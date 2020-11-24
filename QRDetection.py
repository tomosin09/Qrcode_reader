import os
from imutils.video import VideoStream
from pyzbar import pyzbar
import cv2 as cv
import imutils
import time


class QRDetection():

    def __init__(self, ip, port='', login='', password=''):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.stream = None
        self.connect()
        # Initialization parameters
        self.latestCode = []  # list for latest codes

    def connect(self):
        # Function to load stream
        self.stream = VideoStream(self.get_address()).start()
        if self.stream.grabbed == 0:
            self.running = False
            log = {'level': 'Error',
                   'message': 'Can not get stream'}
            raise ConnectionError('No connect')
        self.running = True
        time.sleep(1)

    def get_address(self):
        if self.login != '' or self.password != '':
            return f'rtsp://{self.login}:{self.password}@{self.ip}?tcp'
        elif self.port != '':
            return f'rtsp://{self.ip}:{self.port}?tcp'
        elif self.port == '' and self.login == '' and self.password == '':
            return f'rtsp://{self.ip}?tcp'
        else:
            return f'rtsp://{self.login}:{self.password}@{self.ip}:{self.port}?tcp'

    def check_address(self):
        ping = os.system('ping ' + f'{self.ip} > null')
        if ping == 0:
            print('Network Active')
            connection = True
        else:
            print('Network Error')
            connection = False
        return connection

    def detection(self, latestValue):
        if len(self.latestCode) == 0:
            for code in latestValue:
                self.latestCode.append(code)
        print(self.latestCode)
        # Bool to exit from the loop
        retLog = False
        cv.namedWindow('QR code reader', cv.WINDOW_NORMAL)
        while cv.waitKey(10) != 27:
            # grab a frame from a video stream
            frame = self.stream.read()
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
                for code in self.latestCode:
                    if code == barcodeData:
                        haveRep = True
                        break
                # else the code will be added to the array
                if haveRep is False:

                    # list inside the loop needs to be limited to 5 places
                    if len(self.latestCode) >= 5:
                        del (self.latestCode[0])
                    self.latestCode.append(barcodeData)
                    retLog = True
                    running = True
                    # take a picture of the code
                    img = frame[y:y + h, x:x + w]
                    # take a log of the detected code
                    log = {'level': 'Detected',
                           'message': f'QR-code {self.latestCode[-1]}'}
                    break
            cv.imshow('QR code reader', frame)
            if retLog is True:
                break
        return img, self.latestCode, log, running


vs = QRDetection('192.168.254.18', '554', 'admin', 'AdminNLT!1')
while 1:
    img, codes, log, running = vs.detection(['1234', '3324', '4321', '5678', '8809'])
    time.sleep(1)
    print(img, codes, log, running)
