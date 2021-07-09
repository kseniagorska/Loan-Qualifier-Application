# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data


def save_csv(csvpath, csvdata):
    """ 
    Writes the contents of `csvdata` to `csvpath` as a CSV file

    Args:
        csvpath (Path): The csv file path.
        csvdata (List): The list of data to be written into CSV
       
    Returns:
      None
    """

    # write CSV file (overwrites any existing file with same name)
    with open (csvpath, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in csvdata:
            csv_writer.writerow(row)
           