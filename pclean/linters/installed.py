# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import gentoolkit.query

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def installed_linter(filename, contents):
    '''Keeps only installed packages in the returned contents.

    Uses the portage query mechanisms to find out of the package passed is
    installed on the system and removes unless it is installed.

    .. note::
        ``package.mask`` is an exception!

        When run against the ``package.mask`` file we change the logic of this
        linter to the keep existing ebuilds rather than installed.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents with items modified according to the
    aforementioned criteria.

    '''

    new_contents = []

    for content in contents:
        logger.info('retrieving info about %s', content[0])

        query = gentoolkit.query.Query(content[0])
        if 'package.mask' in filename:
            packages = [ query.find_best() ]
            logger.debug('best: %s', packages)
        else:
            packages = query.find_installed()
            logger.debug('installed: %s', packages)

        if len(packages):
            new_contents.append(content)

    return new_contents

LINTERS['installed'] = installed_linter
