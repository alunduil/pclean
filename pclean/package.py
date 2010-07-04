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

import os

import output

class Package:
    def __init__(self, file, check_installed = False, sort = False, debug = False):
        self._root_file = file
        self._check_installed = check_installed
        self._sort = sort
        self._debug = debug
        if self._debug: output.debug(__file__, "self._root_file -> %s", self._root_file)
        self._cpvs = {}

    def open(self):
        self._read_directories()
        if self._check_installed: self._remove_uninstalled_packages()

    def write(self, directories = False):
        if directories:
            self._write_directories()
        else:
            self._write_file(self._root_file)

    def close(self):
        pass

    def __unicode__(self):
        out = ""
        if self._sort:
            for key in sorted(self._cpvs.iterkeys()):
                out += "%s %s\n" % (key, ' '.join(self._cpvs[key]))
        else:
            for key,value in self._cpvs.items():
                out += "%s %s\n" % (key, ' '.join(value))
        return out

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
        f.close()
        if self._debug: output.debug("self._cpvs %s", self._cpvs)

    def _write_file(self, file):
        """Write the dictionary for this particular file.

        """

        if os.path.isdir(file):
            for root, dirs, files in os.walk(file, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(file)

        f = open(file, 'w')
        if self._sort:
            for key in sorted(self._cpvs.iterkeys()):
                f.write("%s %s\n" % (key, ' '.join(self._cpvs[key])))
        else:
            for key,value in self._cpvs.items():
                f.write("%s %s\n" % (key, ' '.join(value)))

    def _read_directories(self):
        if self._debug: output.debug(__file__, "os.walk(self._root_file) -> %s", os.walk(self._root_file))
        if os.path.isdir(self._root_file):
            for root, dirs, files in os.walk(self._root_file):
                if self._debug:
                    output.debug(__file__, "root -> %s", root)
                    output.debug(__file__, "dirs -> %s", dirs)
                    output.debug(__file__, "files -> %s", files)
                for file in files:
                    if self._debug: output.debug(__file__, "os.path.join(root, file) -> %s", os.path.join(root, file))
                    if os.path.isfile(os.path.join(root, file)):
                        self._read_file(os.path.join(root, file))
        else:
            self._read_file(self._root_file)

    def _write_directories(self):
        pass

    def _remove_uninstalled_packages(self):
        from gentoolkit.helpers import get_installed_cpvs
        
        for cpv in self._cpvs.keys():
            scpv = cpv.split('=')[-1].split('<')[-1].split('>')[-1]
            if self._debug: output.debug(__file__, "scpv: %s", scpv)
            pred = lambda x: x.startswith(scpv)
            if self._debug: 
                output.debug(__file__, "len(set(get_installed_cpvs(pred))): %s", len(set(get_installed_cpvs(pred))))
            if len(set(get_installed_cpvs(pred))) <= 0:
                self._cpvs.pop(cpv)

