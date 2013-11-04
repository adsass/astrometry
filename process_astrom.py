#!/usr/bin/env python
# encoding: utf-8
"""
process_astrom.py :: given astrometry.net solution, convert to WCS

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

s = 'process_astrom.py'        

def id_img(p):
    """ stupid metadata extractor
    """
    try:
        im = Image.open(p)
        print(im.filename, im.format, im.size, im.mode)
    except IOError:
        pass

#def parse_fnm(f):
#    return dict(zip(("bibcode", "page", "figN"), f.split('-'))
    
def parse_img(p):
    """open and extract useful information from the image into a dictionary
    also:
        * Flatten Image to GreyScale (as it should be in this use case)
        * 
    """
    try:
        img = Image.open(p)
        xs, ys = img.size
        imgL = img.convert(mode="L")
        return {
            "im":imgL,
            "xs":xs,
            "ys":ys,
            "format":img.format
            }
    except:
        return {}

def parse_txt(t):
    """process .txt files returned by astrometry.net to extract some WCS
    related quantities.
    
    Example: 2010Ciel...72..113N, Page 2, Figure 2 (Pleiades)

        testing image: 2010Ciel...72..113N-002-002.ppm
        #non-inverted image solved without SIMBAD coordinates in 613.357455015 seconds
        (56.7, 24.15)
        81.4539 x 59.1175 arcminutes
        Field rotation angle: up is -179.411 degrees E of N

    """
    
    # tiny converter [arcseconds per unit]
    u = {
        "arcseconds":3600.,
        "arcminutes":60.,
        "degrees":1.
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

        xs = float(data[3].split(" ")[0])
        ys = float(data[3].split(" ")[2])
        us = data[3].split(" ")[3]
        if us not in u: 
            raise  # units aren't preordained.
        else:
            xs, ys = map(lambda x: x/u[us], (xs, ys))

        rt = float(data[4].split(" ")[5])

    return {
            "solved":True,
            "ra":ra,
            "dec":dec,
            "inverted":inverted,
            "bibcode":bibcode,
            "xs":xs,
            "ys":ys,
            "rt":rt,
            } 

def build_wcs(img, txt):
    """ builder of wcs from input files
    """
    # converters
    ldpix = lambda x: math.floor(x/2)
    
    w = wcs.WCS(naxis=2)
    
    # where does the NAXISn pixel number get encoded? 
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"] # assumed
    w.wcs.cunit = ['deg', 'deg'] #assumed
    
    w.wcs.crpix = [ldpix(l) for l in (img['xs'], img['ys'])] # assume center
    w.wcs.crval = [txt['ra'], txt['dec']]
    
    # the pixel scale is the angular size in degrees / pixels in X, Y
    w.wcs.cdelt = [-1.*txt['xs']/img['xs'], txt['ys']/img['ys']]

    # eventually I have to figure out the CROTAn/rotation axis. 
    # there is probably an axis flip in here too (PIL Image => FITS)
    
    return w

def write_fits(img, hdr, out="test.fits"):
    # test new header with an output fits file
    data = np.asarray(img['imgL'])
    return {}

def test(rdir='test'):
    r = "test/2010Ciel...72..113N-002-002"
    p = r+".ppm"
    t = r+".txt"      
    img = parse_img(p)
    print(img)
    txt = parse_txt(t)
    print(txt)   
    wco = build_wcs(img, txt)
    wco.printwcs()
    print(wco.to_header())
    hdr = wco.to_header()
    hdr['COMMENT'] = "Written by "+ s
    write_fits(img, hdr, out="example.fits")

def main():
	pass


if __name__ == '__main__':
	main()

