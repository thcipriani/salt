# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Jayesh Kariya <jayeshk@saltstack.com>`
'''
# Import Python libs
from __future__ import absolute_import

# Import Salt Testing Libs
from salttesting import skipIf, TestCase
from salttesting.mock import (
    NO_MOCK,
    NO_MOCK_REASON,
    MagicMock,
    patch)

from salttesting.helpers import ensure_in_syspath

ensure_in_syspath('../../')

# Import Salt Libs
from salt.modules import rh_ip
import jinja2.exceptions
import os

# Globals
rh_ip.__grains__ = {}
rh_ip.__salt__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class RhipTestCase(TestCase):
    '''
    Test cases for salt.modules.rh_ip
    '''
    def test_build_bond(self):
        '''
        Test to create a bond script in /etc/modprobe.d with the passed
        settings and load the bonding kernel module.
        '''
        with patch.dict(rh_ip.__grains__, {'osrelease': 'osrelease'}):
            with patch.object(rh_ip, '_parse_settings_bond', MagicMock()):
                mock = jinja2.exceptions.TemplateNotFound('foo')
                with patch.object(jinja2.Environment, 'get_template',
                                  MagicMock(side_effect=mock)):
                    self.assertEqual(rh_ip.build_bond('iface'), '')

                with patch.dict(rh_ip.__salt__, {'kmod.load':
                                                 MagicMock(return_value=None)}):
                    with patch.object(rh_ip, '_write_file_iface',
                                      return_value=None):
                        with patch.object(rh_ip, '_read_temp', return_value='A'):
                            self.assertEqual(rh_ip.build_bond('iface', test='A'),
                                             'A')

                        with patch.object(rh_ip, '_read_file', return_value='A'):
                            self.assertEqual(rh_ip.build_bond('iface', test=None),
                                             'A')

    def test_build_interface(self):
        '''
        Test to build an interface script for a network interface.
        '''
        with patch.dict(rh_ip.__grains__, {'os': 'Fedora'}):
            with patch.object(rh_ip, '_raise_error_iface', return_value=None):

                self.assertRaises(AttributeError,
                                  rh_ip.build_interface,
                                  'iface', 'slave', True)

                with patch.object(rh_ip, '_parse_settings_bond', MagicMock()):
                    mock = jinja2.exceptions.TemplateNotFound('foo')
                    with patch.object(jinja2.Environment,
                                      'get_template',
                                      MagicMock(side_effect=mock)):
                        self.assertEqual(rh_ip.build_interface('iface',
                                                               'vlan',
                                                               True), '')

                    with patch.object(rh_ip, '_read_temp', return_value='A'):
                        with patch.object(jinja2.Environment,
                                          'get_template', MagicMock()):
                            self.assertEqual(rh_ip.build_interface('iface',
                                                                   'vlan',
                                                                   True,
                                                                   test='A'),
                                             'A')

                            with patch.object(rh_ip, '_write_file_iface',
                                              return_value=None):
                                with patch.object(os.path, 'join',
                                                  return_value='A'):
                                    with patch.object(rh_ip, '_read_file',
                                                      return_value='A'):
                                        self.assertEqual(rh_ip.build_interface
                                                         ('iface', 'vlan',
                                                          True), 'A')

    def test_build_routes(self):
        '''
        Test to build a route script for a network interface.
        '''
        with patch.object(rh_ip, '_parse_routes', MagicMock()):
            mock = jinja2.exceptions.TemplateNotFound('foo')
            with patch.object(jinja2.Environment,
                              'get_template', MagicMock(side_effect=mock)):
                self.assertEqual(rh_ip.build_routes('iface'), '')

            with patch.object(jinja2.Environment,
                              'get_template', MagicMock()):
                with patch.object(rh_ip, '_read_temp', return_value='A'):
                    self.assertEqual(rh_ip.build_routes('i', test='t'), 'A')

                with patch.object(rh_ip, '_read_file', return_value='A'):
                    with patch.object(os.path, 'join', return_value='A'):
                        with patch.object(rh_ip, '_write_file_iface',
                                          return_value=None):
                            self.assertEqual(rh_ip.build_routes('i',
                                                                test=None),
                                             'A')

    def test_down(self):
        '''
        Test to shutdown a network interface
        '''
        with patch.dict(rh_ip.__salt__, {'cmd.run':
                                         MagicMock(return_value='A')}):
            self.assertEqual(rh_ip.down('iface', 'iface_type'), 'A')

        self.assertEqual(rh_ip.down('iface', 'slave'), None)

    def test_get_bond(self):
        '''
        Test to return the content of a bond script
        '''
        with patch.object(os.path, 'join', return_value='A'):
            with patch.object(rh_ip, '_read_file', return_value='A'):
                self.assertEqual(rh_ip.get_bond('iface'), 'A')

    def test_get_interface(self):
        '''
        Test to return the contents of an interface script
        '''
        with patch.object(os.path, 'join', return_value='A'):
            with patch.object(rh_ip, '_read_file', return_value='A'):
                self.assertEqual(rh_ip.get_interface('iface'), 'A')

    def test_up(self):
        '''
        Test to start up a network interface
        '''
        with patch.dict(rh_ip.__salt__, {'cmd.run':
                                         MagicMock(return_value='A')}):
            self.assertEqual(rh_ip.up('iface', 'iface_type'), 'A')

        self.assertEqual(rh_ip.up('iface', 'slave'), None)

    def test_get_routes(self):
        '''
        Test to return the contents of the interface routes script.
        '''
        with patch.object(os.path, 'join', return_value='A'):
            with patch.object(rh_ip, '_read_file', return_value='A'):
                self.assertEqual(rh_ip.get_routes('iface'), 'A')

    def test_get_network_settings(self):
        '''
        Test to return the contents of the global network script.
        '''
        with patch.object(rh_ip, '_read_file', return_value='A'):
            self.assertEqual(rh_ip.get_network_settings(), 'A')

    def test_apply_network_settings(self):
        '''
        Test to apply global network configuration.
        '''
        with patch.dict(rh_ip.__salt__, {'service.restart':
                                         MagicMock(return_value=True)}):
            self.assertTrue(rh_ip.apply_network_settings())

    def test_build_network_settings(self):
        '''
        Test to build the global network script.
        '''
        with patch.object(rh_ip, '_parse_rh_config', MagicMock()):
            with patch.object(rh_ip, '_parse_network_settings', MagicMock()):

                mock = jinja2.exceptions.TemplateNotFound('foo')
                with patch.object(jinja2.Environment,
                                  'get_template', MagicMock(side_effect=mock)):
                    self.assertEqual(rh_ip.build_network_settings(), '')

                with patch.object(jinja2.Environment,
                                  'get_template', MagicMock()):
                    with patch.object(rh_ip, '_read_temp', return_value='A'):
                        self.assertEqual(rh_ip.build_network_settings
                                         (test='t'), 'A')

                        with patch.object(rh_ip, '_write_file_network',
                                          return_value=None):
                            with patch.object(rh_ip, '_read_file',
                                              return_value='A'):
                                self.assertEqual(rh_ip.build_network_settings
                                                 (test=None), 'A')


if __name__ == '__main__':
    from integration import run_tests
    run_tests(RhipTestCase, needs_daemon=False)
