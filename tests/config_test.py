# Copyright (c) 2016-2017 Adobe Systems Incorporated.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import types
import unittest

import mock
import tests.helper
import user_sync.identity_type
from user_sync.error import AssertionException
from user_sync.config import ConfigLoader
from user_sync.config import ObjectConfig


class ConfigLoaderTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    @mock.patch('user_sync.config.ConfigFileLoader.load_from_yaml')
    def setUp(self, mock_yaml, mock_isfile):
        mock_isfile.return_value = True
        self.conf_load = ConfigLoader({'options': 'testOpt'})

    def test_get_dict_from_sources_str_found(self):
        # AssertionException when file not loaded by load_from_yaml
        self.assertRaises(AssertionException, lambda: self.conf_load.get_dict_from_sources(['test']))

    @mock.patch('user_sync.config.DictConfig.get_string')
    @mock.patch('user_sync.config.DictConfig.get_dict_config')
    @mock.patch('user_sync.config.DictConfig.get_list_config')
    @mock.patch('user_sync.identity_type.parse_identity_type')
    def test_get_rule_options(self, mock_id_type,mock_get_dict,mock_get_list,mock_get_string):
        mock_id_type.return_value = 'new_acc'
        mock_get_dict.return_value = tests.helper.MockDictConfig()
        mock_get_list.return_value = tests.helper.MockDictConfig()
        options = self.conf_load.get_rule_options()
        expected = {
            'after_mapping_hook': None,
            'default_country_code': 'test',
            'delete_strays': False,
            'directory_group_filter': None,
            'directory_group_mapped': False,
            'disentitle_strays': False,
            'exclude_groups': [],
            'exclude_identity_types': [],
            'exclude_strays': False,
            'exclude_users': [],
            'extended_attributes': None,
            'manage_groups': False,
            'max_adobe_only_users': 1,
            'new_account_type': 'new_acc',
            'remove_strays': False,
            'stray_list_input_path': None,
            'stray_list_output_path': None,
            'update_user_info': True,
            'username_filter_regex': None,
        }
        self.assertEquals(options,
                          expected,
                          'rule options are returned')

    def test_parse_string(self):
        self.assertEquals(self.conf_load.parse_string('{1}{2}{3}', 'abcde'),
                          {'1': 'abc', '3': 'e', '2': 'd'}, 'test parsing 1')
        self.assertEquals(self.conf_load.parse_string('{1}', 'abcde'),{'1': 'abcde'}, 'test parsing 2')


class ObjectConfigTest(unittest.TestCase):
    def setUp(self):
        self.object_conf = ObjectConfig(self)

    def test_describe_types(self):
        self.assertEquals(self.object_conf.describe_types(types.StringTypes), ['str'], 'strings are handeled')
        self.assertEquals(self.object_conf.describe_types(types.BooleanType), ['bool'], 'other types are handeled')
