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

    def parse(self, bugid, url):
        _results = list();
        found = 0
        try:
            self.driver.get(url)
            name = ''
            name = self.driver.find_element(ID, 'short_desc_nonedit_display').text
            oldcode = ''
            newcode = ''
            results = self.driver.find_element(ID, 'attachment_table')
            #diffs = list()
            for result in results.find_elements(TAG, 'tr'):
                #diffs = list()
                try:
                    links = result.find_element(CLASS, 'bz_attach_actions')
                    print 'step 1'
                    for ele in links.find_elements(CSS, 'a'):
                        if ele.text == 'Diff':
                            difflink = ele.get_attribute('href')
                            self.driver.get(difflink)
                            filename = ''
                            for thing in self.driver.find_elements(CLASS, 'file_table'):
                                filename = filename + '\n' + thing.find_element(TAG, 'thead').find_element(CLASS, 'file_head').find_element(TAG, 'input').get_attribute('name')
                            codetable = self.driver.find_element(CLASS, 'file')
                            for line in codetable.find_elements(TAG, 'tr'):
                                proof = 0
                                for datum in line.find_elements(TAG, 'td'):
                                    attr = datum.get_attribute('class')
                                    if attr == 'changed' and proof == 1:
                                        print '\t\t\t\t\t...Changed code'
                                        proof = 0
                                        newcode = newcode + '\n' + datum.text
                                    elif attr == 'changed' and proof == 0:
                                        oldcode = oldcode + '\n' + datum.text
                                        print 'Old code...'
                                        proof = 1
                                    elif attr == 'new':
                                        print '\t\t\t\t\tFound added code'
                                        newcode = newcode + '\n' + datum.text

                            print '\t\tdiff added: ' + difflink + ' with name ' + name
                            found = found + 1
                            _results.append((bugid, name, url, filename, difflink, oldcode, newcode))
                            oldcode, newcode = ['', '']
                except NoSuchElementException:
                    print 'no more diffs found'
            #_results.append((name))
        except WebDriverException:
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)
            print 'something happened'

        if found == 0:
            _results.append((bugid, name, url))
        return _results