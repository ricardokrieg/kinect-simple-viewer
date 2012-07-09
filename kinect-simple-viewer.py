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

image_generator = ImageGenerator()
image_generator.create(context)

context.start_generating_all()

pygame.init()
screen = pygame.display.set_mode((1280, 480))
depth_frame = pygame.Surface((640, 480))
pygame.display.set_caption('Kinect Simple Viewer')

running = True
histogram = numpy.zeros(MAX_DEPTH_SIZE, dtype=int)
image_count = 0
total_time = 0

print "Image dimensions ({full_res[0]}, {full_res[1]})".format(full_res=depth_generator.metadata.full_res)

def calc_histogram():
	global histogram
	max_depth = 0
	num_points = 0

	histogram.fill(0)

	depth_map = depth_generator.get_raw_depth_map()
	depth = numpy.fromstring(depth_map, dtype=numpy.uint8)
	n = len(depth)
	x = numpy.zeros(n/2)

	for index in xrange(0, n, 2):
		i = 0
		try:
			i = int("%c%c" % (depth_map[index], depth_map[index+1]))
		except: pass
		finally:
			numpy.append(x, i)
	# for

	# for index in xrange(0, length):

	# 	max_depth = min(max(max_depth, depth), MAX_DEPTH_SIZE)

	# 	if depth != 0 and depth < MAX_DEPTH_SIZE:
	# 		histogram[depth] += 1
	# 		num_points += 1
	# 	# if
	# # for

	for i in xrange(1, max_depth): histogram[i] += histogram[i-1]

	if num_points > 0:
		for i in xrange(1, max_depth):
			histogram[i] = int(256 * (1.0-(histogram[i] / float(num_points))))
	# if
# calc_histogram

def update_depth_image(surface):
	calc_histogram()

	depth_frame = numpy.empty((depth_generator.metadata.res), numpy.uint8)
	depth_frame.shape = depth_generator.metadata.res

	# for x in xrange(0, 640):
	# 	for y in xrange(0, 480):
	# 		depth = depth_generator.map[x, y]

	# 		depth_frame[x][y] = histogram[depth]
		# for
	# for

	surface.blit(pygame.surfarray.make_surface(depth_frame), (0, 0))
# update_depth_image

def capture_rgb():
	rgb_frame = numpy.fromstring(image_generator.get_raw_image_map_bgr(), dtype=numpy.uint8).reshape(480, 640, 3)
	image = cv.fromarray(rgb_frame)
	cv.CvtColor(cv.fromarray(rgb_frame), image, cv.CV_BGR2RGB)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	return pyimage
# capture_rgb

while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	screen.fill(THECOLORS['white'])
	context.wait_any_update_all()
	cv.WaitKey(10)

	start_time = pygame.time.get_ticks()

	update_depth_image(depth_frame)
	rgb_frame = capture_rgb()

	screen.blit(rgb_frame, (0, 0))
	screen.blit(depth_frame, (640, 0))

	image_count += 1
	total_time += pygame.time.get_ticks() - start_time

	pygame.display.flip()
# while

context.stop_generating_all()
sys.exit(0)