# Основные импорты
import cv2 as cv
from imutils.video import VideoStream
from pyzbar.pyzbar import decode
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

    # Установка соединения с камерой
    # Вызывается один раз - при инициализации
    def connect(self):
        # Function to load stream
        # address = f'rtsp://{self.login}:{self.password}@{self.ip}:{self.port}?tcp'
        self.stream = VideoStream(src=0).start()
        if self.stream.grabbed == 0:
            running = False
            log = {'level': 'ERROR', 'message': 'Невозможно установить соединение с камерой!'}
        else:
            running = True
            log = {'level': 'INFO', 'message': 'Подключение с камерой установлено. Ожидание QR-кода...'}
        return running, log

    # Вызывается при ошибке в 'detection' или извне
    # Отключение соединения с камерой
    def disconnect(self):
        pass

    # Основной код, который будет постоянно вызываться
    def detection(self, latestValue):
        if len(self.latestCode) == 0:
            for code in latestValue:
                self.latestCode.append(code)
        # Bool to exit from the loop
        retLog = False
        cv.namedWindow('QR code reader', cv.WINDOW_NORMAL)
        while 1:
            # grab a frame from a video stream
            frame = self.stream.read()
            if frame is None:
                break
            # initialization QR-codes from frame
            barcodes = decode(frame)
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
                text = f'{barcodeData} ({barcodeType})'

                # put text on the bounding box
                cv.putText(frame, text, (x, y - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

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
                    y1 = int(y * 0.2)
                    y2 = int((y + h) * 0.2)
                    x1 = int(x * 0.2)
                    x2 = int((x + w) * 0.2)
                    img = frame[y - y1:y + h + y2, x - x1:x + w + x2]
                    # take a log of the detected code
                    log = {'level': 'INFO', 'message': f'Распознано: {self.latestCode[-1]}'}
                    break
            cv.waitKey(10)
            cv.imshow('QR code reader', frame)
            if retLog is True:
                break
        cv.destroyAllWindows()
        if frame is None:
            return None, None, {'level': 'ERROR', 'message': 'Потеряно соединение с камерой'}, False
        else:
            return img, self.latestCode, log, running
