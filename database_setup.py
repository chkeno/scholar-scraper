"""Script for setting up sqlite database. Only need to run once unless database file has been deleted"""

import sqlite3

from constants import database_name

con = sqlite3.connect(database_name)
cur = con.cursor()

cur.execute('''
CREATE TABLE publications
(title, journal_info, publication_link, citation_link, authors_text, citations_count, parent_publication_row_id)
''')

con.close()
