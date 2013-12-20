#!/usr/bin/env python
# encoding: utf-8
"""
process_wwt.py :: write WWT URLs based on WCS astrometry

Created by August Muench on 2013-11-04.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

from __future__ import division  # confidence high
from __future__ import print_function  # i have to learn at some point

import os
import sys
import math

import Image
import requests

import numpy as np

from astropy import wcs
from astropy.io import fits

from process_astrom import parse_img, parse_txt, build_hdr, document, comments

s = 'process_wwt.py'


def write_lowres(img, hdr, scale=2):
    """
        shrink image pxiel dim and resolution by factor "scale"
    """
    # img.resize(x/scale,y/scale) # resample
    # hdr['CRPIX1']/scale # recenter
    # hdr['CDELT1'] * scale # scale resolution UP
    # hdr['NAXIS1'] => I think NAXIS# are added when the hdr is appended to
    # the img
    limg = img
    lhdr = hdr
    return (limg, lhdr, scale)


def write_thumbnail(img, size=(128, 128)):
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


def build_wwt_params(hdr, imageurl="http://www.example.net", thumb=""):
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

    wpr = {}
    wpr['reverseparity'] = "True"
    wpr['scale'] = hdr['CDELT1'] * 3600.  # arsec/pixel, not deg/pixel
    #title = hdr['REFERENC'] + " (Page: "+ hdr['REF_PAGE']+"; Image: "+hdr['REF_FIGN']+")"
    title = "{} (Page: {:d}; Image: {:d})".format(
        hdr['REFERENC'],
        int(hdr['REF_PAGE']),
        int(hdr['REF_FIGN'])
    )
    wpr['name'] = title
    wpr['imageurl'] = imageurl
    wpr['credits'] = "ADS+All+Sky+Survey"
    wpr['creditsUrl'] = 'http://adsass.org'
    wpr['ra'] = hdr['CRVAL1']
    wpr['y'] = hdr['CRPIX2']
    wpr['x'] = hdr['CRPIX1']
    wpr['rotation'] = hdr['CROTAX']
    wpr['dec'] = hdr['CRVAL2']
    wpr['thumb'] = thumb

    return wpr


def return_wwt_url(wpr,
                   wwtroot="http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?"):
    if wpr is not None:
        r = requests.get(wwtroot, params=wpr)
        return r.url
    else:
        return None


def test(tfile="astrom", tdir='/tmp/'):
    p = os.path.join(tdir, tfile + ".png")
    t = os.path.join(tdir, tfile + ".txt")
    o = os.path.join(tdir, tfile + ".fits")
    img = parse_img(p)
    txt = parse_txt(t)
    wco = build_hdr(img, txt)
    hdr = wco.to_header()
    docs = {"REFERENC": (txt['bibcode'], "ADS Bibcode"),
            "CROTAX": (txt['rt'], "CROTA2 (hidden)")}

    hdr = document(hdr, docs=docs)
    hdr = comments(hdr, stuff={'Original Header': txt['txt']})

    print(hdr['CDELT1'])

    wpr = build_wwt_params(hdr,
                           # imageurl="http://farm4.staticflickr.com/3820/10729597246_dd2f5efded_o_d.png",
                           # thumb="http://farm6.staticflickr.com/5514/10729613634_92ccb2593a_o_d.png")
                           imageurl="https://www.cfa.harvard.edu/~gmuench/astrom.png",
                           thumb="https://www.cfa.harvard.edu/~gmuench/astrom_tmb.png")
    wurl = return_wwt_url(wpr)

    return wurl, hdr


def main():
    pass


if __name__ == '__main__':
    main()
