# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.invaliduseflags import invalid_use_flags_linter

class InvalidUseFlagsLinterTest(BasePCleanTest):
    def setUp(self):
        super(InvalidUseFlagsLinterTest, self).setUp()

        self.contents = [ _ for _ in self.contents if 'rdiff-backup' not in _[0] ]

    def test_invalid_use_flags_linter_incorrect_filename(self):
        '''linter: invalid_use_flags—incorrect filename'''

        result = invalid_use_flags_linter('/tmp/pclean.test', self.contents)

        self.assertEqual(self.contents, result)

    def test_invalid_use_flags_linter_correct_filename(self):
        '''linter: invalid_use_flags—correct filename'''

        result = invalid_use_flags_linter('/etc/portage/package.use', self.contents)

        self.assertEqual(self.contents, result)
