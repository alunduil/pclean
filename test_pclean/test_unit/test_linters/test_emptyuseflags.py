# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.emptyuseflags import empty_use_flags_linter

class EmptyUseFlagsLinterTest(BasePCleanTest):
    def test_empty_use_flags_linter(self):
        '''linter: empty_use_flags'''

        expected = [
                ( 'app-portage/layman', [ 'git', 'subversion', 'bazaar' ] ),
                ( 'sys-kernel/upkern', [ 'module-rebuild' ] ),
                ( 'net-print/cups', [ '-usb' ] ),
                ( 'app-backup/rdiff-backup', [ '-*', 'x86' ] ),
                ]

        result = empty_use_flags_linter('/tmp/pclean.test', self.contents)

        self.assertEqual(expected, result)

    def test_empty_use_flags_linter_package_unmask(self):
        '''linter: empty_use_flags—package.unmask'''

        result = empty_use_flags_linter('/etc/portage/package.unmask', self.contents)

        self.assertEqual(self.contents, result)

    def test_empty_use_flags_linter_package_mask(self):
        '''linter: empty_use_flags—package.mask'''

        result = empty_use_flags_linter('/etc/portage/package.mask', self.contents)

        self.assertEqual(self.contents, result)
