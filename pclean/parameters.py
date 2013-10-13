# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
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
                'explicitly requested through this option.  If a %(meta)s ' \
                'is specified, the original file will be backed up to the ' \
                'file with the %(meta)s.'
        )

PARAMETERS.add_argument('-r', '--recursive',
        action = 'store_true',
        help = \
                'Create the linted output as a set of directories and  ' \
                'files (e.g. `/etc/portage/package.use/category/package). ' \
                'If this option is specified the above formatting will be ' \
                'used; otherwise, the current structure will be preserved.'
        )

PARAMETERS.add_argument('-I', '--include',
        action = 'append',
        nargs = '*',
        metavar = 'LINTERS',
        default = LINTERS,
        choices = LINTERS,
        help = \
                'Specify %(meta)s that will be run against the specified ' \
                'files.  Default: all available %(meta)s.'
        )

PARAMETERS.add_argument('-E', '--exclude',
        action = 'append',
        nargs = '*',
        metavar = 'LINTERS',
        default = [],
        choices = LINTERS,
        help = \
                'Specify %(meta)s that will NOT be run against the specified ' \
                'files.  This removes items from include.  Default: None.'
        )

PARAMETERS.add_argument('filenames',
        action = 'append',
        nargs = '*',
        default = [ os.path.join(os.path.sep, 'etc', 'portage', _) for _ in information.FILENAMES ],
        help = \
                'The set of files to be checked by %(prog)s.  Default: ' \
                '%(default)s'
        )

PARAMETERS = PARAMETERS.parse_args()
