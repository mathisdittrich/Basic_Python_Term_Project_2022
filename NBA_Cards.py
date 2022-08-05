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





##################################### Get Data #####################################

# read the data
general_information = pd.read_csv('./Data/Player_Generell_Information.csv')
stats = pd.read_csv('./Data/Player_Stats.csv')
player_id = pd.read_csv('./Data/Player_ID.csv')





##################################### Data Preprocessing #####################################

# fill empty cells with zeros 
# so that the overall score can be calculated for every player
stats.fillna(0, inplace=True)

# normalize special names to normal letters
# example = "Luka Dončić" to "Luka Doncic"
for i in range(len(stats["Player"])):
    stats["Player"][i] = str(unicodedata.normalize('NFKD', stats["Player"][i]).encode('ascii', 'ignore'))
    stats["Player"][i] = stats["Player"][i][2:len(stats["Player"][i])-1]

# add Rebound column
rebounds = stats["ORB"] + stats["DRB"]
stats["Rebounds"] = rebounds

# add Overall column
# the current MVP gets the score 99 xD
overall = stats["Rebounds"] + stats["PTS"] + 3*stats["BLK"] + 2*stats["AST"] + 3*stats["STL"] + stats["3P%"]*30 + stats["FG%"]*30 
normalized_overall = (overall-overall.min())/(overall.max()-overall.min())*100
stats["Overall"] = normalized_overall

# take only iformation we need
general_information = general_information[["Name", "Position","Age", "Height"]]
stats = stats[stats["Season"] == "2021-22"] # only stats from the season 2021/22
stats = stats[["Player", "FG%", "3P%", "AST", "TOV", "PTS", "Tm", "Rebounds", "STL", "BLK", "Overall"]]
player_id = player_id[["DISPLAY_FIRST_LAST", "PERSON_ID"]]





##################################### Merge Datasets & Store the final one #####################################

# prepare to merge on Name column & merge data sets
stats = stats.rename({"Player": "Name"}, axis= "columns")
final_data = pd.merge(general_information, stats, on="Name", how = "inner") # merge 

# prepare to merge on Name column & merge data sets
player_id = player_id.rename({"DISPLAY_FIRST_LAST": "Name"}, axis= "columns")
final_data = pd.merge(final_data, player_id, on="Name", how = "left") # merge 

# store final_data set as csv-file
os.makedirs('/Users/mathis/Desktop/UNI/SS2022/Basic_Python/Term_Project', exist_ok=True)  
final_data.to_csv('/Users/mathis/Desktop/UNI/SS2022/Basic_Python/Term_Project/final_data.csv')  





##################################### Save Required Card #####################################

def save_card(name):
    '''Generate an NBA Card of a given player
    
    Args:
        name: string of the name of the player we want to generate a card for
    
    Returns:
        image of the generated NBA card 
    '''

    # if input player is not in dataset - return empty card
    if (not name in final_data["Name"]):
        
        my_image =  Image.open("card.png") # load image
        font = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 20) # prepare Font
        image_editable = ImageDraw.Draw(my_image) # prepare for change
        image_editable.text((220, 630), "Player does not exist", (256, 256, 256), font = font)
        


    # print the stats of the player on the card
    for i in range(len(final_data)):
        if final_data["Name"][i] == name:

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
        
            # print name on the bottom
            if len(final_data["Name"][i]) < 14:
                image_editable.text((220, 630), final_data["Name"][i], (256, 256, 256), font = font_two)
            else:
                image_editable.text((220, 640), final_data["Name"][i], (256, 256, 256), font = font_four)
            

            ### print general information on the left upper corner ###
            # make the layout for the stats
            image_editable.text((210,120), "Team:", (0, 0, 0), font = font)
            image_editable.text((210,170), "Position:", (0, 0, 0), font = font)
            image_editable.text((210,220), "Height:", (0, 0, 0), font = font)
            # print general information of player
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

            
            # print image from URL via Player_ID
            # David Johnson had a Player_ID in the dataset, but is not a NBA_Player anymore, so that he has no Link on the website
            if not math.isnan(final_data["PERSON_ID"][i]) and final_data["Name"][i] != "David Johnson":
                url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + str(int(final_data["PERSON_ID"][i]))  + ".png"
                print(url)
                my_image_two = get_image(url) 
                my_image.paste(my_image_two, (335, 75))

            # ELSE: print image from bing search
            # there was an indexing problem with Armoni Brooks - only with him
            elif final_data["Name"][i] != "Armoni Brooks": 
                my_image_three = bing_get_image(name) 
                box = (265,200)
                my_image_three = my_image_three.resize(box) 
                my_image.paste(my_image_three, (335, 75))

            # save card
            my_image.save("all_players/"+final_data["Name"][i]+".png")
    
        

    return my_image





##################################### Functions that get Images from Web  #####################################

# for official images from NBA website
def get_image(url):
    '''get a photo from an URL
    
    Args:
        url: URL where image can be found
    
    Returns:
        image from the URL
    '''

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    return image

# for pictures from bing web search
def bing_get_image(query_string):
    '''get a photo from bing web search
    
    Args:
        query_string: string that will be searched for
    
    Returns:
        image from bing
    '''

    downloader.download(
        query_string,
        limit=1,
        output_dir='other_players',
        adult_filter_off=True,
        force_replace=False,
        timeout=60)
    
    # look in which format the picture was downlowded, so that the Image we want to open exists
    if path.exists("other_players/" + query_string + "/Image_1.jpg"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.jpg")
    elif path.exists("other_players/" + query_string + "/Image_1.jpeg"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.jpeg")
    elif path.exists("other_players/" + query_string + "/Image_1.png"):
        image_two = Image.open("other_players/" + query_string + "/Image_1.png")

    return image_two





##################################### Show Card #####################################

def show_card(card):
    '''show card that was generated with save_card(name)
    
    Args:
        card: card that was generated with the function save_card(name)
    '''

    card.save("result.png")
    plt.imshow(mpimg.imread('result.png'))
    plt.show()





##################################### Make a Folder with every Player #####################################

def save_all_cards():
    '''Generate a card for every player in the data set and store them in a folder

    Iteration through data set is split into 4 parts, because it takes a while and it is easier to fix bugs this way
    
    Returns:
        a folder with all NBA player cards
    '''

    # first 100 rows
    for i in range(0,100):
        name = final_data["Name"][i]
        print(name)
        save_card(name)
    
    # second 100 rows
    for i in range(101,200):
        name = final_data["Name"][i]
        print(name)
        save_card(name)

    # third 100 rows
    for i in range(201,300):
        name = final_data["Name"][i]
        print(name)
        save_card(name)
    
    # last rows
    for i in range(301,len(final_data)):
        name = final_data["Name"][i]
        print(name)
        save_card(name)
    
# save_all_cards()
# this takes a while - up to 10 minutes
# and all cards are already in the folder all_players





#####################################  Main = Take Input and Get Card #####################################

# you can get a card to every NBA-Player from the season 2021/22 
# if the player switched teams - a card for every team will be shown

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

#### write the name in the terminal or insert it directly in the code ###
nba_player = input("Enter your favourite NBA player: ")
#nba_player = "LeBron James"

show_card(save_card(nba_player))