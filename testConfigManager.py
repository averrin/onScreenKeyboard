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

        manager=ConfigManager()

        self.assertListEqual(manager.getKeyNameFromStr(in_str),result_must_be)

    def testGetKeyNameFromStr(self):
        filename="test_keyboard_config.conf"

        in_str="24:\",,,\":3,2"
        result_must_be=[',',',']

        manager=ConfigManager()

        self.assertListEqual(manager.getKeyNameFromStr(in_str),result_must_be)

    def testDictsKeysCorrect(self):
        filename="test_keyboard_config.conf"

        in_str="9:\"Esc,Esc,Esc,Esc\":5,5"
        result_must_be=[3,2]

        manager=ConfigManager()

        self.assertEqual(manager.index_to_key_name_dict.keys()[0],133)
        self.assertEqual(manager.index_to_key_pos.keys()[0],133)

    def testGetKeyNaPosFromStr(self):
        filename="test_keyboard_config.conf"

        in_str="24:\",,,\":3,2"
        result_must_be=[3,2]

        manager=ConfigManager()

        self.assertListEqual(manager.getKeyPosFromStr(in_str),result_must_be)

    def testCreateConfigFromFile(self):
        filename="test_keyboard_config.conf"

        manager=ConfigManager()

        self.assertEqual(manager.getNumOfRows(),6)

