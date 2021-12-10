import os
import sqlite3
import unittest

from tests.fixtures import simple_publication, publication_with_double_citation
from scrapers import ScholarScraper


class DBTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect('test.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE publications
                       (title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id)''')

        self.simple_publication = simple_publication
        self.nested_publication = publication_with_double_citation
        self.scholar_scraper = ScholarScraper()

    def tearDown(self) -> None:
        self.connection.close()
        os.remove("test.db")

    def test_simple_inserts(self):
        results = self.cursor.execute('SELECT * from publications')
        print()
        self.assertEqual([], results.fetchall())

        self.cursor.execute("INSERT INTO publications VALUES ('hello', 'j1', 'pl1', 'cl1', 'at', 0, Null)")
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expected_results = [(1, 'hello', 'j1', 'pl1', 'cl1', 'at', 0, None)]
        self.assertEqual(expected_results, results.fetchall())

        self.cursor.execute("INSERT INTO publications VALUES ('hello1', 'j2', 'pl2', 'cl2', 'at2', 1, Null)")
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expecte_results = [(1, 'hello', 'j1', 'pl1', 'cl1', 'at', 0, None),
                           (2, 'hello1', 'j2', 'pl2', 'cl2', 'at2', 1, None)]
        self.assertEqual(expecte_results, results.fetchall())

        self.cursor.execute("INSERT INTO publications VALUES ('hello3', 'j4', 'pl5', 'cl6', 'at7', 0, 2)")
        self.cursor.execute("DELETE FROM publications where rowid = 1")
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expected_results = [(2, 'hello1', 'j2', 'pl2', 'cl2', 'at2', 1, None),
                            (3, 'hello3', 'j4', 'pl5', 'cl6', 'at7', 0, 2)]
        self.assertEqual(expected_results, results.fetchall())

    def test_unique_check(self):
        """Tests whether identical rows can be inserted"""
        self.cursor.execute("INSERT INTO publications VALUES ('hello', 'j1', 'pl1', 'cl1', 'at', 0, Null)")
        self.cursor.execute("INSERT INTO publications VALUES ('hello', 'j1', 'pl1', 'cl1', 'at', 0, Null)")
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expected_results = [(1, 'hello', 'j1', 'pl1', 'cl1', 'at', 0, None),
                            (2, 'hello', 'j1', 'pl1', 'cl1', 'at', 0, None)]
        self.assertEqual(expected_results, results.fetchall())

    def test_insert_publication_simple(self):
        """Tests method from scrapers that inserts Publication objects into DB"""
        self.scholar_scraper.store_publications([self.simple_publication], db_connection=self.connection)
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expected_result = [(1, 'Article Title', 'Journal Info', 'https://pub_link.com', 'https://cit_link.com',
                            'Author 1, Author 2', 0, None)]
        self.assertEqual(expected_result, results.fetchall())

    def test_insert_publication_nested(self):
        """Tests method from scrapers that inserts Publication objects into DB using Publication objects with citations"""
        self.scholar_scraper.store_publications([self.nested_publication], db_connection=self.connection)
        results = self.cursor.execute(
            'SELECT rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id from publications')
        expected_result = [(1,
                            'Article Title III',
                            'Journal Info III',
                            'https://pub_linkII.com',
                            'https://cit_linkII.com',
                            'Author 5, Author 6',
                            2,
                            None),
                           (2,
                            'Article Title II',
                            'Journal Info II',
                            'https://pub_linkII.com',
                            'https://cit_linkII.com',
                            'Author 3, Author 4',
                            1,
                            1),
                           (3,
                            'Article Title',
                            'Journal Info',
                            'https://pub_link.com',
                            'https://cit_link.com',
                            'Author 1, Author 2',
                            0,
                            2),
                           (4,
                            'Article Title 3',
                            'Journal Info',
                            'https://pub_link.com',
                            'https://cit_link.com',
                            'Author 0',
                            0,
                            1)]
        self.assertEqual(expected_result, results.fetchall())


if __name__ == '__main__':
    unittest.main()
