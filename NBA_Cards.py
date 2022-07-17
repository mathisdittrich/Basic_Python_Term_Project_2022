
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

# add Rebound Column
Rebounds = Stats["ORB"] + Stats["DRB"]
Stats["Rebounds"] = Rebounds

# take only iformation we need
Generell_Information = Generell_Information[["Name", "Position","Age", "Height", "Weight"]]
Stats = Stats[Stats["Season"] == "2021-22"] # only Stats from the season 2021/22
Stats = Stats[["Player", "G", "FG%", "3P%", "FT%", "AST", "TOV", "PTS", "Tm", "Rebounds"]]

# prepare to merge on Name column & merge data sets
Stats = Stats.rename({"Player": "Name"}, axis= "columns")
joint_Data = pd.merge(Generell_Information, Stats, on="Name", how = "right") # merge 

################ Card Visualisation ############################################################

def showCard(Name):

    # get the data from the row of the player
    Player = joint_Data[joint_Data["Name"] == Name]

    # prepare the card and settings
    my_image = Image.open("card.jpeg") # load image
    image_editable = ImageDraw.Draw(my_image) # prepare for change
    font = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 25) # prepare Font
    font_zwei = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 50) # prepare Font
    
    # make the layout for the stats
    image_editable.text((200,160), "Team:", (0, 0, 0), font = font)
    image_editable.text((200,200), "Position:", (0, 0, 0), font = font)
    image_editable.text((200,240), "Height:", (0, 0, 0), font = font)
    image_editable.text((200,280), "Weight:", (0, 0, 0), font = font)
    image_editable.text((200,320), "AST:", (0, 0, 0), font = font)

    # print the stats of the player on the card
    for (index, values) in pd.DataFrame.iterrows(Player):

        image_editable.text((220, 630), values["Name"], (256, 256, 256), font = font_zwei)
        image_editable.text((320,160), values["Tm"], (0, 0, 0), font = font)
        image_editable.text((320,200), values["Position"], (0, 0, 0), font = font)
        image_editable.text((320,240), str(values["Height"]), (0, 0, 0), font = font)
        image_editable.text((320,280), str(values["Weight"]), (0, 0, 0), font = font)
        image_editable.text((320,320), str(values["AST"]), (0, 0, 0), font = font)
       
        print(values)

    # display generell information
    # title_font = ImageFont.truetype('playfair/playfair-font.ttf', 200)
   

    my_image.save("result.jpg")

    plt.imshow(mpimg.imread('result.jpg'))
    plt.show()



Input = "Trae Young"


showCard(Input)


#########################################################







