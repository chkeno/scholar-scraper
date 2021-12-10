"""Fixtures for tests"""
from models import Publication

simple_publication = Publication(title='Article Title',
                                 journal_info='Journal Info',
                                 publication_link='https://pub_link.com',
                                 citation_link='https://cit_link.com',
                                 authors_text='Author 1, Author 2',
                                 citations_count=0
                                 )
simple_publication_2 = Publication(title='Article Title 3',
                                   journal_info='Journal Info',
                                   publication_link='https://pub_link.com',
                                   citation_link='https://cit_link.com',
                                   authors_text='Author 0',
                                   citations_count=0
                                   )

publication_with_single_citation = Publication(title='Article Title II',
                                               journal_info='Journal Info II',
                                               publication_link='https://pub_linkII.com',
                                               citation_link='https://cit_linkII.com',
                                               authors_text='Author 3, Author 4',
                                               citations_count=1,
                                               citations=[simple_publication]
                                               )
publication_with_double_citation = Publication(title='Article Title III',
                                               journal_info='Journal Info III',
                                               publication_link='https://pub_linkII.com',
                                               citation_link='https://cit_linkII.com',
                                               authors_text='Author 5, Author 6',
                                               citations_count=2,
                                               citations=[publication_with_single_citation,
                                                          simple_publication_2]
                                               )
