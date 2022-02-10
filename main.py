from bs4 import BeautifulSoup
import requests
import re
from termcolor import colored
from pyfiglet import Figlet


f = Figlet(font='standard')
print(colored(f.renderText('Halo Infinite Stat Tracker'), 'green'))
# Create a dictionary for player data.
player_data = {}

#player_profile = input("What player would you like to check stats for: ")
#print(player_profile)
url = "https://halotracker.com/halo-infinite/profile/xbl/FracTalFeaR/overview?experience=ranked&playlist=f7f30787-f607-436b-bdec-44c65bc2ecef"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
##print(soup.prettify())

# Find the span tag that has the player's rank in Solo/Duo Controller.
span_tag_rank = soup.find_all('span', {'class' : 'halo-highlighted-stat__label'})
player_rank = span_tag_rank[0].text
print("Rank: ", player_rank)
player_data['Rank'] = player_rank

# Find the span tag that has the player's CSR in Solo/Duo Controller.
span_tag_csr = soup.find_all('span', {'class' : 'halo-highlighted-stat__value'})
# Delete the CSR characters from the string, delete comma and convert CSR string value to int.
player_csr_string = span_tag_csr[0].text
player_csr = int(player_csr_string[:-3].replace(",", ""))
print("CSR: ", player_csr)
player_data['CSR'] = player_csr

# Find the div tag that has all the main stats from the player in Solo/Duo Controller.
div_tag_giant_stats = soup.find_all('div', {'class' : 'numbers'})
#print(div_tag_giant_stats[1].text)


# Loop through all the categories and initiliaze the keys with the categories.
for stat in div_tag_giant_stats:
    # Check if the category name is more than one word.
    if stat.text.split()[1].isalpha():
        # Add the first and second word.
        category = stat.text.split()[0] + " " + stat.text.split()[1]
        #print(category)
        # Add the category and stats to the player_data dictionary. Stats for two worded categories will always be the
        # third element.
        try:
            stat_number = int(stat.text.split()[2].replace(",", ""))
            player_data[category] = stat_number
        except ValueError:
            stat_number = float(stat.text.split()[2])
            player_data[category] = stat_number

       
    # Add the stats for the categories that consist of one word.
    else:
        category = stat.text.split()[0]
        #print(category)
        # Win percentage is the third element in the list
        if stat.text.split()[0] == 'Win':
            player_data[category] = stat.text.split()[2]
        else:
            player_data[category] = int(stat.text.split()[1].replace(",", ""))
print(player_data)

# Find the div tag that has all the accuracy stats from the player in Solo/Duo Controller.
div_tag_accuracy_stats = soup.find_all('div', {'class' : 'percentage-stat__details'})

# Add the shot accuracy stats to the player_data dictionary.
shot_accuracy_list = div_tag_accuracy_stats[0].text.split()
print(shot_accuracy_list)
player_data['Shot Accuracy'] = shot_accuracy_list[0]
shots_fired_string_name = shot_accuracy_list[1] + " " + shot_accuracy_list[2]
# Remove parentheses and comma from string and convert to int.
shots_fired_stat = int(re.sub("[(,)]", "", shot_accuracy_list[3]))
print(shots_fired_stat)
player_data[shots_fired_string_name] = shots_fired_stat

shots_hit_string_name = shot_accuracy_list[4] + " " + shot_accuracy_list[5]
# Remove parentheses and comma from string and convert to int.
shots_hit_stat = int(re.sub("[(,)]", "", shot_accuracy_list[6]))
print(shots_hit_stat)
player_data[shots_hit_string_name] = shots_hit_stat


# Add the headshot accuracy stats to the player_data dictionary.
headshot_accuracy_list = div_tag_accuracy_stats[1].text.split()
player_data['HS Accuracy'] = headshot_accuracy_list[0]


# Count the number of stat categories.
print("Number of stat categories: ", len(player_data))