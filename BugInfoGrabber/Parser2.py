import re
import traceback
import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# Convenience Aliases
CLASS = By.CLASS_NAME
CSS = By.CSS_SELECTOR
ID = By.ID
TAG = By.TAG_NAME

class Parser(object):
    def __init__(self, browser):
        self.driver = webdriver.Chrome()

    def teardown(self):
        if self.driver:
            self.driver.close()

    def parse(self, url):
        _results = list();
        try:
            self.driver.get(url)
            name = ''
            name = self.driver.find_element(ID, 'short_desc_nonedit_display').text

            results = self.driver.find_element(ID, 'attachment_table')
            diffs = list()
            for result in results.find_elements(TAG, 'tr'):
                diffs = list()
                try:
                    links = result.find_element(CLASS, 'bz_attach_actions')
                    print 'step 1'
                    for ele in links.find_elements(CSS, 'a'):
                        print '\t' + ele.text
                        if ele.text == 'Diff':
                            print '\t\tdiff added' + ele.get_attribute('href')
                            diffs.append(ele.get_attribute('href'))
                            name = name + '\t' + ele.get_attribute('href')
                except NoSuchElementException:
                    print 'no more diffs found'
            print 'appending shit'
            _results.append((name))
        except WebDriverException:
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)

        return _results