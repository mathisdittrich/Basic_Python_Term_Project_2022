
# import libraries
from cmath import nan
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from PIL import Image, ImageFont, ImageDraw
import requests
import math
import os  
from bing_image_downloader import downloader
import unicodedata
import os.path
from os import path



################ Get Data ######################################################################

# read the data
Generell_Information = pd.read_csv('./Data/Player_Generell_Information.csv')
Stats = pd.read_csv('./Data/Player_Stats.csv')
player_id = pd.read_csv('./Data/Player_ID.csv')





################ Data preprocessing ############################################################

# fill empty cells with zeros 
# so that the overall score can be calculatet for every player
Stats.fillna(0, inplace=True)

# normalize special names to normal letters
# example = "Luka Dončić" to "Luka Doncic"
for i in range(len(Stats["Player"])):
    Stats["Player"][i] = str(unicodedata.normalize('NFKD', Stats["Player"][i]).encode('ascii', 'ignore'))
    Stats["Player"][i] = Stats["Player"][i][2:len(Stats["Player"][i])-1]

# add Rebound Column
Rebounds = Stats["ORB"] + Stats["DRB"]
Stats["Rebounds"] = Rebounds

# add Overall Column
Overall = Stats["Rebounds"] + Stats["PTS"] + 3*Stats["BLK"] + 2*Stats["AST"] + 3*Stats["STL"] + Stats["3P%"]*30 + Stats["FG%"]*30 
normalized_Overall = (Overall-Overall.min())/(Overall.max()-Overall.min())*100
Stats["Overall"] = normalized_Overall

# take only iformation we need
Generell_Information = Generell_Information[["Name", "Position","Age", "Height"]]
Stats = Stats[Stats["Season"] == "2021-22"] # only Stats from the season 2021/22
Stats = Stats[["Player", "FG%", "3P%", "AST", "TOV", "PTS", "Tm", "Rebounds", "STL", "BLK", "Overall"]]
player_id = player_id[["DISPLAY_FIRST_LAST", "PERSON_ID"]]






################ Merge Datasets & store the final one ############################################################

# prepare to merge on Name column & merge data sets
Stats = Stats.rename({"Player": "Name"}, axis= "columns")
final_data = pd.merge(Generell_Information, Stats, on="Name", how = "inner") # merge 


# prepare to merge on Name column & merge data sets
player_id = player_id.rename({"DISPLAY_FIRST_LAST": "Name"}, axis= "columns")
final_data = pd.merge(final_data, player_id, on="Name", how = "left") # merge 

#mask = final_data["Name"] != "David Johnson"
#final_data = final_data[mask]

# store final_data set as csv-file
os.makedirs('/Users/mathis/Desktop/UNI/SS2022/Basic_Python/Term_Project', exist_ok=True)  
final_data.to_csv('/Users/mathis/Desktop/UNI/SS2022/Basic_Python/Term_Project/final_data.csv')  




################ Card Visualisation #############################################################

def saveCard(Name):

    # print the stats of the player on the card
    for i in range(len(final_data)):
        if final_data["Name"][i] == Name:

            # prepare the card and settings
            my_image = Image.open("card.png") # load image
            image_editable = ImageDraw.Draw(my_image) # prepare for change
            font = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 20) # prepare Font
            font_two = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 50) # prepare Font
            font_three = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 25) # prepare Font
            font_four = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 35) # prepare Font


            # design card
            streifen = Image.open("streifen.png")
            my_image.paste(streifen, (200, 300))
            my_image.paste(streifen, (405, 300))
            my_image.paste(streifen, (200, 450))
            my_image.paste(streifen, (405, 450))
        
            print(final_data["Name"][i])

            # print name on the bottom
            if len(final_data["Name"][i]) < 16:    image_editable.text((220, 630), final_data["Name"][i], (256, 256, 256), font = font_two)
            else:   image_editable.text((220, 640), final_data["Name"][i], (256, 256, 256), font = font_four)
            
            ### print generell information on the left upper corner ###
            # make the layout for the stats
            image_editable.text((210,120), "Team:", (0, 0, 0), font = font)
            image_editable.text((210,170), "Position:", (0, 0, 0), font = font)
            image_editable.text((210,220), "Height:", (0, 0, 0), font = font)
            # print generell information of player
            image_editable.text((210,140), final_data["Tm"][i], (0, 0, 0), font = font)
            image_editable.text((210,190), final_data["Position"][i], (0, 0, 0), font = font)
            image_editable.text((210,240), str(final_data["Height"][i]), (0, 0, 0), font = font)
            
            
            ### print stats below the foto ####
            # Points per Game
            image_editable.text((310,320), str(final_data["PTS"][i]), (0, 0, 0), font = font_three)
            image_editable.text((210,320), "Points:", (0, 0, 0), font = font_three)
            # Assists
            image_editable.text((310,395), str(final_data["AST"][i]), (0, 0, 0), font = font_three)
            image_editable.text((210,395), "AST:", (0, 0, 0), font = font_three)
            # 3er%
            image_editable.text((310,470), str(final_data["3P%"][i]), (0, 0, 0), font = font_three)
            image_editable.text((210,470), "3P%:", (0, 0, 0), font = font_three)
            # FT%
            image_editable.text((310,545), str(final_data["FG%"][i]), (0, 0, 0), font = font_three)
            image_editable.text((210,545), "FG%:", (0, 0, 0), font = font_three)
            # Rebounds 
            # formated to the length
            if len(str(final_data["Rebounds"][i])) < 4:
                image_editable.text((420,320), "Rebounds:", (0, 0, 0), font = font_three)
                image_editable.text((550,320), str(round((final_data["Rebounds"][i]),1)), (0, 0, 0), font = font_three)
            else: 
                image_editable.text((420,320), "Reb:", (0, 0, 0), font = font_three)
                image_editable.text((535,320), str(round((final_data["Rebounds"][i]),1)), (0, 0, 0), font = font_three)

            # Steals
            image_editable.text((550,395), str(final_data["STL"][i]), (0, 0, 0), font = font_three)
            image_editable.text((420,395), "Steals:", (0, 0, 0), font = font_three)
            # Blocks
            image_editable.text((550,470), str(final_data["BLK"][i]), (0, 0, 0), font = font_three)
            image_editable.text((420,470), "Blocks:", (0, 0, 0), font = font_three)
            # Overall
            image_editable.text((550,545), str(int(final_data["Overall"][i])), (0, 0, 0), font = font_three)
            image_editable.text((420,545), "Overall:", (0, 0, 0), font = font_three)


            #if final_data["Name"][i] == "David Johnson":
            #    final_data["PERSON_ID"][i] = np.empty
            
            # print image from URL via Player_ID
            if not math.isnan(final_data["PERSON_ID"][i]) and final_data["Name"][i] != "David Johnson":
                url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + str(int(final_data["PERSON_ID"][i]))  + ".png"
                print(url)
                my_image_two = getImage(url) 
                my_image.paste(my_image_two, (335, 75))

            # ELSE: print image from bing search
            else: 
                my_image_three = bing_get_image(Name) # + " official picture"
                box = (265,200)
                my_image_three = my_image_three.resize(box) 
                my_image.paste(my_image_three, (335, 75))

            # save card
            my_image.save("all_players/"+final_data["Name"][i]+".png")
    
    return my_image

        



######################## Function that gets Images from Google  #################################

# for official images from website
def getImage(url):

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    return image


# for pictures from websearch
def bing_get_image(query_string):

    downloader.download(query_string, limit=1,  output_dir='other_players',
    adult_filter_off=True, force_replace=False, timeout=60)
    
    if path.exists( "other_players/" + query_string + "/Image_1.jpg"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.jpg")
    elif path.exists( "other_players/" + query_string + "/Image_1.jpeg"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.jpeg")
    elif path.exists( "other_players/" + query_string + "/Image_1.png"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.png")

    return image_two




######################## show card ########################################

def showCard(card):
    card.save("result.png")
    plt.imshow(mpimg.imread('result.png'))
    plt.show()





######################## Make a folder with every player ########################################

def saveAllCards():

    for i in range(len(final_data)):
        name = final_data["Name"][i]
        print(name)
        saveCard(name)

saveAllCards()


########################  Main = Take Input and get Card #################################
'''
Example Players:
# LeBron James
# Nikola Jokic
# Luka Doncic
# Kevin Durant
# Stephen Curry
# Trae Young
# Bam Adebayo
# Chris Paul 
# Devin Booker 
# James Harden
# Paul George
# Klay Thompson
# Patty Mills
# Rudy Gobert
# Draymond Green
# Al Horford
# Giannis Antetokounmpo
# Maxi Kleber
# Zach LaVine
# Kyle Lowry
# Donovan Mitchell
# D'Angelo Russell
# Russell Westbrook
# Steven Adams
# Kevin Love


'''

Input = "Kessler Edwards"
showCard(saveCard(Input))