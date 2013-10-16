# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def empty_use_flags_linter(filename, contents):
    '''Removes contents whose components are empty.

    This linter removes all contents whose second component has no members.
    This technically cleans up after other linters and removes items that have
    been made unnecessary by other actions.

    Does not act on ``package.mask`` or ``package.unmask``.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents with the items modified according to the
    aforementioned criteria.

    '''

    if re.search('package\.(?:un)?mask', filename):
        return contents

    logger.debug('linting %s', filename)

    return [ _ for _ in contents if len(contents[1]) ]

LINTERS['empty_use_flags'] = empty_use_flags_linter
