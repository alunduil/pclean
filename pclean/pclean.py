# -*- coding: utf-8 -*-

#########################################################################
# Copyright (C) 2008 by Alex Brandt <alunduil@alunduil.com>             #
#                                                                       #
# This program is free software; you can redistribute it and#or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 2 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, write to the                         #
# Free Software Foundation, Inc.,                                       #
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
#########################################################################

import sys
import optparse
import textwrap
import os

class PClean:
    def __init__(self, argv):
        self._debug = False
        self._verbose = False
        self._quiet = False

        usage = "usage: %prog [options]"
        parser = optparse.OptionParser(usage=usage)
        variables, arguments = self._parseOptions(argv, parser)

        self._quiet = variables.quiet
        self._debug = variables.debug
        # If we have debugging turned on we should also have verbose.
        if self._debug: self._verbose = True
        else: self._verbose = variables.verbose
        # If we have verbose we shouldn't be quiet.
        if self._verbose: self._quiet = False

    def Run(self):
        
        pass

    def _parseOptions(self, argv, parser):
        verbose_help_list = [
            "Sets verbose output."
            ]
        parser.add_option('--verbose', '-v', action='store_true',
            default=False, help=''.join(verbose_help_list))

        debug_help_list = [
            "Sets debugging output (implies verbose output)."
            ]
        parser.add_option('--debug', '-d', action='store_true',
            default=False, help=''.join(debug_help_list))

        quiet_help_list = [
            "Sets output to be a bit quieter.  If either debug or ",
            "verbose are set this option has no effect."
            ]
        parser.add_option('--quiet', '-q', action='store_true',
            default=False, help=''.join(quiet_help_list))

        return parser.parse_args()

class PCleanException(Exception):
    def __init__(self, message, *args):
        super(PCleanException, self).__init__(args)
        self._message = message

    def GetMessage(self):
        return self._message

