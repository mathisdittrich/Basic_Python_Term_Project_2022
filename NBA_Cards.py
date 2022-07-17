
# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# read the data
Generell_Information = pd.read_csv('./Data/Player_Generell_Information.csv')
Stats = pd.read_csv('./Data/Player_Stats.csv')

# Data preprocessing 
# Generell Information
Generell_Information = Generell_Information[["Name", "Position","Age", "Height"]]

# Stats 
Stats = Stats[Stats["Season"] == "2021-22"]

# add Rebound Column
Rebounds = Stats["ORB"] + Stats["DRB"]
Stats["Rebounds"] = Rebounds

# take only important Stats from Stats
Stats = Stats[["Player", "G", "FG%", "3P%", "FT%", "AST", "TOV", "PTS", "Tm"]]

# prepare to merge on Name column
Stats = Stats.rename({"Player": "Name"}, axis= "columns")

# merge 
joint_Data = pd.merge(Generell_Information, Stats, on="Name", how = "right")


print(joint_Data)