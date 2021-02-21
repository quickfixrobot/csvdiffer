# pylint: disable=E1101
import sys
import argparse
import pandas as pd
import numpy as np
'''
            #df1 = df1.astype('str')
            #df1.set_index(['productno', 'productname'], inplace=True)
            #df1.set_index([1, 2], inplace=True)
            #df1 = pd.MultiIndex.from_frame(df1, names=['productno', 'productname'])
'''

class CsvDiffer:
    def __init__(self, inputs):
        self.csvfile1 = inputs.csvfile1
        self.csvfile2 = inputs.csvfile2
        self.sep = inputs.sep
        self.file1_keycols = inputs.file1_keycols
        self.file2_keycols = inputs.file2_keycols
        self.outfile = inputs.outfile
    def csvdiffer(self):
        try:
            df1 = pd.read_csv(self.csvfile1, sep=self.sep,dtype="string")
            df1['ROWNUM'] = np.arange(df1.shape[0])
            if self.file1_keycols.strip(', ').isdigit():
                column_list = []
                for colnum in self.file1_keycols.strip().split(','):
                    column_list.append(int(colnum.strip()))
                df1.set_index(list(df1.columns[column_list]), inplace=True)
            else:
                column_list = []
                for colstr in self.file1_keycols.strip().split(','):
                    column_list.append(colstr.strip())
                df1.set_index(column_list, inplace=True)

            df1.index = pd.MultiIndex.from_tuples([(ix[0], str(ix[1])) for ix in df1.index.tolist()])
            df1.sort_index(inplace=True)
            print(df1.index)
            print(df1)
            print(df1.loc[('001', 'Apple')])
        except IOError as e:
            print("Could not read file:", self.csvfile1)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            print(e)
        try:
            df2 = pd.read_csv(self.csvfile2, sep=self.sep,dtype="string")
            if self.file2_keycols.strip(', ').isdigit():
                column_list = []
                for colnum in self.file2_keycols.strip().split(','):
                    column_list.append(int(colnum.strip()))
                df2.set_index(list(df2.columns[column_list]), inplace=True)
            else:
                column_list = []
                for colstr in self.file2_keycols.strip().split(','):
                    column_list.append(colstr.strip())
                df2.set_index(column_list, inplace=True)

            df2.index = pd.MultiIndex.from_tuples([(ix[0], str(ix[1])) for ix in df2.index.tolist()])
            df2.sort_index(inplace=True)
            print(df2.index)
            print(df2.loc[('001', 'Apple')])
        except IOError as e:
            print("Could not read file:", self.csvfile2)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            print(e)


def main():
    try:
        parser = argparse.ArgumentParser(description='Find the difference between csv files')
        parser.add_argument('-s', '--sep', action='store', type=str, help='Field separator for input csv files')
        parser.add_argument('-o', '--outfile', action='store', type=str, help='Output file after the csv comparison')
        parser.add_argument('-k', '--file1_keycols', action='store', type=str, help='key columns from inputfile1 for comparison to be given like "0,1" starting from 0')
        parser.add_argument('-c', '--file2_keycols', action='store', type=str, help='key columns from inputfile2 for comparison to be given like "0,1" starting from 0')
        parser.add_argument('csvfile1', type=str)
        parser.add_argument('csvfile2', type=str)
        inputs = parser.parse_args()
        print(inputs.csvfile1)
        print(inputs.csvfile2)
        print(inputs.outfile)
        print(inputs.file1_keycols)
        print(inputs.file2_keycols)
        print(inputs.sep)
        csvd = CsvDiffer(inputs)
        csvd.csvdiffer()
    except Exception as e:  # handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])
        print(e)


if __name__ == "__main__":
    main()
