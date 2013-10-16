# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.defaultuseflags import default_use_flags_linter

class DefaultUseFlagsLinterTest(BasePCleanTest):
    def setUp(self):
        super(DefaultUseFlagsLinterTest, self).setUp()

        self.contents = [ _ for _ in self.contents if 'rdiff-backup' not in _[0] ]

    def test_default_use_flags_linter(self):
        '''linter: default_use_flags'''

        result = default_use_flags_linter('/tmp/pclean.test', self.contents)

        self.assertEqual(self.contents, result)

    def test_default_use_flags_linter_package_use(self):
        '''linter: default_use_flags—package.use'''

        expected = [
                ( 'app-portage/layman', [ 'subversion', 'bazaar' ] ),
                ( 'sys-kernel/upkern', [ 'module-rebuild' ] ),
                ( 'net-print/cups', [] ),
                ( '=media-libs/harfbuzz-0.9.18-r1', [] ),
                ( '=dev-db/mysql-5.5.32', [] ),
                ]

        result = default_use_flags_linter('/etc/portage/package.use', self.contents)

        self.assertEqual(expected, result)
