import sys
import argparse


class CsvDiffer:
    def __init__(self, fileonename, filetwoname):
        self.fileonename = fileonename
        self.filetwoname = filetwoname

    def csvdiffer(self):
        try:
            foh = open(self.fileonename, "r")
        except IOError as e:
            print("Could not read file:", self.fileonename)
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
        try:
            fth = open(self.filetwoname, "r")
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
        parser.add_argument('csvfile1', type=str)
        parser.add_argument('csvfile2', type=str)
        inputs = parser.parse_args()
        print(inputs.csvfile1)
        print(inputs.csvfile2)
        print(inputs.outfile)
        print(inputs.sep)
    except Exception as e:  # handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    main()
