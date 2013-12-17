#!/usr/bin/env python
# encoding: utf-8
"""
process.py

Created by August Muench on 2013-12-17.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

from __future__ import division # confidence high
from __future__ import print_function # i have to learn at some point

import os
import sys

import requests

from process_astrom import parse_img, parse_txt, build_hdr
from process_wwt import build_wwt_params, return_wwt_url

from astropy.table import Table

#wdir = "." 
#rooturl="http://www.adsass.org/oldastro/data/"
wdir, rooturl = sys.argv[1:3]
wwtroot = "http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?"

def get_field(p, key):
    val = []
    for hdr, wpr in p:
        if hdr is not None:
            if key in hdr.keys():
                val.append(hdr[key])
            elif wpr.has_key(key):
                val.append(wpr[key])
            else: 
                print('invalid key')
                return None
        else:
            val.append(None)
             
    return val
    
def run(f, wdir=wdir, rooturl=rooturl):
    f = wdir+f
    r = ".".join(f.split(".")[:-1])
    p, t = [r+"."+x for x in ('png','txt')] 
    s = sum(map(os.path.exists, (p, t)))
    if s < 2:
        print('{0} input files are missing'.format(2-s))
        return {}
        
    txt = parse_txt(t)
    img = parse_img(p)

    hdr = txt['solved'] and build_hdr(img, txt) or None
    wpr = hdr and build_wwt_params(hdr,imageurl=rooturl+f) or None
           
    return (hdr, wpr)

# 
flist = [f for f in os.listdir(wdir) if (f[-3:] == "png")]
flist = flist[0:10]

p = map(run, flist)

t = Table()

keys = ['REFERENC','ra', 'dec', 'scale',]

for key in keys:
    val = get_field(p, key)
    print(len(val))
    assert len(val) == len(p)
    t[key] = val

print(t)

# add wurls
wurl = []
for hdr,wpr in p:
    wurl.append(return_wwt_url(wpr,wwtroot = wwtroot))

# t['wurl'] = wurl

print(wurl[-1])

#t.write("test", format='ascii')
