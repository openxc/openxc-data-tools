#!/usr/bin/env python

#This script will slurp in a trace file and output a CSV formatted
#file with the timestamp as the first column and subsequent vehicle
#data keys as separate columns in undefined order.

#TODO: This implementation is dead simple -- it will read through the
#tracefile once to identify all unique keys and build a dictionary
#mapping key names to column numbers.  It will then loop back through
#the file to generate the CSV.

#The next iteration will speculatively
#read in some number of seconds of the tracefile and speculatively
#assume that we have picked up all unique keys.  If it encounters
#another unique key after the speculative execution period, it can
#default back to the correct two file read implementation.

#Assumptions: each JSON object has a unique timestamp.
import json
import sys

#csv_row returns a string with the value formatted in correct csv
#order.
def csv_row(timestamp, key, value, column_map):
    #Determine which column the key is in
    column_num = column_map[key]

    #print "Column num of " + key + " is " + str(column_num)

    #Timestamp is always column 0
    ret_string = "%.3f" % timestamp + ","
    for i in range(1, len(column_map) + 1):
        if (i == column_num):
            #Place the value in the correct column
            #print str(value) + ","
            ret_string += str(value) + ","
        else:
            ret_string += ','

    #print "DEBUG: " + ret_string
    return ret_string

def main():
    if len(sys.argv) < 3:
        sys.exit("Specify name of both an input file and an output file")

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    current_column = 1 #The current column number. Column 0 is timestamp
    column_map = {}

    #Open the input file and loop through
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if not line.rstrip() : continue
            try:
                obj = json.loads(line)
            except ValueError:
                print("Skipping invalid JSON: %s" % line)
                continue
            if not obj['name'] in column_map:
                column_map[obj['name']] = current_column
                current_column += 1

    #print column_map

    #Open the input file and loop through a second time
    with open(input_file_name, 'r') as input_file,\
            open(output_file_name, 'w') as output_file:
        #Print a header for the output file specifying column values
        output_file.write("#timestamp," +\
                              ','.join(sorted(column_map, key = column_map.get))\
                              + "\n")
        for line in input_file:
            if not line.rstrip() : continue
            try:
                obj = json.loads(line)
            except ValueError:
                print("Skipping invalid JSON: %s" % line)
                continue
            output_file.write(csv_row(obj['timestamp'],\
                                          obj['name'],\
                                          obj['value'],\
                                          column_map) + "\n")

if __name__ == "__main__":
    main()
