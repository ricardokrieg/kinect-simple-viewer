#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from openni import *
import numpy
import cv
import sys
from inspect import getmembers

XML_FILE = 'config.xml'
MAX_DEPTH_SIZE = 10000

context = Context()
context.init_from_xml_file(XML_FILE)

depth_generator = DepthGenerator()
depth_generator.create(context)

context.start_generating_all()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Kinect Simple Viewer')

histogram = [0] * MAX_DEPTH_SIZE

print "Image dimensions ({full_res[0]}, {full_res[1]})".format(full_res=depth_generator.metadata.full_res)

while True:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE: sys.exit(0)
	# for

	screen.fill(THECOLORS['white'])

	context.wait_any_update_all()
	cv.WaitKey(10)

	pygame.display.flip()
# while

def capture_rgb(self):
	rgb_frame = numpy.fromstring(self.image_generator.get_raw_image_map_bgr(), dtype=numpy.uint8).reshape(480, 640, 3)
	image = cv.fromarray(rgb_frame)
	cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	return pyimage
# capture_rgb