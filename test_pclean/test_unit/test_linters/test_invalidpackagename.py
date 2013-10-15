# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import copy

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.invalidpackagename import invalid_package_name_linter

class InvalidPackageNameLinterTest(BasePCleanTest):
    def test_invalid_package_name_linter(self):
        '''linter: invalid_package_name'''

        self.my_contents = copy.copy(self.contents)

        self.my_contents.extend([
            ( '=app-portage/layman', [ 'git', 'subversion', 'bazaar' ] ),
            ])

        result = invalid_package_name_linter('/tmp/pclean.test', self.my_contents)

        self.assertEqual(self.contents, result)
