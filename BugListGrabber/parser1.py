import re
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from logger1 import *

# Convenience Aliases
CLASS = By.CLASS_NAME
CSS = By.CSS_SELECTOR
ID = By.ID
TAG = By.TAG_NAME

# Date Parsing
DATE_RE = re.compile('(\d{4})-(\d{2})-(\d{2})')
YEAR_RE = re.compile('(\d{4})')


class Parser(object):
    def __init__(self, service, browser):
        self.service = service
        self.browser = browser
        self.driver = webdriver.Chrome()

    def get_header(self):
        return ('bug_id', 'link')

    def parse(self, url):
        debug('Parsing {}'.format(url))
        return self._parse_firefox_bug_list(url)

    def setup(self):
        self.driver = self._get_driver(self.browser)

    def teardown(self):
        if self.driver:
            self.driver.close()

    def _get_driver(self, browser):
        driver = None

        if browser == 'firefox':
            driver = webdriver.Firefox()
        elif browser == 'phantom':
            driver = webdriver.PhantomJS()
        elif browser == 'chrome':
            driver = webdriver.Chrome()
        else:
            error('Cannot create driver for browser {}'.format(browser))
            sys.exit(1)

        return driver

    def _parse_firefox_bug_list(self, url):
        _results = list()

        try:
            self.driver.get(url)
            results = self.driver.find_element(CLASS, 'sorttable_body')
            for result in results.find_elements(By.TAG_NAME, 'tr'):
                bug_id = 0
                link = ''
				
                bug_id = result.get_attribute('id')
                link = result.find_element(CSS, 'a').get_attribute('href')

                _results.append((bug_id, link))
        except WebDriverException:
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)

        return _results

    def _contains(self, element, by, value):
        elements = element.find_elements(by, value)
        return len(elements) > 0
