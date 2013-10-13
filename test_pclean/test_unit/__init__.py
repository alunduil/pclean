# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pclean is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import mock
import sys
import os

import logging

logger = logging.getLogger(__name__)

from pclean import write_file

class BasePCleanTest(unittest.TestCase):
    def setUp(self):
        super(BasePCleanTest, self).setUp()

        logger.debug('module: %s', self.__module__)

        _ = '.'.join([
            'pclean',
            self.__module__.replace('test_', '').replace('unit', ''),
            'PARAMETERS',
            ])

        _ = _.replace('..', '.')

        logger.info('patching %s', _)

        patcher = mock.patch(_)
        self.mock_parameters = patcher.start()
        self.addCleanup(patcher.stop)

class WriteFileTest(BasePCleanTest):
    def setUp(self):
        super(WriteFileTest, self).setUp()

        logger.info('patching builtins.open')

        patcher = mock.patch('builtins.open', mock.mock_open())
        self.mock_open = patcher.start()
        self.addCleanup(patcher.stop)

        logger.debug('mock_open(): %s', self.mock_open.return_value)

        _ = sys.stdout

        def cleanup():
            sys.stdout = _

        self.addCleanup(cleanup)
        sys.stdout = self.mock_open.return_value

        self.contents = [
                ( 'app-portage/layman', [ 'git', 'subversion', 'bazaar' ] ),
                ( 'sys-kernel/upkern', [ 'module-rebuild' ] ),
                ( 'net-print/cups', [ '-usb' ] ),
                ( '=media-libs/harfbuzz-0.9.18-r1', [] ),
                ( '=dev-db/mysql-5.5.32', [] ),
                ( 'app-backup/rdiff-backup', [ '-*', 'x86' ] ),
                ]

        self.written_contents = [
                'app-portage/layman git subversion bazaar',
                'sys-kernel/upkern module-rebuild',
                'net-print/cups -usb',
                '=media-libs/harfbuzz-0.9.18-r1',
                '=dev-db/mysql-5.5.32',
                'app-backup/rdiff-backup -* x86',
                ]

    def test_write_options_none(self):
        '''write contents with options: none'''

        del self.mock_parameters.in_place

        write_file('/tmp/pclean.test', self.contents)

        self.mock_open.assert_has_calls([ mock.call().write(_) for _ in self.written_contents ])

    def test_write_options_inplace0(self):
        '''write contents with options: in_place[0]'''

        self.mock_parameters.in_place = ''

        write_file('/tmp/pclean.test', self.contents)

        self.mock_open.assert_called_once_with('/tmp/pclean.test', 'w')

        self.mock_open.assert_has_calls([ mock.call().write(_) for _ in self.written_contents ])

    def test_write_options_inplace1(self):
        '''write contents with options: in_place[1]'''

        self.mock_parameters.in_place = '.bak'

        with mock.patch('pclean.os.rename') as mock_rename:
            write_file('/tmp/pclean.test', self.contents)

            mock_rename.assert_called_once_with('/tmp/pclean.test', '/tmp/pclean.test.bak')

        self.mock_open.assert_called_once_with('/tmp/pclean.test', 'w')

        self.mock_open.assert_has_calls([ mock.call().write(_) for _ in self.written_contents ])
