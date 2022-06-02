import csv
import os
import pandas as pd
import numpy as np

from pathlib import Path


def extract_data(dir):
    input_folder = 'Circle_Files_Raw/' + dir
    output_folder = 'Circle_Files/' + dir
    for file in os.listdir(input_folder):
        output_filename = output_folder + file.split('.')[0] + '.csv'
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(input_folder + file, 'r') as inf, open(output_filename, 'w', newline='') as outf:
            csvreader = csv.reader(inf)
            edited_rows = []
            rows = []
            for row in csvreader:
                for circle in row:
                    for node in circle.split('\t')[1:]:
                        edited_rows.append(node)
                rows.append(edited_rows)
                edited_rows = []
            csvwriter = csv.writer(outf)
            csvwriter.writerows(rows)

def process_Edges(dir):
    input_folder = 'Edge_Files_Raw/' + dir
    output_folder = 'Edge_Files/' + dir
    headerList = ['SRC','DST']
    for file in os.listdir(input_folder):
        output_filename = output_folder + file.split('.')[0] + '.csv'
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(input_folder + file, 'r') as inf, open(output_filename, 'w', newline='') as outf:
            csvreader = csv.reader(inf)
            dWriter = csv.DictWriter(outf,delimiter=',',fieldnames=headerList)
            dWriter.writeheader()
            for row in csvreader:
                dWriter.writerow({'SRC': row[0].split(" ")[0], 'DST': row[0].split(" ")[1]})
        csvData = pd.read_csv(output_filename)
        csvData.sort_values(["SRC", "DST"], axis=0, ascending=[True,True], inplace=True)
        csvData.to_csv(output_filename)


datasets = ['Facebook/', 'Twitter/']
for dataset in datasets:
    extract_data(dataset)
    process_Edges(dataset)