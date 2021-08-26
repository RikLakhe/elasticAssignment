import unittest
from unittest import mock
from unittest import TestCase

from elasticbook import ElasticBook

class ElasticBookTest(TestCase):
    def setUp(self) -> None:
        self.elasticbook = ElasticBook()

    def tearDown(self) -> None:
        self.elasticbook.clean_up()

    @mock.patch('builtins.input', return_value='test.txt')
    def test_set_filename(self, input):
        self.elasticbook.start_bookfile_process()
        self.assertEqual(self.elasticbook.get_filename(), 'test.txt')

    @unittest.skip("Empty passed, avoid uploading big data again")
    @mock.patch('builtins.input', return_value='')
    def test_set_filename_empty(self,input):
        self.elasticbook.start_bookfile_process()
        self.assertEqual(self.elasticbook.get_filename(), 'pg18866.txt')

    def test_check_elasticsearch(self):
        self.assertTrue(self.elasticbook.check_elasticsearch_connection())

    @mock.patch('builtins.input', return_value='test.txt')
    def test_check_bookfile_not_opened(self, input):
        self.assertFalse(self.elasticbook.check_bookfile_opened())

    @mock.patch('builtins.input', return_value='test2.txt')
    def test_check_bookfile_not_found(self, input):
        with self.assertRaises(FileNotFoundError):
            self.elasticbook.start_bookfile_process()

    @mock.patch('builtins.input', return_value='test.txt')
    def test_check_bookfile_opened(self,input):
        self.elasticbook.start_bookfile_process()
        self.assertTrue(self.elasticbook.check_bookfile_opened())

    @mock.patch('builtins.input', return_value='test.txt')
    def test_check_elasticsearch_upload(self,input):
        self.elasticbook.start_bookfile_process()
        response = self.elasticbook.search("newsletter")
        self.assertEqual(response['hits']['hits'][0]['_source']['content'],' This website includes information about Project Gutenberg-tm, including how to make donations to the Project Gutenberg Literary Archive Foundation, how to help produce our new eBooks, and how to subscribe to our email newsletter to hear about new eBooks.')

if __name__ == '__main__':
    unittest.main()
