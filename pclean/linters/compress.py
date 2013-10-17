# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def compress_linter(filename, contents):
    '''Compress duplicate CPVs into a single content.

    This isn't classic compression, it compresses the output into fewer lines
    by combining CPV's second components into a single list.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents according the afotrementioned criteria.

    '''

    new_contents = {}

    for content in contents:
        if content[0] in new_contents:
            new_contents[content[0]] += content[1]
        else:
            new_contents[content[0]] = content[1]

    return [ (k, v) for k, v in new_contents.items() ]

LINTERS['compress'] = compress_linter
