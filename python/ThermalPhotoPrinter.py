import math
import time
import RPi.GPIO as GPIO

from serial import Serial
from PIL import Image


class ThermalPhotoPrinter(Serial):
    def __init__(self, serialPort, baudrate=9600, dtrPin=18):
        self.dtrPin = dtrPin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dtrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        Serial.__init__(self, serialPort, baudrate)

        self.writeBytes(27, 64)  # Reset

        printDensity = 10  # 100%
        printBreakTime = 2  # 500 uS

        self.writeBytes(29, 97, (1 << 5))  # Enable DTR

        self.writeBytes(18, 35, (printBreakTime << 5) | printDensity)

    def timeoutWait(self):
        while (GPIO.input(self.dtrPin) == GPIO.HIGH):
            pass

    def writeBytes(self, *args):
        for arg in args:
            super(ThermalPhotoPrinter, self).write(bytes([arg]))

    def feedRows(self, rows):
        self.writeBytes(27, 74, rows)

    def printBitmap(self, w, h, bitmap):
        rowBytes = (w + 7) / 8
        self.writeBytes(29, 118, 48, 0, int(rowBytes % 256), int(rowBytes / 256), int(h % 256), int(h / 256))

        i = 0
        for _ in range(h):
            for _ in range(int(rowBytes)):
                self.timeoutWait()
                super(ThermalPhotoPrinter, self).write(bytes([bitmap[i]]))
                i += 1

    def printImage(self, image_file):
        image = Image.open(image_file)
        if image.mode != '1':
            image = image.convert('1')

        width = image.size[0]
        if width > 512:
            width = 512
        height = image.size[1]
        rowBytes = math.floor((width + 7) / 8)
        bitmap = bytearray(rowBytes * height)
        pixels = image.load()

        for y in range(height):
            n = y * rowBytes
            x = 0
            for b in range(rowBytes):
                sum = 0
                bit = 128
                while bit > 0:
                    if x >= width:
                        break
                    if pixels[x, y] == 0:
                        sum |= bit
                    x += 1
                    bit >>= 1
                bitmap[n + b] = sum

        self.printBitmap(width, height, bitmap)
