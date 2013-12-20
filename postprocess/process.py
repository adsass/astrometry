#!/usr/bin/env python
# encoding: utf-8
"""
process.py

Created by August Muench on 2013-12-17.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

from __future__ import division  # confidence high
from __future__ import print_function  # i have to learn at some point

import os
import sys

import requests

from process_astrom import parse_img, parse_txt, build_hdr
from process_wwt import build_wwt_params, return_wwt_url

from astropy.table import Table

clip = 10000
adsroot = "http://labs.adsabs.harvard.edu/adsabs/abs/"
#wdir = "."
# rooturl="http://www.adsass.org/oldastro/data/"
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
    print("postprocessing: {}".format(f))
    fa = wdir + f
    r = ".".join(fa.split(".")[:-1])
    p, t = [r + "." + x for x in ('png', 'txt')]
    s = sum(map(os.path.exists, (p, t)))
    if s < 2:
        print('{0} input files are missing'.format(2 - s))
        return {}

    txt = parse_txt(t)
    img = parse_img(p)

    hdr = txt['solved'] and build_hdr(img, txt) or None
    wpr = hdr and build_wwt_params(hdr, imageurl=rooturl + f) or None

    return (hdr, wpr)

#
flist = [f for f in os.listdir(wdir) if (f[-3:] == "png")]
flist = flist[0:clip]

p = map(run, flist)

print("Building Table")
t = Table()

keys = ['REFERENC', 'ra', 'dec', 'scale', 'REF_PAGE', 'REF_FIGN']
for key in keys:
    val = get_field(p, key)
    assert len(val) == len(p)
    t[key] = val

sizes = []
for f in flist:
    fa = wdir + f
    info = os.stat(fa)
    sizes.append(info.st_size / (1024. * 1024.))
t['filesize(Mb)'] = sizes

years = []
journals = []
for hdr, wpr in p:
    if hdr is not None:
        years.append(hdr['REFERENC'][0:4])
        journals.append(hdr['REFERENC'][4:11].strip("."))
    else:
        years.append(None)
        journals.append(None)
t['Year'] = years
t['Journal'] = journals

aurl = []
iurl = []
wurl = []
for hdr, wpr in p:
    if wpr is not None:
        wurl.append(return_wwt_url(wpr, wwtroot=wwtroot))
        iurl.append(wpr['imageurl'])
        aurl.append(adsroot + hdr['REFERENC'])
    else:
        wurl.append(None)
        iurl.append(None)
        aurl.append(None)
t['ADSurl'] = aurl
t['imageurl'] = iurl
t['WWTurl'] = wurl

with open("./allfiles.xml", "w") as fo:
    t.write(fo, format="votable")
with open("./allfiles.csv", "w") as fo:
    t.write(fo, format="ascii", delimiter=",")

#t.write("test", format='ascii')
