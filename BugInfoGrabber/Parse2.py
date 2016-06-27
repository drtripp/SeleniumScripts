import argparse
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Parser2 import Parser


def parse(browser, listfile, output):
    results = list()
    parser = Parser(browser)
    try:
        buglist = open(listfile, 'rb')
        urlreader = csv.reader(buglist, delimiter='\t')
        row = urlreader.next()
        row = urlreader.next()
        while row:
            if(row[0] == ''):
			    break
            print row[1]
            results.append(parser.parse(row[1]))
            try:
                row = urlreader.next()
            except StopIteration:
                print 'Input File Parsed'
                row = None;
    except KeyboardInterrupt:
        sys.stdout.write('\r')
        info('Exiting...')
    finally:
        parser.teardown()

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=(
                'Script to scrape bug details from premade tsv bug list.'
            )
        )
    parser.add_argument(
            '-b', dest='browser', default='chrome',
            choices=['phantom', 'firefox', 'chrome'],
            help=(
			    'The browser to use when retrieving the search results.'
                '(Only Chrome implemented)'
            )
        )

    parser.add_argument(
            'listfile',
            help=(
                'Name of .tsv file to read from (include .tsv/.csv in param)'
            )
        )
    parser.add_argument(
            'output', help=(
                'Path to the file to which the parse results should be '
                'written.'
            )
        )
    args = parser.parse_args()

    results = parse(
            args.browser, args.listfile, args.output
        )
    if results:
        with open(args.output, 'wb') as file_:
            writer = csv.writer(file_, delimiter = '\t', lineterminator = '\n')
            writer.writerows(results)
