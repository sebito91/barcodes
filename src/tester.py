""" Module to build all of the barcodes """
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import defaultdict
from pprint import pprint

import csv
import os

import barcode
from barcode.writer import ImageWriter

def barcode_it(product, sku, path):
    """ barcode all the things """
    if len(sku) < 1:
        return False

    # update to save as png
    ean = barcode.get('ean13', sku.replace('-', ''), writer=ImageWriter())

    try:
        return bool(ean.save(''.join([path, '_'.join([product.replace(' ', '_'), sku])])))
    except IOError:
        print "ERROR -- path name is incorrect -- path: {}, prod: {}, sku: {}".format(\
                path, product, sku)

    return False

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

    vendors = {f.split('.')[0]: f for f in only_files if '.csv' in f and not "~" in f}

    print "DEBUG -- files: {}, {}".format(vendors, only_files)


    output = defaultdict(lambda: defaultdict(list))

    for vendor, each in vendors.iteritems():
        with open(files_raw + each) as csvfile:
            reader = csv.reader(csvfile)

            output[vendor] = {row[2]: row[1].split('\n') for row in reader \
                    if len(row) > 1 and len(row[2]) > 0 and 'Name' not in row[2]}

    #print "DEBUG -- finished reading files"
    failed = defaultdict(list)

    print "DEBUG -- output: {}".format(output)

    for vendor in output:
        print "DEBUG -- handling {}".format(vendor)
        for each, val in output[vendor].iteritems():
            failed[vendor] = [(each, item) for item in val if not \
                    barcode_it(each, item, ''.join([files, "/", vendor, "/"]))]

    print "DEBUG -- done with barcode generation, failed: {}".format(failed)

if __name__ == "__main__":
    run_it()
