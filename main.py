from email import header
import imp
from bs4 import BeautifulSoup
import requests
import re
from termcolor import colored
from pyfiglet import Figlet

# Import data manipulation modules
import pandas as pd
import numpy as np
# Import data visualization modules
import matplotlib as mpl
import matplotlib.pyplot as plt

from player_stats import *


f = Figlet(font='standard')
print(colored(f.renderText('Halo Infinite Stat Tracker'), 'green'))
# Create a dictionary for player data.
player_data = {}

# Get the number of players we want to compare stats.
num_of_players = int(input('How many players do you want to compare stats? '))
player_profile = []

# Get the player_profile for each player.
while num_of_players != 0:
    player_name = input('What player would you like to check stats for: ')
    player_profile.append(player_name)
    num_of_players -= 1

print(player_profile)
#player_profile = input("What player would you like to check stats for: ")

# For each player check if the player exists and get their stats.
for player in player_profile:
    soup = check_if_player_exist(player)
    # Search for the player name to have the dict show the correct player name when a incorrect player name is searched for. 
    span_tag_player_name = soup.find_all('span', {'class' : 'trn-ign__username'})
    player_name = span_tag_player_name[0].text
    player_data[player_name] = get_player_data(soup)

#print(player_data['FracTalFeaR'])
#print(player_data['thyHumanoid'])
'''
url = "https://halotracker.com/halo-infinite/profile/xbl/{}/overview?experience=ranked&playlist=f7f30787-f607-436b-bdec-44c65bc2ecef".format(player_profile)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Find the span tag that has the error code when searching for a player's name.
span_tag_error = soup.find_all('span', {'class' : 'lead'})
# Keep asking the user to input the correct player name.
while span_tag_error[0].text == 'Player Not Found':
    print('Player was not found. Please enter the correct player name. If you would like to exit type exit().')
    player_profile = input("What player would you like to check stats for: ")
    
    # Check to see if the user wants to exit the program.
    if player_profile == 'exit()':
        exit(0)
    url = "https://halotracker.com/halo-infinite/profile/xbl/{}/overview?experience=ranked&playlist=f7f30787-f607-436b-bdec-44c65bc2ecef".format(player_profile)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')   
    span_tag_error = soup.find_all('span', {'class' : 'lead'})

# Get the data from the player the user inputted. 
player_data = get_player_data(soup, player_data)
'''
print('player_data data type is', type(player_data))
column_headers = []
# Get all the keys that will make the column header for pandas.
for key, values in player_data.items():
    print(key, values)
    
#for key, value in player_data.items():
 #   print(type(key))
  #  column_headers.append(key)


# Create a DataFrame from our scraped data using index set to 0 to get the keys as columns.
data = pd.DataFrame(player_data, index=[0])
print(data.head())
print(data.columns)

# Select the categories we are going to graph.
categories = ['K/D Ratio', 'Win %', 'Shot Accuracy %', 'Avg. Damage', 'Damage Taken', 'Damage Dealt']
# Create data subset for radar chart. Additionally, we will add the player name and rank.
data_radar = data[['Name', 'Rank'] + categories]
print(data_radar.head())

data_radar_filtered = data_radar[data_radar['Shot Accuracy %'] > 45.0]
# Create columns with percentile rank
for i in categories:
    data_radar_filtered[i + '_Rank'] = data_radar_filtered[i].rank(pct=True)

# Flip the rank for damage taken
data_radar_filtered['Damage Taken_Rank'] = 1 - data_radar_filtered['Damage Taken_Rank']
print(data_radar_filtered.head())

labels = categories
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

fig = plt.figure(figsize=(6,6))
plt.suptitle('Halo Comparison')

# Count the number of stat categories.
print("Number of stat categories: ", len(player_data))


player_one = input('What is the name of the first player that has crypto? ')

# Check if the player profile exists.
soup = check_if_player_exist(player_one)
print(soup)
