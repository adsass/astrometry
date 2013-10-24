#!/usr/bin/env python
# encoding: utf-8
"""
process_avm.py

Created by August Muench on 2013-09-17.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""
from __future__ import division # confidence high

import os
import sys
import math

import pyavm
import Image

from astropy import wcs
from astropy.io import fits

def parse_im(p):
    # open and extract useful information from image into a dictionary
    try:
        im = Image.open(p)
        xs,ys = im.size
        return {
            "im":im,
            "xs":xs,
            "ys":ys,
            "format":im.format
            }
    except:
        return {}

def parse_txt(t):
    # process .txt files returned by astrometry.net to extract some WCS
    # related quantities.
    #
    # Example: 2010AfrSk..14...58M-001-000.txt
    #____ 
    #testing image: 2010AfrSk..14...58M-001-000.ppm
    ##non-inverted image solved without SIMBAD coordinates in 601.016569853 seconds
    #(341.9, -46.85)
    #6.61392 x 7.83538 arcminutes
    #Field rotation angle: up is -88.0602 degrees E of N
    #----
    #
    # tiny converter
    u = {
        "arcseconds":1.,
        "arcminutes":60.,
        "degrees":3600.
        }
        #
    with open(t) as f:
        data = f.readlines()
        data = [d.strip() for d in data]
        if len(data) == 3: return {solved:False}
        bibcode = data[0][15:34]
        inverted = data[1].split(" ")[0][1:]
        inverted = inverted == 'inverted' and True or False
        ra = float(data[2].split(" ")[0][1:-1])
        dec = float(data[2].split(" ")[1][0:-1])
        xs = float(data[3].split(" ")[0][1:])
        ys = float(data[3].split(" ")[2])
        us = data[3].split(" ")[3]
        if us not in u: 
            raise  # units aren't preordained.
        else:
            xs, ys = map(lambda x:u[us]*x, (xs, ys)) 
        return {
                "solved":True,
                "ra":ra,
                "dec":dec,
                "inverted":inverted,
                "bibcode":bibcode,
                "xs":xs,
                "ys":ys,
                } 

# def map_wcs(png, txt):
    # w = wcs.WCS(naxis=2)
    # w.wcs.crpix = [-234.75, 8.3393]
    # w.wcs.cdelt = numpy.array([-0.066667, 0.066667])
    # w.wcs.crval = [0, -90]
    # w.wcs.ctype = ["RA---TAN", "DEC--TAN"] # assumed
    # w.wcs.set_pv([(2, 1, 45.0)])

def write_thumbnail(png):
    # if called use PIL to create a thumbnail
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

def write_xmp_sidecar(metadata):
    # take metadata dictionary and write xmp side car
    return {}
    
def insert_xmp(metadata, png, sidecar="foo.xmp"):
    # given a prebuilt AVM tags
    # insert into PNG.     
    return {}
    
def author_avm():
    # given metadata, write out AVM. 
    # avm = AVM()
    # avm.Spatial.CoordinateFrame = "ICRS"
    # avm.Spatial.ReferencePixel = []
    # avm.Spatial.Equinox = "J2000"
    # avm.Spatial.CDMatrix = []
    # avm.Spatial.ReferenceValue = [txt['ra'],txt['dec']]
    # avm.Spatial.ReferenceDimension = []
    # avm.Spatial.Scale = []
    # avm.Spatial.CoordsystemProjection = "TAN"
    # avm.Spatial.Quality: Full
    # avm.Spatial.Rotation: -0.22
    # 
    return {} 
    
def main():
    r = "../files2010/2010AfrSk..14...58M-001-000"
    p = r+".ppm"
    t = r+".txt"      
    img = parse_im(p)
    print img
    txt = parse_txt(t)
    print txt
    crval = [txt['ra'],txt['dec']]
    ldpix = lambda x: math.floor(x/2)
    crpix = # assume center
    ctype = ["RA---TAN", "DEC--TAN"] # assumed


if __name__ == '__main__':
    main()

