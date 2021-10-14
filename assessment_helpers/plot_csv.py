#This script uses seaborn to plot "ga_data.csv" (aka the output from to_csv.py)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_filename", nargs='?', type=str, default="../ga_data.csv")
    parser.add_argument("--figure_filename", nargs='?', type=str, default="")
    args = parser.parse_args()
    
    sns.set_theme(color_codes=True)
    
    plotData = pd.read_csv(args.csv_filename)
    #ax = sns.regplot(x="Generation", y="Best Fitness", data=plotData)
    #ax = sns.regplot(x="Generation", y="Average Fitness", data=plotData)
    ax = sns.regplot(x="Generation", y="Average Score", data=plotData)
    plt.show()
    
    if (args.figure_filename):
        plt.savefig(args.figure_filename)