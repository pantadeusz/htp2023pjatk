# This is the AI model that uses the data about water quality to predict next weeks

import csv
from itertools import islice



def read_training_data():
    # the data for model is taken from here:
    file_path = 'data/stavanger-randaberg-data.csv'
    data_rows = []
    # Open the CSV file
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        # Create a CSV reader object with tab as the delimiter
        reader = csv.reader(file, delimiter='\t')
        for row in islice(reader, 1, 2):
            print(row)
        # Skip the first three rows
        for row in islice(reader, 3, None):
            row = [ e.replace('"','').replace(',','.') for e in row ]
            row = [ (e if e != '<2' else 0.05) for e in row]
            row = [(e if e != '' else '-1.0') for e in row]
            row = [float(e) for e in row]
            data_rows = data_rows + [row]
    return data_rows


def main():
    """Run administrative tasks."""
    print (read_training_data())

if __name__ == '__main__':
    main()
