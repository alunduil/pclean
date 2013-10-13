# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import sys

logging.basicConfig(level = getattr(logging, os.environ.get('PCLEAN_LOGGING_LEVEL', 'warn').upper()))

logger = logging.getLogger(__name__)

from pclean.parameters import PARAMETERS
from pclean.parsers import parse

def write_file(filename, contents):
    '''Writes the specified file given the contents (name and blob).

    This houses the logic for several parameters to influence how the file is
    written.  This allows the concerns of how the user wants the files written
    to be housed once, here.

    Arguments
    ---------

    :``filename``: The path that the contents should be written to (perhaps) and
                   from which the contents originally came.
    :``contents``: The contents to be written to the desired file.  They should
                   be provided as a key (the CPV) and a blob (the items being
                   manipulated.

    Examples
    --------

    Example contents::
        [
            ( 'app-portage/pclean', [ 'doc', 'test' ] ),
            ]

    '''

    output = sys.stdout

    _ = hasattr(PARAMETERS, 'in_place')
    logger.debug('hasattr(PARAMETERS, in_place): %s', _)
    if _:
        logger.debug('PARAMETERS.in_place: %s', PARAMETERS.in_place)

    if hasattr(PARAMETERS, 'in_place'):
        output = open(filename, 'w')

        if len(PARAMETERS.in_place):
            logger.info('backup %s to %s', filename, filename + PARAMETERS.in_place)

            os.rename(filename, filename + PARAMETERS.in_place)

    logger.info('writing to %s', output)

    for line in contents:
        logger.debug('writing %s', '{0} {1}'.format(line[0], ' '.join(line[1])))

        output.write('{0} {1}'.format(line[0], ' '.join(line[1])).strip())

def main():
    '''Main function for pclean.  Does all the things.

    Performs the high level logic of this linting tool:

    #. setup logging system
    #. parse each file in turn
    #. run all desired and applicable linters on the contents
    #. write the new contents to the appropriate location

    Returns
    -------

    The number of errors that occurred during parsing or linting.

    '''

    error_count = 0

    logging.basicConfig(level = getattr(logging, PARAMETERS.log_level.upper()))

    for filename in PARAMETERS.filenames:
        logger.info('parsing %s', filename)

        contents = parse(filename)

        logger.debug('contents[0]: %s', contents[0])
        logger.debug('contents[-1]: %s', contents[-1])

        for linter in PARAMETERS.include - PARAMETERS.exclude:
            logger.info('linting %s', linter)

            contents = linter(filename, contents)

            logger.debug('contents[0]: %s', contents[0])
            logger.debug('contents[-1]: %s', contents[-1])

        logger.info('writing %s', filename)

        write_file(filename, contents)

    return error_count
