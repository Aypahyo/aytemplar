from logging import Logger
import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from aytemplar_core.replacer import Replacer

class TestReplacer(unittest.TestCase):
    __uut : Replacer = None
    __logger : Logger = None

    def setUp(self):
        self.__logger = MagicMock()
        self.__uut : Replacer = Replacer( logger = self.__logger)

    def test_load_raises_if_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            self.__uut.load("file")

    def test_repalce_warns_if_no_replacement_was_detected(self):
        self.__uut.load("tests/test_replacer_data/no_env_reference.txt")
        self.__uut.replace_from_env()
        self.__logger.warn.assert_called_once()

    @mock.patch.dict(os.environ, {"MULTILINE_VAR": "SHOULD_BE_IGNORED_1", "MULTILINE_VAR\n": "SHOULD_BE_IGNORED_2"})
    def test_repalce_will_not_match_multiline(self):
        filepath = "tests/test_replacer_data/no_multiline.txt"
        self.__uut.load(filepath)
        self.__uut.replace_from_env()
        self.__uut.store(filepath)
        with open(filepath, "r") as file:
            actual = file.read()
        self.assertFalse("SHOULD_BE_IGNORED_1" in actual, "a replacement happened but should not have")
        self.assertFalse("SHOULD_BE_IGNORED_2" in actual, "a replacement happened but should not have")

    @mock.patch.dict(os.environ, {"SHOULD_BE_REPLACED": "has been replaced"})
    def test_repalce_replaces_a_variable(self):
        filepath = "tests/test_replacer_data/one_replacement.txt"
        expected='This string has been replaced and this string $SHOULD_BE_REPLACED was not.'
        with open(filepath, "w+") as file:
            file.write('This string ${SHOULD_BE_REPLACED} and this string $SHOULD_BE_REPLACED was not.')
        self.__uut.load(filepath)
        self.__uut.replace_from_env()
        self.__uut.store(filepath)
        with open(filepath, "r") as file:
            actual = file.read()
        self.assertEqual(expected, actual)

    def test_repalce_raises_if_env_is_missing_key(self):
        filepath = "tests/test_replacer_data/env_is_missing_key.txt"
        with open(filepath, "w+") as file:
            file.write('The ${ENV_IS_MISSING_THIS_KEY}')
        self.__uut.load(filepath)
        with self.assertRaises(TypeError):
            self.__uut.replace_from_env()
