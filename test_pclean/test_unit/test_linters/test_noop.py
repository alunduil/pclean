# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.noop import noop_linter

class NoOpLinterTest(BasePCleanTest):
    def test_noop_linter(self):
        '''linter: noop'''

        result = noop_linter('/tmp/pclean.test', self.contents)

        self.assertEqual(self.contents, result)
