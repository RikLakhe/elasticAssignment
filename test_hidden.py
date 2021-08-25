import unittest

import hidden


class HiddenTest(unittest.TestCase):

    def setUp(self):
        self.secrets = hidden.elastic()

    def test_hidden_gives_correct_values(self):
        self.assertEqual(self.secrets["host"], "www.pg4e.com")
