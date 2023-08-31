#!/usr/bin/python

import sys
from ThermalPhotoPrinter import *

printer = ThermalPhotoPrinter("/dev/serial0", 9600, 18)
printer.writeBytes(27, 55, 17, 125, 40)

def printPhoto(image_file):
	printer.feedRows(50)	
	printer.printImage(image_file)
	printer.feedRows(50)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		image_file = sys.argv[1]
		print ("Image file is: ", image_file)
		printPhoto(image_file)
	else:
		print ("No image a file!")
		sys.exit(2)
