"""
Parser HTML of books to find its properties.
"""
import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger('scraping.book_parser')


class BookParser:
    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        logger.debug(f'New BookParser created from `{parent}`.')
        self.parent = parent

    def __repr__(self):
        return f'<Book: {self.name}>, ${self.price}, {self.rating} stars'

    @property
    def name(self):
        locator = BookLocators.NAME
        return self.parent.select_one(locator).get('title')

    @property
    def price(self):
        locator = BookLocators.PRICE
        item_price = self.parent.select_one(locator).string

        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))

    @property
    def rating(self):
        locator = BookLocators.RATING
        classes = self.parent.select_one(locator).get('class')
        rating_classes = [r for r in classes if r != 'star-rating']
        return BookParser.RATINGS.get(rating_classes[0])

    @property
    def link(self):
        locator = BookLocators.LINK
        return self.parent.select_one(locator).get('href')

    @property
    def image_src(self):
        locator = BookLocators.IMAGE_SRC
        return self.parent.select_one(locator).get('src')
