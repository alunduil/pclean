# -*- coding: utf-8 -*-

########################################################################
# Copyright (C) 2010 by Alex Brandt <alunduil@alunduil.com>            #
#                                                                      #
# This program is free software; you can redistribute it and#or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program; if not, write to the                        #
# Free Software Foundation, Inc.,                                      #
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.            #
########################################################################

import os

import itertools

try:
    import pycolorize
except:
    sys.path.append(os.path.dirname(__file__) + "/../../vendor/pycolorize/")
    import pycolorize

from package import Package

class PackageFile:
    def __init__(self, f, dry_run = False, debug = False, verbose = False):
        self._f = f
        
        self._verbose = verbose
        self._debug = debug
        self._dry_run = dry_run

        if self._debug: pycolorize.debug(__file__, {"self._f":self._f})

        self._packages = self._get_packages(self._f)

    def __unicode__(self):
        return '\n'.join(self._packages)

    def _get_packages(self, f):
        return self._read_directory(f)
        
    def _read_directory(self, f):
        ret = []
        files = [f]
        if os.path.isdir(f): files = itertools.chain(*[ [ os.path.join(x[0], fs) for fs in x[2] ] for x in os.walk(f) ] )
        
        for file in files: ret.extend(self._read_file(file))

        return ret

    def _read_file(self, f):
        m = {}
        f = open(f, 'r')
        for l in f:
            l = l.split('#')[0]
            if len(l.split()) < 1: continue
            p = l.split()[0]
            u = l.split()[1:]
            if p not in m: m[p] = []
            m[p].extend(u)
        f.close()
        return [Package(k + " " + " ".join(v), self._dry_run, self._debug, self._verbose) for k,v in m.iteritems()]

    def write(self, recursive = False):
        if recursive:
            self._write_directory(self._f)
        else:
            self._write_file(self._f)

    def _write_directory(self, d):
        if not self._dry_run:
            self._create_directory(d)

            for p in self._packages:
                c = os.path.join(d, p.category())
                self._create_directory(c)
                a = os.path.join(c, p.atom())
                f = open(a, 'w')
                f.write(p.line() + "\n")
                f.close()
        else:
            pycolorize.verbose("mkdir -p %s" % d)
            for p in self._packages:
                c = os.path.join(d, p.category())
                pycolorize.verbose("mkdir -p %s" % c) 
                a = os.path.join(c, p.atom())
                pycolorize.verbose("echo %s > %s" % (p.line(), a))

    def _write_file(self, f):
        if not self._dry_run:
            self._remove_directory(f)
                
            f = open(f, 'w')
            map(lambda x: f.write(x.line() + "\n"), self._packages)
            f.close()
        else:
            pycolorize.verbose("rm -rf %s" % f)
            map(lambda x: pycolorize.verbose("echo %s >> %s" % (x.line(), f)), self._packages)

    def _create_directory(self, d):
        if not os.path.isdir(d):
            if os.path.isfile(d): os.remove(d)
            os.mkdir(d)

    def _remove_directory(self, d):
        if os.path.isdir(d):
            map(lambda x: os.rmdir(os.path.join(x[0], x[2])), os.walk(f))

    def clean(self, reverse = False, clean_use = False):
        total = set(self._packages)
        if reverse: self._packages = filter(lambda x: not x.installed(), self._packages)
        else: self._packages = filter(lambda x: x.installed(), self._packages)
        if self._verbose: map(lambda x: pycolorize.status("Removed \"%s\" since it is no longer installed.", x.line()), total - set(self._packages))
        # TODO Add invalid package removal ...
        if clean_use: 
            map(lambda x: x.clean_use(), self._packages)
            if self._verbose:
                map(lambda x: pycolorize.status("Removed \"%s\" since it has no more use flags.", x.line()), filter(lambda x: x.empty_use(), self._packages))
            self._packages = filter(lambda x: not x.empty_use(), self._packages)

    def sort(self):
        if len(self._packages) > 0: 
            self._packages = sorted(self._packages, lambda x,y: cmp(x.shortname(), y.shortname()))

