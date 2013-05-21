#!/usr/bin/python

#Go through an OpenXC trace file and print out a list
#of all present signals.

import json
import sys
import argparse

def main():
    #Set up the command line argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file",
                        help = "name of the input file")

    args = parser.parse_args()

    input_file_name = args.input_file

    signal_list = list()

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if not line.rstrip() : continue
            try:
                obj = json.loads(line)
            except ValueError:
                print("Skipping invalid JSON: %s" % line)
                continue

            if obj['name'] not in signal_list:
                signal_list.append(obj['name'])

    signal_list.sort()
    print "\n".join(signal_list)

if __name__ == "__main__":
    main()
