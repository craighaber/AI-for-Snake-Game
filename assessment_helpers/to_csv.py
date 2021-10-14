#This script formats the "GAdata.txt" file (created by trainGeneticAlgorithm.py) as a .csv file named "ga_data.csv"
#Note: make sure "GAdata.txt" is named exactly that and is in the same directory as this script
#Note: if "ga_data.csv" already exists in this directory it will be overwritten

import csv
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ga_data_filename", nargs='?', type=str, default="GAdata.txt")
    parser.add_argument("--output_filename", nargs='?', type=str, default="ga_data.csv")
    args = parser.parse_args()

    ga_data = open(args.ga_data_filename, "r")

    output_ext = os.path.splitext(args.output_filename)[1]

    if(output_ext != ".csv"):
        raise Exception("output file must be a .csv")

    csv_ga_data = open(args.output_filename, "w")

    csv_writer = csv.writer(csv_ga_data)
    csv_writer.writerow(["Generation", "Best Fitness", "Average Fitness", "Average Score"])

    line = ga_data.readline()

    while(line):
        if("Generation" in line):
            row = []
            
            split = line.split(" ")
            row.append(split[1].strip())
            
            line = ga_data.readline() # skip binary line
            
            line = ga_data.readline()
            split = line.split(" ")
            row.append(split[2].strip()) 
            
            line = ga_data.readline()
            split = line.split(" ")
            row.append(split[2].strip())
            
            line = ga_data.readline()
            split = line.split(" ")
            row.append(split[3].strip())
            
            csv_writer.writerow(row)
        line = ga_data.readline() #iterate

    ga_data.close()
    csv_ga_data.close()
