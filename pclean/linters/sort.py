# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def sort_linter(filename, contents):
    '''Sort the contents by CPV lexicographically.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents.  Sorted by CPV lexicographically.

    '''

    return sorted(contents, key = lambda _: _[0])

LINTERS['sort'] = sort_linter
