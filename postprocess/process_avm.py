#!/usr/bin/env python
# encoding: utf-8
"""
process_avm.py :: given metadata set, write XMP sidecar, insert into files

Created by August Muench on 2013-09-17.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""
from __future__ import division  # confidence high
from __future__ import print_function  # i have to learn at some point

import os
import sys
import math

import pyavm
import Image

import numpy as np

from astropy import wcs
from astropy.io import fits

s = 'process_avm.py'


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


def test_avm():
    pass


def main():
    pass

if __name__ == '__main__':
    main()
