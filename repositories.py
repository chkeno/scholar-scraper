"""
Module containing methods for retrieving information from sqlite database
"""

import sqlite3
from typing import List

from constants import database_name
from models import Publication


class ScholarRepository:
    """
    Class containing various methods for querying Google Scholar.
    """

    def search_by_title(self, title: str, citation_tree_depth: int = 0) -> List[Publication]:
        """
        Retrive publication from database based on publication title

        :param title: article title
        :param citation_tree_depth: dept to search citations of title
        :return: List of Publication objects that match input title
        """

        publications = []

        sql = """
        SELECT 
            rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count 
        FROM publications
        WHERE lower(title) like :title"""

        parameters = {'title': '%{}%'.format(title.lower())}

        # I know there are smarter ways to do this, where a connection doesn't need to be created so often but I'm new to
        # sqlite and want to make sure I'm closing each connection without having to do anything fancy
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        result = cursor.execute(sql, parameters)
        results = result.fetchall()
        connection.close()

        for row_id, title, journal_info, publication_link, citation_link, authors_text, citations_count in results:
            publication = Publication(title, journal_info, publication_link, citation_link, authors_text, citations_count)
            if citation_tree_depth > 0:
                citations = self.search_by_parent_publication_row_id(row_id, citation_tree_depth - 1)
                publication.citations = citations

            publications.append(publication)

        return publications

    def search_by_parent_publication_row_id(self, parent_publication_row_id: int, citation_tree_depth: int) -> List[Publication]:
        """
        Searches database by parent publication row id
        :param parent_publication_row_id: row ID of parent publication
        :param citation_tree_depth: dept to search citations of title
        :return: List of Publication objects
        """
        publications = []

        sql = """
        SELECT 
            rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count 
        FROM publications
        WHERE 
            parent_publication_row_id = :parent_publication_row_id"""

        parameters = {'parent_publication_row_id': parent_publication_row_id}

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        result = cursor.execute(sql, parameters)
        results = result.fetchall()
        connection.close()

        for row_id, title, journal_info, publication_link, citation_link, authors_text, citations_count in results:
            publication = Publication(title, journal_info, publication_link, citation_link, authors_text,
                                      citations_count)
            if citation_tree_depth > 0:
                citations = self.search_by_parent_publication_row_id(row_id, citation_tree_depth - 1)
                publication.citations = citations

            publications.append(publication)
        return publications
