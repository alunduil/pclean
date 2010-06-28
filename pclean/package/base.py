# -*- coding: utf-8 -*-

########################################################################
# Copyright (C) 2008 by Alex Brandt <alunduil@alunduil.com>            #
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

import output

class Base:
    def __init__(self):
        self._cpvs = {}

    def _read_file(self, file):
        """Read the file into a dictionary mapping the cpv to any flags.

        We read each line in and the first item space delimited becomes 
        a key in the dictionary.
        """

        f = open(file, 'r')
        for line in f:
            sline = line.split()
            if sline[0] in self._cpvs:
              self._cpvs[sline[0]].extend(sline[1:])
            else:
              self._cpvs[sline[0]] = sline[1:]
        file.close()
        output.debug("self._cpvs %s", self._cpvs)

    def _write_file(self):
        """Write the dictionary for this particular file.

        """

        f = open(file, 'w')

    def _write_directories(self):
        pass

    def _remove_stale_packages(self):
        pass

