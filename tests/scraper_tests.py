import unittest

from models import Publication
from scrapers import ScholarScraper


class ScraperTests(unittest.TestCase):

    def setUp(self) -> None:
        self.scholar_scraper = ScholarScraper()

    def test_one_result_with_citations_scrape(self):
        publications = self.scholar_scraper.scrape_result_page(
            'https://scholar.google.com/scholar?as_q=&as_epq=Statistical+properties+and+sensitivity+of+a+new+adaptive+sampling+method+for+quality+control&as_oq=&as_eq=&as_occt=title&as_sauthors=&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C6',
            citation_tree_depth=1)
        expected_publication = [Publication(
            title='Statistical properties and sensitivity of a new adaptive sampling method for quality control',
            journal_info=' Revstat Statistical Journal, 2018 - run.unl.pt',
            publication_link='https://run.unl.pt/handle/10362/31958',
            citation_link='https://scholar.google.com/scholar?cites=14607346792419271180&as_sdt=4005&sciodt=0,6&hl=en&oe=ASCII',
            authors_text='M Carmo, P Infante, JM Mendes\xa0',
            citations_count=1,
            citations=[Publication(
                title='New Sampling Methods in Statistical Process Control',
                journal_info=' cima.uevora.pt',
                publication_link='http://www.cima.uevora.pt/Seminar/sem2019-02-19.pdf',
                citation_link='',
                authors_text='M do Carmo ',
                citations_count=0,
                citations=[])]
        )]
        self.assertEqual(expected_publication, publications)

    def test_one_result_no_citations_scrape(self):
        publications = self.scholar_scraper.scrape_result_page(
            'https://scholar.google.com/scholar?as_q=&as_epq=Economic-statistical+design+of+the+variable+sampling+interval+Poisson+EWMA+chart&as_oq=&as_eq=&as_occt=title&as_sauthors=&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C6',
            citation_tree_depth=1)
        expected_publication = [Publication(
            title='Economic-statistical design of the variable sampling interval Poisson EWMA chart',
            journal_info=' …\xa0in Statistics-Simulation and\xa0…, 2021 - Taylor & Francis',
            publication_link='https://www.tandfonline.com/doi/abs/10.1080/03610918.2021.1898637',
            citation_link='',
            authors_text='MH Lee, MBC Khoo, A Haq…\xa0',
            citations_count=0,
            citations=[])]

        self.assertEqual(expected_publication, publications)  # add assertion here


if __name__ == '__main__':
    unittest.main()
