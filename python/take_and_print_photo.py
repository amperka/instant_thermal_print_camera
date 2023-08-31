#!/usr/bin/python

import subprocess
import RPi.GPIO as GPIO
from ThermalPhotoPrinter import *
from gpiozero import Button, LED

led_pin = 23
button_pin = 24

button = Button(button_pin, False)
led = LED(led_pin, False)

printer = ThermalPhotoPrinter("/dev/serial0", 9600, 18)
printer.writeBytes(27, 55, 17, 125, 40)


def on_pressed():
    printer.feedRows(10)


def on_held():
    print("Taking original photo")
    led.blink(0.05, 0.05)
    p = subprocess.Popen(
        ["raspistill -n -ex auto -br 52 -o /home/pi/photos/original_photo.jpg"], shell=True)
    p.wait()

    print("Converting image")
    led.blink(0.2, 0.2)
    p = subprocess.Popen(
        ["convert /home/pi/photos/original_photo.jpg -resize 512x384 -remap /home/pi/photos/ctrl_colors.gif -normalize -rotate 90 /home/pi/photos/photo_dither.png"], shell=True)
    p.wait()

    print("Remove original photo")
    p = subprocess.Popen(
        ["rm  /home/pi/photos/original_photo.jpg"], shell=True)
    p.wait()

    print("Printing image")
    led.blink(0.5, 0.5)
    printer.feedRows(50)
    printer.printImage("/home/pi/photos/photo_dither.png")
    printer.feedRows(50)

    led.on()


if __name__ == "__main__":
    led.on()

    button.when_pressed = on_pressed
    button.when_held = on_held

    while (1):
        try:
            pass
        except KeyboardInterrupt:
            button.close()
            led.close()
            break
