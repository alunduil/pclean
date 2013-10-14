# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import tempfile

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.parsers.general import general_parser

class GeneralParserTest(BasePCleanTest):
    def setUp(self):
        super(GeneralParserTest, self).setUp()

        logger.info('writing temporary file')

        self.tmp_file = tempfile.NamedTemporaryFile(mode = 'w')
        self.tmp_file.write('\n'.join(self.written_contents))
        self.tmp_file.seek(0)

    def test_general_parser(self):
        '''General Parser'''

        logger.debug('temporary filename: %s', self.tmp_file.name)

        result = general_parser(self.tmp_file.name)

        self.assertEqual(self.contents, result)
