from DetectQR import Detect

if __name__ == '__main__':
    latestCode = []
    detect = Detect()
    running, logData = detect.connect()
    imageView, latestCode, logData, running = Detect.detection(detect, latestCode)