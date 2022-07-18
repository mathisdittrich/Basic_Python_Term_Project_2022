
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
# from StringIO import StringIO



################ Get Data ######################################################################

# read the data
Generell_Information = pd.read_csv('./Data/Player_Generell_Information.csv')
Stats = pd.read_csv('./Data/Player_Stats.csv')
Player_ID = pd.read_csv('./Data/Player_ID.csv')





################ Data preprocessing ############################################################

# add Rebound Column
Rebounds = Stats["ORB"] + Stats["DRB"]
Stats["Rebounds"] = Rebounds

# add Overall Column
Overall = Stats["Rebounds"] + Stats["PTS"] + 3*Stats["BLK"] + 2*Stats["AST"] + 3*Stats["STL"] + Stats["3P%"]/2 + Stats["FT%"]/10
normalized_Overall = (Overall-Overall.min())/(Overall.max()-Overall.min())*100
Stats["Overall"] = normalized_Overall



# take only iformation we need
Generell_Information = Generell_Information[["Name", "Position","Age", "Height", "Weight"]]
Stats = Stats[Stats["Season"] == "2021-22"] # only Stats from the season 2021/22
Stats = Stats[["Player", "G", "FG%", "3P%", "FT%", "AST", "TOV", "PTS", "Tm", "Rebounds", "STL", "BLK", "Overall"]]

# prepare to merge on Name column & merge data sets
Stats = Stats.rename({"Player": "Name"}, axis= "columns")
joint_Data = pd.merge(Generell_Information, Stats, on="Name", how = "right") # merge 

# prepare to merge on Name column & merge data sets
Player_ID = Player_ID[["DISPLAY_FIRST_LAST", "PERSON_ID"]]
Player_ID = Player_ID.rename({"DISPLAY_FIRST_LAST": "Name"}, axis= "columns")
joint_Data = pd.merge(joint_Data, Player_ID, on="Name", how = "inner") # merge 

print(joint_Data.head())

################ Card Visualisation #############################################################

def showCard(Name):

    # get the data from the row of the player
    Player = joint_Data[joint_Data["Name"] == Name]

    # prepare the card and settings
    my_image = Image.open("card.png") # load image
    image_editable = ImageDraw.Draw(my_image) # prepare for change
    font = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 20) # prepare Font
    font_two = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 50) # prepare Font
    font_three = ImageFont.truetype("./Roboto/Roboto-Black.ttf", 25) # prepare Font


    # design card
    streifen = Image.open("streifen.png")
    my_image.paste(streifen, (200, 300))
    my_image.paste(streifen, (405, 300))
    my_image.paste(streifen, (200, 450))
    my_image.paste(streifen, (405, 450))

    # print the stats of the player on the card
    for (index, values) in pd.DataFrame.iterrows(Player):
        print(values)

        
        # print name on the bottom
        image_editable.text((220, 630), values["Name"], (256, 256, 256), font = font_two)
        
        ### print generell information on the left upper corner
        # make the layout for the stats
        image_editable.text((210,120), "Team:", (0, 0, 0), font = font)
        image_editable.text((210,170), "Position:", (0, 0, 0), font = font)
        image_editable.text((210,220), "Height:", (0, 0, 0), font = font)
        # image_editable.text((200,270), "Weight:", (0, 0, 0), font = font)
        # print generell information of player
        image_editable.text((210,140), values["Tm"], (0, 0, 0), font = font)
        image_editable.text((210,190), values["Position"], (0, 0, 0), font = font)
        image_editable.text((210,240), str(values["Height"]), (0, 0, 0), font = font)
        # image_editable.text((200,290), str(values["Weight"]), (0, 0, 0), font = font)
        
        
        ### print stats below the foto
        # Points per Game
        image_editable.text((310,320), str(values["PTS"]), (0, 0, 0), font = font_three)
        image_editable.text((210,320), "Points:", (0, 0, 0), font = font_three)
        # Assists
        image_editable.text((310,395), str(values["AST"]), (0, 0, 0), font = font_three)
        image_editable.text((210,395), "AST:", (0, 0, 0), font = font_three)
        # 3er%
        image_editable.text((310,470), str(values["3P%"]), (0, 0, 0), font = font_three)
        image_editable.text((210,470), "3P%:", (0, 0, 0), font = font_three)
        # FT%
        image_editable.text((310,545), str(values["AST"]), (0, 0, 0), font = font_three)
        image_editable.text((210,545), "AST:", (0, 0, 0), font = font_three)
        # Rebounds
        image_editable.text((550,320), str(round((values["Rebounds"]),1)), (0, 0, 0), font = font_three)
        image_editable.text((420,320), "Rebounds:", (0, 0, 0), font = font_three)
        # Steals
        image_editable.text((550,395), str(values["STL"]), (0, 0, 0), font = font_three)
        image_editable.text((420,395), "Steals:", (0, 0, 0), font = font_three)
        # Blocks
        image_editable.text((550,470), str(values["BLK"]), (0, 0, 0), font = font_three)
        image_editable.text((420,470), "Blocks:", (0, 0, 0), font = font_three)
        # Overall
        image_editable.text((550,545), str(int(values["Overall"])), (0, 0, 0), font = font_three)
        image_editable.text((420,545), "Overall:", (0, 0, 0), font = font_three)





        if not math.isnan(values["PERSON_ID"]):
            url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + str(values["PERSON_ID"])  + ".png"
            print(url)
            my_image_two = getImage(url) 
            box = (280, 75, 620, 320)
            # my_image_three = my_image_two.crop(box)
            # my_image_three = my_image_two.crop((280, 75, 620, 320))
            my_image.paste(my_image_two, (335, 75))
       
        print(values)

    

    '''
    split_name = Name.split(' ')
    print(split_name)

    url = "https://nba-players.herokuapp.com/players/" + split_name[1] + "/" + split_name[0]
    my_image_two = getImage(url) 
    '''

    # save and print card
  
    my_image.save("result.png")
    plt.imshow(mpimg.imread('result.png'))
    plt.show()





######################## Function that gets Images from Google  #################################

def getImage(url):

    response = requests.get(url)
    im = Image.open(BytesIO(response.content))

    return im





########################  Main = Take Input and get Card #################################
'''
Example Names:
# LeBron James
# Kevin Durant
# Trae Young
# Bam Adebayo
# Chris Paul 
# Devin Booker 
# James Harden
# Paul George
# Klay Thompson
# Patty Mills
# Rudy Gobert

'''

Input = "Trae Young"
showCard(Input)






















'''
def getImage(Player):

    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://www.google.com/")

    box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    box.send_keys('giraffe')
    box.send_keys(Keys.ENTER)

    driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()





    from bs4 import BeautifulSoup
import urllib2
import re


def getImage(url):

    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    print(images)

'''