from unittest import TestCase

from elasticmail import Elasticmail

class ElasticMailTest(TestCase):

    def setUp(self) -> None:
        self.elasticmail = Elasticmail()

    def tearDown(self) -> None:
        self.elasticmail.end_all()

    def test_check_elastic_server_connection_success(self):
        self.assertTrue(self.elasticmail.check_elastic_server_connection())

    def test_initial_elastic_search_zero_hits(self):
        response = (self.elasticmail.search('test'))
        self.assertEqual(len(response['hits']['hits']), 0)