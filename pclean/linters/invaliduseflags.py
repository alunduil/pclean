# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import gentoolkit.query
import gentoolkit.flag

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def invalid_use_flags_linter(filename, contents):
    '''Keeps use flags that are still part of corresponding ebuilds.

    This linter removes all USE flags no longer in use on a CPV from
    ``package.use``.  This does not check if those use flags match default
    values only if they are present on the installed version of the package.

    This linter only applies to filenames with ``package.use`` in them.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents with the items modified according to the
    aforementioned criteria.

    '''

    logger.debug('linting %s', filename)

    if 'package.use' not in filename:
        return contents

    new_contents = []

    for content in contents:
        logger.info('retrieving info about %s', content[0])

        query = gentoolkit.query.Query(content[0])
        packages = query.find_installed()

        logger.debug('installed: %s', packages)

        use_flags = set()

        for package in packages:
            flags = gentoolkit.flag.get_iuse(package.cpv)

            logger.debug('use flags for %s: %s', package, flags)

            use_flags |= set([ gentoolkit.flag.reduce_flag(flag) for flag in flags ])

        logger.debug('content\'s use flags: %s', content[1])

        new_flags = [ flag for flag in content[1] if gentoolkit.flag.reduce_flag(flag) in use_flags ]

        logger.debug('pruned flags: %s', new_flags)

        new_contents.append((content[0], new_flags))

    return new_contents

LINTERS['invalid_use_flags'] = invalid_use_flags_linter
