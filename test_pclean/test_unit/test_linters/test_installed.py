# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.installed import installed_linter

class InstalledLinterTest(BasePCleanTest):
    def test_installed_linter(self):
        '''linter: installed'''

        expected = [ _ for _ in self.contents if not re.search('harfbuzz|mysql', _[0]) ]

        result = installed_linter('/tmp/pclean.test', self.contents)

        self.assertEqual(expected, result)

    def test_installed_linter_package_mask(self):
        '''linter: installed—package.mask'''

        result = installed_linter('/etc/portage/package.mask', self.contents)

        self.assertEqual(self.contents, result)
