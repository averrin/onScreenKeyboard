__author__ = 'tsa'
import unittest
from ConfigManager import ConfigManager

class testConfigManager(unittest.TestCase):
    def setUp(self):
        pass

    def testGetKeyNameFromStrMulti(self):
        filename="test_keyboard_config.conf"

        in_str="24:\"Esc,Esc\":3,2"
        result_must_be=['Esc','Esc']

        manager=ConfigManager(filename)

        self.assertListEqual(manager.getKeyNameFromStr(in_str),result_must_be)

    def testGetKeyNameFromStr(self):
        filename="test_keyboard_config.conf"

        in_str="24:\",,,\":3,2"
        result_must_be=[',',',']

        manager=ConfigManager(filename)

        self.assertListEqual(manager.getKeyNameFromStr(in_str),result_must_be)

    def testDictsKeysCorrect(self):
        filename="test_keyboard_config.conf"

        in_str="24:\",,,\":3,2"
        result_must_be=[3,2]

        manager=ConfigManager(filename)

        self.assertEqual(manager.index_to_key_name_dict.keys()[0],9)
        self.assertEqual(manager.index_to_key_pos.keys()[0],9)

    def testGetKeyNaPosFromStr(self):
        filename="test_keyboard_config.conf"

        in_str="24:\",,,\":3,2"
        result_must_be=[3,2]

        manager=ConfigManager(filename)

        self.assertListEqual(manager.getKeyPosFromStr(in_str),result_must_be)

    def testCreateConfigFromFile(self):
        filename="test_keyboard_config.conf"

        manager=ConfigManager(filename)

        self.assertEqual(manager.getNumOfRows(),5)

