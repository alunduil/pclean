# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def noop_linter(filename, contents):
    '''Does nothing to the contents passed.

    Passes through the contents completely untouched.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents.  In this case, the same contents we received.

    '''

    return contents

LINTERS['noop'] = noop_linter
