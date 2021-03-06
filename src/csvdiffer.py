# pylint: disable=E1101
import sys
import argparse
import pandas as pd
import numpy as np

class CsvDiffer:
    def __init__(self, inputs):
        self.csvfile1 = inputs.csvfile1
        self.csvfile2 = inputs.csvfile2
        self.sep = inputs.sep
        self.file1_keycols = inputs.file1_keycols
        self.file2_keycols = inputs.file2_keycols
        self.outfile = inputs.outfile
        self.df1 = None
        self.df2 = None
        self.df1cols = None
        self.df2cols = None
    def csvdiffer(self):
        try:
            self.df1 = pd.read_csv(self.csvfile1, sep=self.sep, dtype="string")
            self.df1['ROWNUM'] = np.arange(self.df1.shape[0])
            self.df1cols = self.df1.columns
            if self.file1_keycols.strip(', ').isdigit():
                column_list = []
                for colnum in self.file1_keycols.strip().split(','):
                    column_list.append(int(colnum.strip()))
                self.df1['indexcol'] = self.df1[column_list].apply(tuple, axis=1)
                self.df1 = self.df1.set_index(['indexcol'])
            else:
                column_list = []
                for colstr in self.file1_keycols.strip().split(','):
                    column_list.append(colstr.strip())
                self.df1['indexcol'] = self.df1[column_list].apply(tuple, axis=1)
                self.df1 = self.df1.set_index(['indexcol'])
            self.df1.index = pd.MultiIndex.from_tuples([(ix[0], str(ix[1])) for ix in self.df1.index.tolist()])
            self.df1 = self.df1.sort_index()
        except IOError as e:
            print("Could not read file:", self.csvfile1)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error here:", sys.exc_info()[0])
            print(e)
        try:
            self.df2 = pd.read_csv(self.csvfile2, sep=self.sep,dtype="string")
            self.df2['ROWNUM'] = np.arange(self.df2.shape[0])
            self.df2cols = self.df2.columns
            if self.file2_keycols.strip(', ').isdigit():
                column_list = []
                for colnum in self.file2_keycols.strip().split(','):
                    column_list.append(int(colnum.strip()))
                self.df2['indexcol'] = self.df2[column_list].apply(tuple, axis=1)
                self.df2 = self.df2.set_index(['indexcol'])
            else:
                column_list = []
                for colstr in self.file2_keycols.strip().split(','):
                    column_list.append(colstr.strip())
                self.df2['indexcol'] = self.df2[column_list].apply(tuple, axis=1)
                self.df2 = self.df2.set_index(['indexcol'])
            self.df2.index = pd.MultiIndex.from_tuples([(ix[0], str(ix[1])) for ix in self.df2.index.tolist()])
            self.df2 = self.df2.sort_index()
        except IOError as e:
            print("Could not read file:", self.csvfile2)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error here:", sys.exc_info()[0])
            print(e)
        self.diffFrames()
    def diffFrames(self):
        print("Starting the diff")
        counter = 0
        colnames = self.df1.columns
        idx1 = self.df1.index
        idx2 = self.df2.index
        idxunion = idx1.union(idx2)
        ignoreColumns = ['ROWNUM']
        for index in idxunion:
            try:
                leftfilerow = [self.csvfile1,str(self.df1.loc[index,'ROWNUM'])]
            except KeyError as kerror:
                leftfilerow = [self.csvfile1,'Missing']
            except Exception as exception:
                leftfilerow = [self.csvfile1,'Missing']
            try:
                rightfilerow = [self.csvfile2,str(self.df2.loc[index,'ROWNUM'])]
            except KeyError as kerror:
                rightfilerow = [self.csvfile2,'Missing']
            except Exception as exception:
                rightfilerow = [self.csvfile2,'Missing']
            mismatchFound = False
            leftLineMissing = False
            rightLineMissing = False
            for col in colnames[:-1]:
                if col in ignoreColumns:
                    continue
                try:
                    leftword = self.df1.loc[index,col]
                except KeyError as kerror:
                    leftword = ""
                    leftLineMissing = True
                except Exception as exception:
                    leftword = ""
                    leftLineMissing = True
                    print("Exception: {}".format(type(exception).__name__))
                    print("Exception message: {}".format(exception))
                try:
                    rightword = self.df2.loc[index, col]
                except KeyError as kerror:
                    rightword = ""
                    rightLineMissing = True
                except Exception as exception:
                    rightword = ""
                    rightLineMissing = True
                if(leftLineMissing and not(rightLineMissing)):
                    mismatchFound = True
                elif((not leftLineMissing) and rightLineMissing):
                    mismatchFound = True

                if(not(pd.isnull(leftword) and pd.isnull(rightword))):
                    if(not isinstance(leftword, str)):
                        leftword = str(leftword)
                    if(not isinstance(rightword, str)):
                        rightword = str(rightword)
                    if(leftword != rightword and (not rightLineMissing) and (not leftLineMissing)):
                        leftfilerow.append("<<<"+leftword+">>>")
                        rightfilerow.append("<<<"+rightword+">>>")
                        mismatchFound = True
                    else:
                        leftfilerow.append(leftword)
                        rightfilerow.append(rightword)
            if(mismatchFound):
                print('---------------------------------------------------------------------------------------')
                print(','.join(leftfilerow))
                print(','.join(rightfilerow))
                print('Mismatch found')
                print('---------------------------------------------------------------------------------------')

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
