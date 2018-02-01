#!/usr/bin/env python2

"""
NAME:			d-check
PURPOSE: 		check the probability of chance alignment between two small bodies (comets, asteroids or meteoroids)
USAGE:			d-check.py q1 e1 i1 Om1 w1 q2 e2 i2 Om2 w2
INPUT: 			q e i Om w	-	orbital elements of object 1 and 2, angles in deg
OUTPUT:			stdout
PREQUISTE:		NEOSSat1modelH18extraction.txt generated from S. Greenstreet's NEO Model
LICENSE:		MIT-like, see LICENSE
NOTE:			Greenstreet's model can be obtained from http://www.sarahgreenstreet.com/neo-model/

(C) Quan-Zhi Ye
"""

import numpy as np, sys, os.path

# SETTING

gsmodel = '/home/User/Release_NoIntegrations/restime/separated/extraction/NEOSSat1modelH18extraction.txt'

# FUNCTION

def dsh (q1, q2, e1, e2, i1, i2, om1, om2, w1, w2):
	d1 = (q1 - q2)**2.
	d2 = (e1 - e2)**2.
	bigi = np.arccos(np.cos(np.deg2rad(i1)) * np.cos(np.deg2rad(i2)) + np.sin(np.deg2rad(i1)) * np.sin(np.deg2rad(i2)) * np.cos(np.deg2rad(om1) - np.deg2rad(om2)))
	d3 = (2*np.sin(bigi/2.))**2.
	if abs(om1 - om2) <= 180.:
		bigpi = np.deg2rad(w1) - np.deg2rad(w2) + 2*np.arcsin(np.cos((np.deg2rad(i1)+np.deg2rad(i2))/2.) * np.sin((np.deg2rad(om1)-np.deg2rad(om2))/2.) / np.cos(bigi/2.))
	else:
		bigpi = np.deg2rad(w1) - np.deg2rad(w2) - 2*np.arcsin(np.cos((np.deg2rad(i1)+np.deg2rad(i2))/2.) * np.sin((np.deg2rad(om1)-np.deg2rad(om2))/2.) / np.cos(bigi/2.))
	d4 = ((e1+e2) * np.sin(bigpi/2.))**2.
	return np.sqrt(d1 + d2 + d3 + d4)

# MAIN

if not os.path.isfile(gsmodel):
	print "can not find NEOSSat1modelH18extraction.txt :("
	exit(1)

primary = [0, 0, 0, 0, 0]
primary[0] = float(sys.argv[1])
primary[1] = float(sys.argv[2])
primary[2] = float(sys.argv[3])
primary[3] = float(sys.argv[4])
primary[4] = float(sys.argv[5])
check = [0, 0, 0, 0, 0]
check[0] = float(sys.argv[6])
check[1] = float(sys.argv[7])
check[2] = float(sys.argv[8])
check[3] = float(sys.argv[9])
check[4] = float(sys.argv[10])
pc_dsh = dsh(primary[0], check[0], primary[1], check[1], primary[2], check[2], primary[3], check[3], primary[4], check[4])
print "primary", primary[0], primary[1], primary[2], primary[3], primary[4], "check", check[0], check[1], check[2], check[3], check[4], "in q e i Om w"
print "D_SH of the check object is", pc_dsh
c = 0
a = 0
with open(gsmodel) as f:
	for l in f:
		ll = l.split(" ")[1:]
		ll = filter(None, ll)
		ll = map(float, ll)
		dshi = dsh(primary[0], ll[0]*(1-ll[1]), primary[1], ll[1], primary[2], ll[2], primary[3], ll[3], primary[4], ll[4])
		if dshi < pc_dsh:
			c += 1
		a += 1
print "there are", c, "out of", a, "synthetic objects with D_SH smaller than the check object"
