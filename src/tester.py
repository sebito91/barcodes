""" Module to build all of the barcodes """
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import defaultdict
from pprint import pprint

import csv
import os

import barcode

def run_it():
    """ handle the function """
    print "DEBUG -- testing velveteen"
    files = os.path.dirname(os.path.abspath(__file__))
    if not files:
        raise ValueError("could not find path for sources")

    files = files + "/raw_data/"

    # generate the list of files
    only_files = [f for f in os.listdir(files) if os.path.isfile( \
            os.path.join(files, f))]

    print "DEBUG -- files: {}, {}".format(files, only_files)

    output = defaultdict(list)

    for each in only_files:
        with open(files + each) as csvfile:
            reader = csv.reader(csvfile)

            output = {row[2]: row[1].split('\n') for row in reader \
                    if len(row[2]) > 0 and 'Name' not in row[2]}
#            for row in reader:
#                if len(row[2]) > 0:
#                    output[row[2]] = row[1].split('\n')

    print "DEBUG -- finished reading files"
    pprint(output)


if __name__ == "__main__":
    run_it()
