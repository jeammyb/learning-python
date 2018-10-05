"""
Parsing page content with BeautifulSoup4.
"""
import re
import logging
from bs4 import BeautifulSoup

from locators.books_page_locators import BooksPageLocators
from parsers.book import BookParser

logger = logging.getLogger('scraping.books_page')


class BookPage:
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    def __repr__(self):
        return f'Book Page: {self.books}'

    def __len__(self):
        return len(self.books)

    @property
    def books(self):
        logger.debug(f'Finding all books in the page using `{BooksPageLocators.BOOKS}`.')
        return [BookParser(b) for b in self.soup.select(BooksPageLocators.BOOKS)]

    @property
    def page_count(self):
        logger.debug('Finding all number of catalogue pages available...')
        content = self.soup.select_one(BooksPageLocators.PAGER).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.debug(f'Extracted number of pages as integer: `{pages}`.')
        return pages
