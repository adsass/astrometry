#!/usr/bin/env python
# encoding: utf-8
"""
process_avm.py

Created by August Muench on 2013-09-17.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

import sys
import os

import pyavm
import Image

def parse_im(p):
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
    #testing image: 2010AfrSk..14...58M-001-000.ppm
    ##non-inverted image solved without SIMBAD coordinates in 601.016569853 seconds
    #(341.9, -46.85)
    #6.61392 x 7.83538 arcminutes
    #Field rotation angle: up is -88.0602 degrees E of N
    u = {
        "arcseconds":1.,
        "arcminutes":60.,
        "degrees":3600.
        }
    with open(t) as f:
        data = f.readlines()
        data = [d.strip() for d in data]
        if len(data) == 3: return {solved:False}
        bibcode = data[0][15:34]
        inverted = data[1].split(" ")[0][1:]
        ra = float(data[2].split(" ")[0][1:-1])
        dec = float(data[2].split(" ")[1][0:-1])
        xs = float(data[3].split(" ")[0][1:])
        ys = float(data[3].split(" ")[2])
        us = data[3].split(" ")[3]
        if us not in u: 
            raise
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
    
def main():
    r = "../files2010/2010AfrSk..14...58M-001-000"
    p = r+".ppm"
    t = r+".txt"      
    png = parse_im(p)
    print png
    txt = parse_txt(t)
    print txt
    
    
    
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
    


if __name__ == '__main__':
    main()

