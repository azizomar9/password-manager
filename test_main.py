import unittest
from main import *

#testing hashing master password function
class TestMain(unittest.TestCase):

    def test_hash_master_password(self):
        actual = hash_master_password("dad".encode('utf-8'))
        expected = ("df3939f11965e7e75dbc046cd9af1c67")
        self.assertEqual(actual, expected)

    def test_user_password_check(self):
        actual = user_password_check("test", "result")
        expected = ("result")
        self.assertEqual(actual, expected)