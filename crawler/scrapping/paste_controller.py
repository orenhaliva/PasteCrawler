import logging
import re
from datetime import datetime

from lxml import html

from crawler.config import TorConfig, PasteXPathConfig, PasteNormalizeConfig
from crawler.db_handler.paste import Paste
from crawler.scrapping import tor


class OldPasteException(Exception):
    pass


class PasteCrawler(object):
    """
    This class is responsible for scraping the pastes from the website
    You can get all the pastes or pastes from specific page.

    this class is coupled to tor send request because
    this website is working only with tor proxy
    """
    URI_ALL = "all"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_pastes(self, min_date=None):
        pastes = tor.send_get_request(TorConfig.URL + self.URI_ALL)
        html_content = html.fromstring(pastes)
        page_elem = html_content.xpath(PasteXPathConfig.PAGINATION)

        # two elements for going backward and forward
        pages = len(page_elem) - 2
        self.logger.info("number of pages is: {0}".format(str(pages)))
        try:
            # plus one is offset for range
            for page_number in range(1, pages + 1):
                for paste in self.get_pastes_per_page(page_number, min_date):
                    yield paste
        except OldPasteException:
            self.logger.info("No more new pastes")

    def get_pastes_per_page(self, page_number, min_date):
        full_url = TorConfig.URL + self.URI_ALL + "?page=" + str(page_number)
        pastes = tor.send_get_request(full_url)
        html_content = html.fromstring(pastes)
        urls = html_content.xpath(PasteXPathConfig.PASTE_URL)
        self.logger.info("Found {0} urls are found in: {1}"
                         .format(len(urls), full_url))
        for url in urls:
            yield self.get_paste(url, min_date)

    def get_paste(self, url, min_date):
        try:
            self.logger.info("Scraping new url: {0}".format(url))
            paste = self.scrap_paste(url)
            if not min_date or paste.creation_date > min_date:
                self.logger.info("Done scraping paste: {0}:"
                                 .format(paste.__dict__))
                return paste
            else:
                self.logger.info("Found an old paste: {0}:"
                                 .format(url))
                # the pages are sort by date
                # so if we found an old one the rest will be older too
                raise OldPasteException(url)
        # can not get paste page, useless to continue
        except (IOError, OldPasteException):
            raise
        except Exception:
            self.logger.exception("Scraping went wrong url: {0}"
                                  .format(url))

    def scrap_paste(self, url):
        paste_text = tor.send_get_request(url)
        paste_content = html.fromstring(paste_text)
        paste_element = paste_content.xpath(PasteXPathConfig.PASTE_ELEMENT)[0]
        title_elem = paste_element.xpath(PasteXPathConfig.TITLE)
        title = str(title_elem[0]).strip()
        content = ''.join(paste_element.xpath(PasteXPathConfig.CONTENT))
        footer_element = paste_element.xpath(PasteXPathConfig.FOOTER)
        footer = ''.join(footer_element)
        author, date = self._extract_author_and_date(footer)

        return Paste(author, title, date, content)

    def _extract_author_and_date(self, footer):
        m = re.match(PasteNormalizeConfig.FOOTER_REGEX, footer)

        author = m.group("author")
        if author in PasteNormalizeConfig.UNKNOWN_AUTHORS:
            author = PasteNormalizeConfig.DEFAULT_AUTHOR

        date_str = m.group("date")
        date = datetime.strptime(date_str, PasteNormalizeConfig.DATE_FORMAT)
        return author, date
