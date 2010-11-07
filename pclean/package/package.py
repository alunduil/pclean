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

import gentoolkit.query

try:
    import pycolorize
except:
    sys.path.append(os.path.dirname(__file__) + "/../vendor/pycolorize/")
    import pycolorize

class Package:
    def __init__(self, l, dry_run = False, debug = False, verbose = False):
        self._p = l.strip('\n').split()[0]
        self._use = l.strip('\n').split()[1:]
        
        self._dry_run = dry_run
        self._debug = debug
        self._verbose = verbose

        self._query = gentoolkit.query.Query(self._p)

        self._installed = True
        self._cpv = None

        if self._debug:
            pycolorize.debug(__file__,{"Installed Package Count":len(self._query.find_installed())})
            map(lambda x: pycolorize.debug(__file__,{"Installed":x.cpv}), self._query.find_installed())
        if len(self._query.find_installed()) < 1: self._installed = False
        else: self._cpv = self._query.find_installed()

    def __str__(self):
        return self.line()

    def __unicode__(self):
        return self.line()

    def line(self):
        return self._p + " " + " ".join(self._use)

    def installed(self):
        return self._installed

    def category(self):
        return self._cpv[0].category

    def atom(self):
        return self._cpv[0].name

    def clean_use(self):
        iuse = []
        map(lambda x: iuse.extend(x), map(lambda x: x.environment("IUSE").split(), self._cpv))

        if self._debug:
            map(lambda x: pycolorize.debug(__file__,{"iuse":x}), iuse)
            map(lambda x: pycolorize.debug(__file__,{"count":iuse.count(x.strip('-').strip('+'))}), self._use)
        if self._verbose:
            map(lambda x: pycolorize.status("Removing use flag, %s, from line, \"%s\"", x, self.line()), filter(lambda x: iuse.count(x.strip('-').strip('+')) < 1, self._use))
        if self._debug: 
            map(lambda x: pycolorize.debug(__file__,{"flag (before)":x}), self._use)
        self._use = filter(lambda x: iuse.count(x.strip('-').strip('+')) > 0, self._use)
        if self._debug: 
            map(lambda x: pycolorize.debug(__file__,{"flag (after)":x}), self._use)

    def empty_use(self):
        return len(self._use) < 1
        
    def shortname(self):
        return str(self._cpv.cp)
