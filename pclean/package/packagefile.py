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

        if os.path.isdir(f): files = map(lambda x: os.path.join(x[0], x[2]), os.walk(f))
        for file in files: ret.extend(self._read_file(file))

        return ret

    def _read_file(self, f):
        f = open(f, 'r')
        ret = map(lambda x: Package(x, self._dry_run, self._debug, self._verbose), f.readlines())
        f.close()
        return ret

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
                f.write(p)
                f.close()
        else:
            pycolorize.verbose("mkdir -p %s" % d)
            for p in self._package:
                c = os.path.join(d, p.category())
                pycolorize.verbose("mkdir -p %s" % c) 
                a = os.path.join(c, p.atom())
                pycolorize.verbose("echo %s > %s" % (p, a))

    def _write_file(self, f):
        if not self._dry_run:
            self._remove_directory(f)
                
            f = open(f, 'w')
            map(lambda x: f.write(x), self._packages)
            f.close()
        else:
            pycolorize.verbose("rm -rf %s" % f)
            map(lambda x: pycolorize.verbose("echo %s >> %s" % (x, f)), self._packages)

    def _create_directory(self, d):
        if not os.path.isdir(d):
            if os.path.isfile(d): os.remove(d)
            os.mkdir(d)

    def _remove_directory(self, d):
        if os.path.isdir(d):
            map(lambda x: os.rmdir(os.path.join(x[0], x[2])), os.walk(f))

    def clean(self):
        filter(lambda x: x.installed(), self._packages)
        map(lambda x: x.clean_use(), self._packages)

    def sort(self):
        self._packages = sorted(self._packages, lambda x,y: cmp(x.shortname(), y.shortname()))

