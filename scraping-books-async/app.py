"""
Async scraping exercise using the test site http://books.toscrape.com
"""

import requests
import asyncio
import async_timeout
import aiohttp
import logging

from pages.book_page import BookPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('scraping')
loop = asyncio.get_event_loop()


async def fetch_page(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            logger.info(f'Getting page {url}')
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks


def scrape(page_content):
    page = BookPage(page_content)
    books.extend(page.books)


def print_best_books():
    logger.info('Getting best books by rating...')
    best_books = sorted(books, key=lambda x: x.rating * -1)[:10]
    for book in best_books:
        print(book)


def print_cheapest_book():
    logger.info('Getting best books by price...')
    cheapest_books = sorted(books, key=lambda x: x.price)[:10]
    for book in cheapest_books:
        print(book)


logger.info('Scraping books...')
page_content = requests.get('http://books.toscrape.com').content
page = BookPage(page_content)

_books = []

urls = [f'http://books.toscrape.com/catalogue/page-{page_num+1}.html' for page_num in range(page.page_count)]
pages = loop.run_until_complete(get_multiple_pages(loop, *urls))

for page_content in pages:
    page = BookPage(page_content)
    _books.extend(page.books)


books = _books

logger.info(f'{len(books)} books were found')

print_best_books()
print_cheapest_book()
