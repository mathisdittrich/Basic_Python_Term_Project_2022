
# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from PIL import Image, ImageFont, ImageDraw 



# read the data
Generell_Information = pd.read_csv('./Data/Player_Generell_Information.csv')
Stats = pd.read_csv('./Data/Player_Stats.csv')

################ Data preprocessing - Start ############################################################

# Generell Information
Generell_Information = Generell_Information[["Name", "Position","Age", "Height", "Weight"]]

# only Stats from the season 2021/22
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

################ Card Visualisation ############################################################

def showCard(Name):

    Player = joint_Data[joint_Data["Name"] == Name]

    my_image = Image.open("card.jpeg")

    image_editable = ImageDraw.Draw(my_image)

    for (index, values) in pd.DataFrame.iterrows(Player):
        image_editable.text((200,140), values["Name"], (0, 0, 0))
        image_editable.text((200,160), values["Tm"], (0, 0, 0))
        image_editable.text((200,180), values["Position"], (0, 0, 0))
        image_editable.text((200,200), str(values["Height"]), (0, 0, 0))
        image_editable.text((200,220), str(values["Weight"]), (0, 0, 0))
        image_editable.text((200,240), str(values["AST"]), (0, 0, 0))
       
        print(values)

    # display generell information
    # title_font = ImageFont.truetype('playfair/playfair-font.ttf', 200)
   

    my_image.save("result.jpg")

    plt.imshow(mpimg.imread('result.jpg'))
    plt.show()



Input = "Trae Young"


showCard(Input)




