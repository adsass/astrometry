#!/usr/bin/env python
"""Module implementing methods for SIMBAD.

Methods implemented in this module:
- makeQuery()
- getObjects()

For 'makeQuery' method:
Given a set of input parameters, the client sends a query
to the specified SIMBAD server. If the query is executed
successfully, the result will Python list of bibcodes.
If the query fails, the error message will be captured.

For 'getObjects' method:
Given a bibcode, the client returns a list of dictionaries,
one for each astronomical object associated with the bibcode.
The dictionary for each object contains parsed information,
and the raw string returned by the SIMBAD server. The dictionary
also contains the bibcode used for this query. The dictionaries have
the following format:

    {'refcode': '2009Sci...326.1675B'
      'id'    : 'V* AA Tau',
      'ra'    : '068.73092',
      'dec'   : '+24.48144',
      'otype' : 'Orion_V* ~',
      'stype' : 'M0V:e,D,~',
      'mtype' : '~,~,~',
      '_raw'  : 'V* AA Tau|068.73092|+24.48144|Orion_V* ~|M0V:e,D,~|~,~,~'
    }

where 'id' is the first (main) identifier from the list of identifiers
of the object, 'ra' and 'dec' are the decimal coordinates, 'otype' is
the default display for the main object type (in the above example, this
is "Variable Star of Orion Type". See: http://cdsweb.u-strasbg.fr/cgi-bin/Otype?X),
'stype' is the spectral type with three parameters (string, quality and
bibliographic reference) and 'mtype' is the morphological type with three
parameteres (string, quality and bibliographic reference). The '_raw' entry
contains the whole string as returned by the server

The input parameters are as follows:
A. General parameters (all optional):
- 'URL'         this parameter will change the default server
                    to be queried ('simbad.harvard.edu')
                    This parameter is set during the instantiation
                    of the client object 'Client(URL='...')'
- proxy         this parameter will set a proxy server
- startyear,endyear return bibcodes in the year publication year
                    interval defined by these values
- journals          this is a Python list of bibstems, defining the
                    journals to be returned
- debug             turning debug on will provide more verbose output
                    This parameter is set during the instantiation
                    of the client object 'Client(debug=1)'
B. For object query (to get bibcodes):
- 'object'          the name of the object (e.g. "M31", "Arcturus")
- 'radius'          radius of circle around the object to expand
                    the search. The entry needs to have a qualifier
                    appended: 'd' for degrees, or 'm' for arcminutes
                    or 's' for arcseconds. The default is 20m.
C. For coordinate query:
- 'pstring'         right ascension and declination for coordinate
                    query. Coordinates can be written in sexagesimal,
                    with spaces as field separators. A search radius can
                    be specified using a colon, and given either
                    sexigesimally or decimally. Its default value
                    is 2arcmin.
                    Examples:
                      05 23 34.6 -69 45 22:0 6
                      05 23 34.6 -69 45 22:0.166666
- 'frame'           parameter to change the default 'frame' (ICRS).
                    Valid values are: ICRS, FK4, FK5, GAL, SGAL, ECL
- 'equinox'         parameter to change the default 'equinox' (2006.7)
- 'epoch'           paramater to change the default 'epoch' (J2000)
D. For astronomical object query (for a given bibcode):
- 'bibcode'         bibcode of paper for which astronomical objects
                    are required
Examples:
    >>> from ads.SIMBAD import Client as Client
    >>> SimbadClient = Client(URL="http://simbad.u-strasbg.fr",debug=1)
    >>> SimbadClient.object    = 'M31'
    >>> SimbadClient.startyear = '1910'
    >>> SimbadClient.endyear   = '1990'
    >>> SimbadClient.journals  = ['LicOB','PASP']
    >>> SimbadClient.makeQuery()
    >>> print SimbadClient.result

"""
import re
import sys
import time

class NoQueryElementsError(Exception):
    pass

class IncorrectInputError(Exception):
    pass

class Client:
    # alternative: http://simbad.u-strasbg.fr
    def_baseURL = 'http://simbad.harvard.edu'

    def __init__(self, URL=None, proxy=None, debug=0):

        self.debug   = debug
        self.baseURL = URL or self.def_baseURL
        self.proxees = {}
        if proxy:
            self.proxees['http'] = proxy
        self.elements = []
        self.startyear= ''
        self.endyear  = ''
        self.journals = []
        self.pstring  = ''
        self.radius   = ''
        self.ra       = ''
        self.dec      = ''
        self.equinox  = ''
        self.epoch    = ''
        self.frame    = ''
        self.frames   = ['ICRS','FK4','FK5','GAL','SGAL','ECL']
        self.error    = ''
        self.__preamble = 'simbad/sim-script?submit=submit+script&script='
        self.object   = ''
        self.result   = ''
        self.script   = ''
        self.bibcode  = ''
        self.qFormats = {'bibquery':'%BIBCODELIST',
                         'objquery':'%IDLIST(1)|%COO(d;A|D)|%OTYPE|%SP(S,Q,B)|%MT(M,Q,B)'}
        self.stime    = time.time()

    def makeQuery(self,makelist=1):
        ppat = re.compile('([0-9\.\ ]+)\s+([\-\+][0-9\.\ ]+)')
        rpat = re.compile('([0-9]+)\s+([0-9]+)\s*([0-9]+)?')

        self.qType = 'bibquery'

        self.script = ''
        self.elements = []

        if len(self.elements) == 0:
            self.__setscriptheader()

        if len(self.elements) == 0:
            raise NoQueryElementsError

        if self.pstring:
            pos = re.sub('[\'\"]','',self.pstring)
            try:
                radec,rad = pos.split(':')
            except ValueError:
                rad = ''
                radec = pos
            rmat = rpat.search(rad)
            if rmat:
                try:
                    rad = "%sh%sm%ss" % (rmat.group(1),rmat.group(2),int(rmat.group(3)))
                except (IndexError, TypeError):
                    if int(rmat.group(1)) > 0:
                        rad = "%sh%sm" % (rmat.group(1),rmat.group(2))
                    else:
                        rad = "%sm" % rmat.group(2)
            pmat = ppat.search(radec)
            try:
                self.ra = pmat.group(1)
                self.dec= pmat.group(2)
            except:
                raise IncorrectInputError, "coordinate string could not be parsed"
            if rad:
                if re.search('m',rad):
                    self.radius = rad
                else:
                    self.radius = "%sd"%rad

        if self.object:
            if self.radius:
                if self.radius[-1] not in ['h','m','s','d']:
                    raise IncorrectInputError, "radius is missing qualifier!"
                self.elements.append('query ~ %s radius=%s'%
                                          (self.object,self.radius))
            else:
                self.elements.append('query id %s'%self.object)
        elif self.ra and self.dec:
            if self.dec[0] not in ['+','-']:
                raise IncorrectInputError, "DEC must start with '+' or '-'!"
            if self.radius:
                if self.radius[-1] not in ['h','m','s','d']:
                    raise IncorrectInputError, "radius is missing qualifier!"
                ra = self.ra
                dec= self.dec
                coo_query = 'query coo %s %s radius=%s'% (ra,dec,self.radius)
            else:
                ra = self.ra
                dec= self.dec
                coo_query = 'query coo %s %s'%(ra,dec)
            if self.frame and self.frame in self.frames:
                coo_query += " frame %s" % self.frame
            if self.equinox:
                coo_query += " equi=%s" % self.equinox
            if self.epoch:
                coo_query += "epoch=%s" % self.epoch
            self.elements.append(coo_query)
        else:
            self.result = ''
            raise IncorrectInputError

        self.script = "\n".join(self.elements)

        self.result = self.__doQuery()
        if re.search(':error:',self.result):
            if self.debug:
                sys.stderr.write("Returned result:\n%s\n"%self.result)
            self.error = filter(lambda a: len(a) > 0 and a!='XXX',
                             self.result.split('\n'))
            self.error = " ".join(filter(lambda a: not re.search(':::',a),
                                  self.error))
        if makelist and not self.error:
            self.result = filter(lambda a: len(a) > 0 and a!='XXX',
                                 self.result.split('\n'))

        self.duration = time.time() - self.stime

    def getObjects(self):

        self.qType = 'objquery'

        self.script = ''
        self.error  = ''
        self.elements = []
        self.objects  = []

        if len(self.elements) == 0:
            self.__setscriptheader()

        if len(self.elements) == 0:
            raise NoQueryElementsError

        self.elements.append('query bibobj %s'%self.bibcode)

        self.script = "\n".join(self.elements)

        oqres = self.__doQuery()
        if re.search(':error:',oqres):
            if self.debug:
                sys.stderr.write("Returned result:\n%s\n"%oqres)
            self.error = filter(lambda a: len(a) > 0 and a!='XXX',
                             oqres.split('\n'))
            self.error = " ".join(filter(lambda a: not re.search(':::',a),
                                  self.error))
        elif re.search('Service Unvailable',oqres):
            self.error = 'There seems to be a problem with the proxy'

        if not self.error:
            objects = filter(lambda a: len(a) > 0 and a!='XXX',
                                 oqres.split('\n'))
        else:
            objects = []

        for entry in objects:
            fields = map(lambda a: a.strip(),entry.split('|'))
            # now start creation a list of (astronomical) objects
            Object = {}
            Object['_raw'] = "|".join(fields)
            Object['refcode'] = self.bibcode
            if fields[1].strip() == 'No Coord.':
                Object['id']      = fields[0]
                Object['ra']      = fields[1]
                Object['dec']     = fields[1]
                Object['otype']   = fields[2]
                Object['mtype']   = fields[3]
            else:
                Object['id']      = fields[0]
                Object['ra']      = fields[1]
                Object['dec']     = fields[2]
                Object['otype']   = fields[3]
                Object['mtype']   = fields[4]

            self.objects.append(Object)

        self.duration = time.time() - self.stime

    def __setscriptheader(self):

        self.elements.append('output console=off error=off script=off')
        format = self.qFormats[self.qType]
        if self.startyear and self.endyear and not self.journals:
            format += "(%s-%s;1)"%(self.startyear,self.endyear)
        elif self.startyear and self.endyear and self.journals:
            format += "(%s-%s/%s;1)"%(self.startyear,self.endyear,
                                      ",".join(self.journals))
        elif self.journals:
            format += "(%s;1)"%",".join(self.journals)
        self.elements.append('format obj "%s"'%format)
        self.elements.append('echodata XXX')

    def __doQuery(self):

        import urllib
        import urllib2

        queryURL   = "%s/%s%s" % (self.baseURL,self.__preamble,
                                  urllib.quote(self.script))

        if self.debug:
            sys.stderr.write("Query URL: %s\n"%queryURL)
        try:
            b=urllib.urlopen(queryURL,proxies=self.proxees)
        except urllib2.HTTPError, e:
            sys.stderr.write("%d: %s" % (e.code,e.msg))
            return

        buffer = b.read().strip()
        return buffer

if __name__ == '__main__':

#    SimbadClient = Client(URL='http://simbad.u-strasbg.fr',debug=1)
    SimbadClient = Client()
    SimbadClient.debug = 0

#    SimbadClient.startyear = '1910'
#    SimbadClient.endyear   = '1990'
#    SimbadClient.journals  = ['PASP','AJ']
#    SimbadClient.object    = ''
#    SimbadClient.pstring = "05 23 34.6 -69 45 22:0 10"
#    SimbadClient.pstring = "05 23 34.6 -69 45 22:0.16667"
    SimbadClient.bibcode = '2009Sci...326.1675B'
    if len(sys.argv) > 1:
        SimbadClient.bibcode = sys.argv[-1]
#    SimbadClient.makeQuery()
    SimbadClient.getObjects()
    if not SimbadClient.error:
        print SimbadClient.result
    else:
        print SimbadClient.error
    print SimbadClient.objects

    print "Duration: %s seconds" % SimbadClient.duration


