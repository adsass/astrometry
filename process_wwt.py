#!/usr/bin/env python
# encoding: utf-8
"""
process_wwt.py :: write WWT URLs based on WCS astrometry

Created by August Muench on 2013-11-04.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

from __future__ import division # confidence high
from __future__ import print_function # i have to learn at some point

import os
import sys
import math

import Image

import numpy as np

from astropy import wcs 
from astropy.io import fits

s = 'process_avm.py'        

def write_thumbnail(img, size = (128, 128)):
    # if called use PIL to create a thumbnail
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print("cannot create thumbnail for ", infile)
            
    return {}

def write_wwt_url(png, txt, file_url="http://www.example.net"):
    # the basic URL string for referencing a WWT image on the web
    # 
    # reverseparity=True
    # scale=0.761969280137
    # name=LRGB+of+NGC+6914+in+Cygnus
    # imageurl=http://farm4.staticflickr.com/3824/9785561024_a6cba97588_o.jpg
    # credits=Bob+Scott(All+Rights+Reserved)
    # creditsUrl=
    # ra=306.266834742
    # y=659
    # x=1000#
    # rotation=-150.601614164
    # dec=42.4659571643
    # thumb=http://farm4.staticflickr.com/3824/9785561024_08ebe259a2_q.jpg
    
    wwtroot = "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?"
    
    return {}


def main():
    pass


if __name__ == '__main__':
    main()

