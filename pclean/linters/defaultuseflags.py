# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import gentoolkit.query
import gentoolkit.flag

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def default_use_flags_linter(filename, contents):
    '''Removes any USE flags that match the defaults listed on the ebuild.

    This linter removes all USE flags from the second component of the content
    that match what would be used if it wasn't specified in the content.

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

        default_use_flags = set()

        for package in packages:
            flags = gentoolkit.flag.get_iuse(package.cpv)

            default_flags = []
            for flag in flags:
                if flag.startswith('+') or flag.startswith('-'):
                    default_flags.append(flag)
                else:
                    default_flags.append('-' + flag)

            logger.debug('default use flags for %s: %s', package, default_flags)

            default_use_flags |= set(default_flags)

        logger.debug('content\'s use flags: %s', content[1])

        new_flags = []
        for flag in content[1]:
            if not (flag.startswith('+') or flag.startswith('-')):
                flag = '+' + flag

            if flag not in default_use_flags:
                new_flags.append(flag.lstrip('+'))

        logger.debug('pruned flags: %s', new_flags)

        new_contents.append((content[0], new_flags))

    return new_contents

LINTERS['default_use_flags'] = default_use_flags_linter
