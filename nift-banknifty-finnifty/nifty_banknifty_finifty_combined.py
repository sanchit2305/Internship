import pandas as pd
import csv
import numpy as numpy


input_files = ['^NSEI.csv' , '^NSEBANK.csv' , 'NIFTY_FIN_SERVICE.NS.NIFTY_FIN_SERVICE.NS.csv']
output_file = 'nifty_banknifty_finnifty_combined.csv'

output = None
j = 0
for infile in input_files:
    with open(infile, 'r') as fh:
        if output:
            for i,l in enumerate(fh.readlines()):
                if j == 0:
                    j = j+1
                    output[i]='index'
                else:
                        output[i] = "{}{}".format(output[i],l)
        else:
                output = fh.readlines()

    with open(output_file, 'w') as fh:
        for line in output:
            fh.write(line)