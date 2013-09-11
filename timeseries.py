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
    parser.add_argument("-x",
                        help = "the key to use for the function being plotted",
                        default=None)

    args = parser.parse_args()

    input_file_name = args.input_file

    y_key = str(args.y)
    x_key = args.x

    #initialize the x axis and function to be plotted
    x = []
    y = []

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if not line.rstrip() : continue
            try:
                obj = json.loads(line)
            except ValueError:
                print("Skipping invalid JSON: %s" % line)
                continue

            #if the parsed JSON object has the key we're looking for,
            #add the key's value to the y graph and the timestamp
            #to the x list
            if obj['name'] == y_key:
                y.append(obj['value'])
                if x_key is None:
                    x.append(obj['timestamp'])
            if obj['name'] == x_key:
                x.append(obj['value'])

        autoscale(True, 'both')
        xlabel(x_key or 'timestamp')
        ylabel(y_key)
        plot(x, y, 'ro')
        show()

if __name__ == "__main__":
    main()
