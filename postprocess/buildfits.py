#!/usr/bin/env python
# encoding: utf-8
"""
buildfits.py

Created by August Muench on 2013-12-19.
Copyright (c) 2013 Smithsonian Astrophysical Observatory. All rights reserved.
"""

import sys
import os

from process_astrom import write_fits, run


def main():
    f = sys.argv[1]
    d = sys.argv[2]
    fa = os.path.split(f)[1]
    r = ".".join(fa.split(".")[:-1])
    o = d + '/' + r + '.fits'
    results = run(f)
    if results['hdr'] is not None:
        img = results['img']
        hdr = results['hdr']
        write_fits(img, hdr, out=o)


if __name__ == '__main__':
    main()
