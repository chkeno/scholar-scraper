import unittest

from models import Publication, PublicationSchema
from tests.fixtures import simple_publication, simple_publication_2, publication_with_single_citation, publication_with_double_citation


class ModelTests(unittest.TestCase):

    def setUp(self) -> None:
        """
        Method runs before each test to set up test data
        """
        self.simple_publication = simple_publication
        self.simple_publication_2 = simple_publication_2
        self.publication_with_single_citation = publication_with_single_citation
        self.publication_with_double_citation = publication_with_double_citation
        self.publication_schema = PublicationSchema()

    def test_single_dump(self):
        actual_simple_publication_json = self.publication_schema.dump(self.simple_publication)
        expected_simple_publication_json = {'authors_text': 'Author 1, Author 2',
                                            'citation_link': 'https://cit_link.com',
                                            'citations': None,
                                            'citations_count': 0,
                                            'journal_info': 'Journal Info',
                                            'publication_link': 'https://pub_link.com',
                                            'title': 'Article Title'}
        self.assertEqual(actual_simple_publication_json, expected_simple_publication_json)

    def test_single_publication_dump(self):
        actual_publication_with_single_citation_json = self.publication_schema.dump(
            self.publication_with_single_citation)
        expected_publication_with_single_citation_json = {'authors_text': 'Author 3, Author 4',
                                                          'citation_link': 'https://cit_linkII.com',
                                                          'citations': [{'authors_text': 'Author 1, Author 2',
                                                                         'citation_link': 'https://cit_link.com',
                                                                         'citations': None,
                                                                         'citations_count': 0,
                                                                         'journal_info': 'Journal Info',
                                                                         'publication_link': 'https://pub_link.com',
                                                                         'title': 'Article Title'}],
                                                          'citations_count': 1,
                                                          'journal_info': 'Journal Info II',
                                                          'publication_link': 'https://pub_linkII.com',
                                                          'title': 'Article Title II'}
        self.assertEqual(actual_publication_with_single_citation_json, expected_publication_with_single_citation_json)

    def test_publication_with_double_citation_dump(self):
        actual_publication_with_double_citation_json = self.publication_schema.dump(
            self.publication_with_double_citation)
        expected_publication_with_double_citation_json = {'authors_text': 'Author 5, Author 6',
                                                          'citation_link': 'https://cit_linkII.com',
                                                          'citations': [{'authors_text': 'Author 3, Author 4',
                                                                         'citation_link': 'https://cit_linkII.com',
                                                                         'citations': [
                                                                             {'authors_text': 'Author 1, Author 2',
                                                                              'citation_link': 'https://cit_link.com',
                                                                              'citations': None,
                                                                              'citations_count': 0,
                                                                              'journal_info': 'Journal Info',
                                                                              'publication_link': 'https://pub_link.com',
                                                                              'title': 'Article Title'}],
                                                                         'citations_count': 1,
                                                                         'journal_info': 'Journal Info II',
                                                                         'publication_link': 'https://pub_linkII.com',
                                                                         'title': 'Article Title II'},
                                                                        {'authors_text': 'Author 0',
                                                                         'citation_link': 'https://cit_link.com',
                                                                         'citations': None,
                                                                         'citations_count': 0,
                                                                         'journal_info': 'Journal Info',
                                                                         'publication_link': 'https://pub_link.com',
                                                                         'title': 'Article Title 3'}],
                                                          'citations_count': 2,
                                                          'journal_info': 'Journal Info III',
                                                          'publication_link': 'https://pub_linkII.com',
                                                          'title': 'Article Title III'}
        self.assertEqual(actual_publication_with_double_citation_json, expected_publication_with_double_citation_json)


if __name__ == '__main__':
    unittest.main()
