"""
Module containing methods for retrieving information from Google Scholar using web calls.
Information from Google Scholar is scraped using Beautiful Soup
"""
from bs4 import BeautifulSoup
import time
from typing import List
import requests
import sqlite3
from selenium import webdriver
from urllib import parse
from webdriver_manager.chrome import ChromeDriverManager

from constants import database_name
from models import Publication


class ScholarScraper:
    """
    Class containing various methods for querying Google Scholar.
    """

    def scrape_result_page(self, query_url: str, citation_tree_depth: int = 0) -> List[Publication]:
        """
        Scrapes Google Scholar results page given input URl and parameters. These are the types of pages that return
        when a title is searched or a link to citations is followed. Will scrape citation results pages if
        dept_level is greater than 0. Scraped results are stored in database for future retrieval.

        TODO: Pagination, this scraper currently only search the first page of results, which is limited to 10 results.

        :param query_url: Google Scholar results url
        :param citation_tree_depth: Integer representing the number of child-citations the scraper should go down to discovery tree structure
        :return: List of scraped Publication objects
        """

        response = requests.get(query_url)
        # If Google catches on, you have to start manually solving captcha puzzles
        if response.status_code == requests.codes.too_many:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(query_url)
            time.sleep(15)
            full_page = driver.page_source
            driver.close()
        else:
            full_page = response.text

        publications = []

        soup = BeautifulSoup(full_page, 'html.parser')
        publication_rows = soup.find_all('div', {'class': 'gs_ri'})
        for publication_row in publication_rows:
            title_tag, author_and_journal_tag, _, citations_tag = publication_row.contents

            paper_title = ''
            publication_link = ''
            if title_tag is not None:
                paper_title = title_tag.find('a').text
                publication_link = title_tag.find('a').get('href')

            journal_info_text = ''
            author_text = ''
            if author_and_journal_tag is not None and hasattr(author_and_journal_tag, 'contents') and len(
                    author_and_journal_tag.contents) > 0:
                raw_author_and_journal_info = author_and_journal_tag.text
                author_text, journal_info_text = raw_author_and_journal_info.split('-', 1)

            citations_link = ''
            citations_count = 0
            if citations_tag is not None and hasattr(citations_tag, 'contents') and len(citations_tag.contents) > 0:
                for content in citations_tag.contents:
                    if 'Cited by' in content.text:
                        citations_extension = content.get('href')
                        citations_link = parse.urljoin('https://scholar.google.com/',
                                                       citations_extension) if citations_extension is not None else ''
                        citations_count = int(content.text[9:])

            citations = []
            if citations_count > 0:
                citations = None
            if citation_tree_depth > 0 and citations_link is not '':
                citations = self.scrape_result_page(citations_link, citation_tree_depth=citation_tree_depth - 1)

            publication = Publication(paper_title, journal_info_text, publication_link, citations_link, author_text,
                                      citations_count, citations)
            publications.append(publication)

        return publications

    def store_publications(self, publications: List[Publication], parent_publication_row_id: int = None,
                           db_connection: sqlite3.Connection = None) -> None:
        """
        Helper method for storing Publication objects and their citations in sqlite DB
        :param publications: List of Publication objects
        :param parent_publication_row_id: Optional row ID for parent publications
        :param db_connection: sqlite DB connection
        """

        if db_connection is None:
            connection = sqlite3.connect(database_name)
        else:
            connection = db_connection

        cursor = connection.cursor()

        sql = """
        INSERT INTO publications (
            title, 
            journal_info, 
            publication_link, 
            citation_link, 
            authors_text, 
            citations_count, 
            parent_publication_row_id
        ) VALUES (
            :title, 
            :journal_info, 
            :publication_link, 
            :citation_link, 
            :authors_text, 
            :citations_count, 
            :parent_publication_row_id
        )
        """

        for publication in publications:

            parameters = {
                'title': publication.title,
                'journal_info': publication.journal_info,
                'publication_link': publication.publication_link,
                'citation_link': publication.citation_link,
                'authors_text': publication.authors_text,
                'citations_count': publication.citations_count,
                'parent_publication_row_id': parent_publication_row_id
            }
            cursor.execute(sql, parameters)
            last_row_id = cursor.lastrowid
            if publication.citations is not None:
                self.store_publications(publication.citations, last_row_id, connection)

        if db_connection is None:
            # Only commit the changes if a cursor was not passed as argument.
            # If the connection is an argument, it is assumed the original creator of the connection will commit and close it.
            connection.commit()
            connection.close()
