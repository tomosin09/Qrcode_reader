# Основные импорты
import os
import cv2 as cv
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
from Config import ConfigGetter



# Основной класс по распознаванию QR-кода
class Detect:

    def __init__(self):
        super().__init__()
        cfg = ConfigGetter()
        self.latestCode = []
        self.ip = cfg.cameraIp
        self.login = cfg.cameraLogin
        self.password = cfg.cameraPassword
        self.port = cfg.cameraArguments
        self.connect()

    # Установка соединения с камерой
    # Вызывается один раз - при инициализации
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

    # Вызывается при ошибке в 'detection' или извне
    # Отключение соединения с камерой
    def disconnect(self):
        # !Код Андрея
        pass

    # Основной код, который будет постоянно вызываться
    def detection(self, latestValue):
        for value in latestValue:
            self.latestCode.append(value)
        print(self.latestCode)
        # Bool to exit from the loop
        retLog = False
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

            if retLog is True:
                break
        self.stream.stop()
        return img, self.latestCode, log, running