#!/usr/bin/env python

#Go through an OpenXC trace file and plot a time series graph using
#matplotlib

import json
import sys
import argparse
from pylab import *

def main():
    #Set up the command line argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file",
                        help = "name of the input file")
    parser.add_argument("-y",
                        help = "the key to use for the function being plotted")

    args = parser.parse_args()

    input_file_name = args.input_file

    y_key = str(args.y)

    #initialize the x axis and function to be plotted
    x = []
    y = []

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if not line.rstrip() : continue
            obj = json.loads(line)

            #if the parsed JSON object has the key we're looking for,
            #add the key's value to the y graph and the timestamp
            #to the x list
            if obj['name'] == y_key:
                y.append(obj['value'])
                x.append(obj['timestamp'])

        autoscale(True, 'both')
        plot(x, y, label = y_key)
        legend(loc='upper left')
        show()

if __name__ == "__main__":
    main()
