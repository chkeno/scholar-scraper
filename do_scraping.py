"""Script run for scraping."""

import sqlite3

from constants import database_name
from models import Publication
from scrapers import ScholarScraper

scholar_scraper = ScholarScraper()

connection = sqlite3.connect('scraped.db')

# # Let start with the Dorrestein paper
# publications = scholar_scraper.scrape_result_page(
#     'https://scholar.google.com/scholar?as_q=&as_epq=Molecular+Networking%3A+A+Useful+Tool+for+the+Identification+of+New+Psychoactive+Substances+in+Seizures+by+LC%E2%80%93HRMS&as_oq=&as_eq=&as_occt=title&as_sauthors=&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=4005&sciodt=0%2C6&cites=14607346792419271180&scipsc=',
#     depth_level=5)
#
# scholar_scraper.store_publications(publications, db_connection=connection)
# connection.commit()
#
# # That big CRISPR paper
# publications = scholar_scraper.scrape_result_page(
#     'https://scholar.google.com/scholar?as_q=&as_epq=A+programmable+dual-RNA-guided+DNA+endonuclease+in+adaptive+bacterial+immunity&as_oq=&as_eq=&as_occt=title&as_sauthors=&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C6&as_vis=1',
#     depth_level=7)
#
# scholar_scraper.store_publications(publications, db_connection=connection)
# connection.commit()


# Quick check that our results made it in.
sql = """
SELECT 
    rowid, title, journal_info, publication_link, citation_link, authors_text, citations_count 
FROM publications
"""

cursor = connection.cursor()
cursor.execute(sql)
results = cursor.fetchall()

print(results)