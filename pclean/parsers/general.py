# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

def general_parser(filename):
    '''Generic parser for portage configuration files.

    Nothing special.  Assumes that the first entry will be a CPV of some sort
    and the last whitespace separated items are the modifiers on it.  This gets
    returned as a list of tuples as outlined in ``pclean.parsers.parse``_.

    Arguments
    ---------

    :``filename``: File to be read and parsed.

    Returns
    -------

    A list of tuples (one for each line) with the following structure::
        ( 'app-portage/pclean', [ 'doc', 'test' ] )

    '''

    contents = []

    logger.info('parsing %s', filename)

    with open(filename, 'r') as file_handle:
        for line in file_handle:
            logger.debug('line: %s', line.strip())

            cpv, blob = line.strip().split(maxsplit = 1), []

            if len(cpv) > 1:
                blob = cpv[1].split()

            cpv = cpv[0]

            contents.append((cpv, blob))

            logger.debug('parsed line: %s', contents[-1])

    return contents
