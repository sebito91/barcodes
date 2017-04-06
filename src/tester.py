""" Module to build all of the barcodes """
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import defaultdict
from pprint import pprint

import csv
import os

import barcode

def barcode_it(product, sku, path):
    """ barcode all the things """
    if len(sku) < 1:
        return False

    ean = barcode.get('ean13', sku.replace('-', ''))

    return bool(ean.save(''.join([path, '_'.join([product.replace(' ', '_'), sku])])))

def run_it():
    """ handle the function """
    print "DEBUG -- testing velveteen"
    files = os.path.dirname(os.path.abspath(__file__))
    if not files:
        raise ValueError("could not find path for sources")

    #print "DEBUG -- {}, {}".format(files, os.path.abspath(__file__))

    files_raw = files + "/raw_data/"

    # generate the list of files
    only_files = [f for f in os.listdir(files_raw) if os.path.isfile( \
            os.path.join(files_raw, f))]

    #print "DEBUG -- files: {}, {}, {}".format(files, files_raw, only_files)

    output = defaultdict(list)

    for each in only_files:
        with open(files_raw + each) as csvfile:
            reader = csv.reader(csvfile)

            output = {row[2]: row[1].split('\n') for row in reader \
                    if len(row[2]) > 0 and 'Name' not in row[2]}

    #print "DEBUG -- finished reading files"
    pprint(output)
    failed = []

    for each, val in output.iteritems():
        failed += [(each, item) for item in val if not \
                barcode_it(each, item, ''.join([files, "/velveteen/"]))]

    print "DEBUG -- done with gens, failed: {}".format(failed)

if __name__ == "__main__":
    run_it()
