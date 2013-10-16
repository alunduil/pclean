# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

from test_pclean.test_unit import BasePCleanTest

from pclean.linters.sort import sort_linter

class SortLinterTest(BasePCleanTest):
    def test_sort_linter_incorrect_filename(self):
        '''linter: sort'''

        result = sort_linter('/tmp/pclean.test', self.contents)

        sorted_contents = [
                ( '=dev-db/mysql-5.5.32', [] ),
                ( '=media-libs/harfbuzz-0.9.18-r1', [] ),
                ( 'app-backup/rdiff-backup', [ '-*', 'x86' ] ),
                ( 'app-portage/layman', [ 'git', 'subversion', 'bazaar' ] ),
                ( 'net-print/cups', [ '-usb' ] ),
                ( 'sys-kernel/upkern', [ 'module-rebuild' ] ),
                ]

        self.assertEqual(sorted_contents, result)
