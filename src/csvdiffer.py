# pylint: disable=E1101
import sys
import argparse


class CsvDiffer:
    def __init__(self, inputs):
        self.fileonename = inputs.csvfile1
        self.filetwoname = inputs.csvfile2
        self.sep = inputs.sep
        self.file1_keycols = inputs.file1_keycols
        self.file1_keycols = inputs.file2_keycols
        self.outfile = inputs.outfile
    def csvdiffer(self):
        try:
            foh = open(self.fileonename, "r")
            print("\n".join(foh.readlines()))
        except IOError as e:
            print("Could not read file:", self.fileonename)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
        try:
            fth = open(self.filetwoname, "r")
            print("\n".join(fth.readlines()))
        except IOError as e:
            print("Could not read file:", self.filetwoname)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:  # handle other exceptions such as attribute errors
            print("Unexpected error:", sys.exc_info()[0])


def main():
    try:
        parser = argparse.ArgumentParser(description='Find the difference between csv files')
        parser.add_argument('-s', '--sep', action='store', type=str, help='Field separator for input csv files')
        parser.add_argument('-o', '--outfile', action='store', type=str, help='Output file after the csv comparison')
        parser.add_argument('-k', '--file1_keycols', action='store', type=str, help='key columns from inputfile1 for comparison to be given like "2,3,4"')
        parser.add_argument('-c', '--file2_keycols', action='store', type=str, help='key columns from inputfile2 for comparison to be given like "2,3,4"')
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
