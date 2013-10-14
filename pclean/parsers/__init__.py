# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from pclean.parsers.general import general_parser

def parse(filename):
    '''Read and parse the given file into a list of tuples (CPV, blob).

    This function is a wrapper around the specific parsers for the various
    types of files we'll be parsing.  All of the specific parsers (only a small
    number) return the same structure.

    Arguments
    ---------

    :``filename``: File to be read and parsed.

    Returns
    -------

    A list of tuples (one for each line) with the following structure::
        ( 'app-portage/pclean', [ 'doc', 'test' ] )

    '''

    parsers = zip(information.FILENAMES, [
        general_parser,
        general_parser,
        general_parser,
        general_parser,
        general_parser,
        None, # TODO Check that the general_parser works.
        general_parser,
        None, # TODO Check that the general_parser works.
        general_parser,
        ])

    logger.debug('splitting %s', filename)

    _, base = os.path.split(filename)

    logger.info('parser selected: %s', parsers[base])

    return parsers[base](filename)
