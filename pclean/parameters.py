# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

__all__ = [
        'PARAMETERS',
        ]

import logging
import os

logger = logging.getLogger(__name__)

import argparse

from pclean import information
from pclean.linters import LINTERS

__epilog = \
        'Copyright (C) {i.COPY_YEAR} by {i.AUTHOR} licensed under a ' \
        '{i.LICENSE} license'

PARAMETERS = argparse.ArgumentParser(
        description = information.DESCRIPTION,
        epilog = __epilog.format(i = information)
        )

PARAMETERS.add_argument('--version',
        action = 'version',
        version = '%(prog)s version {i.VERSION}'.format(i = information)
        )

PARAMETERS.add_argument('-l', '--log-level',
        metavar = 'LEVEL',
        default = os.environ.get('PCLEAN_LOG_LEVEL', 'warn'),
        help = \
                'Set the verbosity of the application.  %(prog)s does not ' \
                'use a log file but utilizes the logging mechanism to ' \
                'control the output level.  Default: %(default)s'
        )

PARAMETERS.add_argument('-i', '--in-place',
        metavar = 'SUFFIX',
        help = \
                'Overwrite the specified files in place.  Similar to `sed`, ' \
                '%(prog)s can overwrite the requested files as they are ' \
                'checked.  This is not a default action and must be ' \
                'explicitly requested through this option.  If a %(metavar)s ' \
                'is specified, the original file will be backed up to the ' \
                'file with the %(metavar)s.'
        )

PARAMETERS.add_argument('-I', '--include',
        nargs = '*',
        metavar = 'LINTER',
        default = LINTERS.keys(),
        choices = LINTERS.keys(),
        help = \
                'Specify %(metavar)s that will be run against the specified ' \
                'files.  Default: %(default)s.'
        )

PARAMETERS.add_argument('-E', '--exclude',
        nargs = '*',
        metavar = 'LINTER',
        default = [ 'noop' ],
        choices = LINTERS.keys(),
        help = \
                'Specify %(metavar)s that will NOT be run against the specified ' \
                'files.  This removes items from include.  Default: %(default)s.'
        )

PARAMETERS.add_argument('filenames',
        nargs = '+',
        metavar = 'FILE',
        help = \
                'The set of files to be checked by %(prog)s.'
        )
