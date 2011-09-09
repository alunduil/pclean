# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Alex Brandt <alunduil@alunduil.com>             
#                                                                    
# This program is free software; you can redistribute it andor modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#                                                                    
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#                                                           
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA  02111-1307, USA.

import argparse
import glob
import os

import helpers

from package import PackageFile

class PCleanApplication(object):
    def __init__(self):
        self._debug = False
        self._verbose = False
        self._quiet = False

        arguments = PCleanOptions("pclean").parsed_args

        self._quiet = arguments.quiet
        self._debug = arguments.debug

        # If we have debugging turned on we should also have verbose.
        if self._debug: 
            self._verbose = True
        else: 
            self._verbose = arguments.verbose

        # If we have verbose we shouldn't be quiet.
        if self._verbose: 
            self._quiet = False

        helpers.COLORIZE = arguments.color

        # Other option handling ...
        self._destructive = arguments.destructive
        self._reorganize = arguments.reorganize
        self._sort = arguments.sort
        self._pretend = arguments.pretend

    def run(self):
        files = glob.glob("/etc/portage/package.*")

        if self._verbose:
            helpers.debug(__file__, "Files to clean:", files = files)

        for file_ in files:
            if not os.access(file_, os.F_OK):
                helpers.error("Cant access file %s", file_)
                continue

            package_file = PackageFile(file_, self._pretend, self._debug,
                    self._verbose)
            
            if self._destructive: 
                package_file.clean(reverse = file_.endswith(".mask"),
                        clean_use = file_.endswith(".use"))

            if not file_.endswith(".mask") and self._sort: 
                package_file.sort()
            
            package_file.write(self._reorganize)

class PCleanOptions(object):
    """Options for pclean."""

    def __init__(self, name):
        self._parser = argparse.ArgumentParser(prog = name)
        self._parser = self._add_args()

    @property
    def parser(self):
        return self._parser

    @property
    def parsed_args(self):
        return self._parser.parse_args()

    def _add_args(self):
        self._parser.add_argument('--version', action = "version",
                version = "%(prog)s 0.15")

        # --verbose, -v
        help_list = [
                "Sets verbose output.",
                ]
        self._parser.add_argument('--verbose', '-v', action = 'store_true', 
                default = False, help = ''.join(help_list))

        # --debug, -D
        help_list = [
                "Sets debuggin output (implies verbose output).",
                ]
        self._parser.add_argument('--debug', '-D', action = 'store_true',
                default = False, help = ''.join(help_list))


        # --quiet, -q
        help_list = [
                "Sets ouptut to be quiter.  If either debug or verbose are ",
                "set, this option has no effect.",
                ]
        self._parser.add_argument('--quiet', '-q', action = 'store_true', 
                default = False, help = ''.join(help_list))

        # --reorganize, -r
        help_list = [
                "Reorganizes teh files into a directory structure.",
                ]
        self._parser.add_argument('--reorganize', '-r', action = 'store_true',
                default = False, help = ''.join(help_list))

        # --destructive, -d
        help_list = [
                "Removes packages that aren't installed on the system anymore.",
                ]
        self._parser.add_argument('--destructive', '-d', action = 'store_true',
                default = False, help = ''.join(help_list))

        # --sort, -s
        help_list = [
                "Sort the packages in alphabetical order.",
                ]
        self._parser.add_argument('--sort', '-s', action = 'store_true', 
                default = False, help = ''.join(help_list))

        # --pretend, -p
        help_list = [
                "Pretend but don't actually write any changes."
                ]
        self._parser.add_argument('--pretend', '-p', action = 'store_true',
                default = False, help = ''.join(help_list))

        # --color
        help_list = [
                "Enables colorized output."
                ]
        self._parser.add_argument('--color', 
                choices = [ "none", "light", "dark", "auto" ],
                default = "none", help = ''.join(help_list))

        return self._parser

