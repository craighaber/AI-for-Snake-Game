#This script formats the "GAdata.txt" file (created by trainGeneticAlgorithm.py) as a .csv file named "clean_ga_data.csv"
#Note: make sure "GAdata.txt" is named exactly that and is in the same directory as this script
#Note: if "clean_ga_data.csv" already exists in this directory it will be overwritten

import csv

ga_data = open("GAdata.txt", "r")

clean_ga_data = open("clean_ga_data.csv", "w")

csv_writer = csv.writer(clean_ga_data)
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
clean_ga_data.close()