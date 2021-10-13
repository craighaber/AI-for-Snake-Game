#This script uses seaborn to plot "clean_ga_data.csv" (aka the output from to_csv.py)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(color_codes=True)

plotData = pd.read_csv("clean_GA_Data.csv")

#ax = sns.regplot(x="Generation", y="Best Fitness", data=plotData)
#ax = sns.regplot(x="Generation", y="Average Fitness", data=plotData)
ax = sns.regplot(x="Generation", y="Average Score", data=plotData)
plt.show()
