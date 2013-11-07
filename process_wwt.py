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
import requests

import numpy as np

from astropy import wcs 
from astropy.io import fits

from process_astrom import parse_img, parse_txt, build_wcs, document, comments

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

def write_wwt_url(hdr, imageurl="http://www.example.net", thumb=""):
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
    wurl = {}
    wurl['reverseparity'] = "True"
    wurl['scale'] = hdr['CDELT1'] * 3600. # arsec/pixel, not deg/pixel
    wurl['name'] = "test"
    wurl['imageurl'] = imageurl
    wurl['credits']="ADS+All+Sky+Survey"
    wurl['creditsUrl'] = 'http://adsass.org'
    wurl['ra'] = hdr['CRVAL1']
    wurl['y'] = hdr['CRPIX2']
    wurl['x'] = hdr['CRPIX1']
    wurl['rotation'] = hdr['CROTAX']
    wurl['dec'] = hdr['CRVAL2']
    wurl['thumb'] = thumb

    r = requests.get(wwtroot,params=wurl)
    return r

def test(tfile="astrom", tdir='test'):
    p = os.path.join(tdir, tfile+".png")
    t = os.path.join(tdir, tfile+".txt")
    o = os.path.join(tdir, tfile+".fits")
    img = parse_img(p)
    #print(img)
    txt = parse_txt(t)
    #print(txt)   
    wco = build_wcs(img, txt)
    #wco.printwcs()
    #print(wco.to_header())
    hdr = wco.to_header()
    docs = {"REFERENC":(txt['bibcode'], "ADS Bibcode"),
            "CROTAX":(txt['rt'], "CROTA2 (hidden)")}
            
    hdr = document(hdr, docs=docs)
    hdr = comments(hdr, stuff={'Original Header':txt['txt']})
    
    print(hdr['CDELT1'])
    
    wurl = write_wwt_url(hdr,
        imageurl="http://farm4.staticflickr.com/3820/10729597246_dd2f5efded_o_d.png",
        thumb="http://farm6.staticflickr.com/5514/10729613634_92ccb2593a_o_d.png")

    return wurl, hdr

def main():
    pass


if __name__ == '__main__':
    main()

