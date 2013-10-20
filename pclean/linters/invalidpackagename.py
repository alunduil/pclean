# Copyright (C) 2013 by Alex Brandt <alunduil@alunduil.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
# TODO Change gentoolkit dependency to portage.
import gentoolkit.errors
import gentoolkit.cpv

logger = logging.getLogger(__name__)

from pclean.linters import LINTERS

def invalid_package_name_linter(filename, contents):
    '''Keeps only contents that have a valid package name.

    Uses the gentoolkit cpv module to determine if the contents' CPVs are
    valid and removes them from the list if not.

    Arguments
    ---------

    :``filename``: The file that is being linted.
    :``contents``: The contents being linted.

    Returns
    -------

    An updated set of contents with the items modified according to the
    aforementioned criteria.

    '''

    new_contents = []

    for content in contents:
        if content[0].startswith('=') and valid_cpv(content[0][1:], version = True):
            new_contents.append(content)
        elif valid_cpv(content[0]):
            new_contents.append(content)

    return new_contents

LINTERS['invalid_package_name'] = invalid_package_name_linter

def valid_cpv(cpv, version = False):
    '''Validate a CPV string.

    Takes a CPV string without a leading '=' if one is required and verifies
    that the string is valid.  If requested, the version is required on the
    passed CPV.

    Arguments
    ---------

    :``cpv``:     The CPV string being validated.
    :``version``: True if the version is required to be valid; default: False

    Returns
    -------

    True if the CPV is valid; otherwise, False.

    '''

    valid = True

    logger.debug('validating CPV %s', cpv)
    logger.debug('require version: %s', version)

    try:
        cpv = gentoolkit.cpv.CPV(cpv, validate = True)
    except gentoolkit.errors.GentoolkitInvalidCPV:
        valid = False

    if version and not len(cpv.version):
        valid = False

    logger.debug('valid: %s', valid)

    return valid
