import urllib2, xml.etree.ElementTree as ET, datetime, string, sys

def convertTime(strT):
	time = string.atoi(strT)
	result = ""
	hours = time/3600
	result = result + str(hours) + ":"
	minutes = (time - 60*hours)/60
	seconds = (time - 60*hours)%60
	result = result + str(minutes) + ":" + str(seconds)
	return result

def statPerMin(strT, stat):
    time = string.atoi(strT)
    hours = time/3600
    minutes = (time - 60*hours)/60
    return str(string.atoi(stat)/minutes)
    
#get my steam api key from a storage file
keyFile = open('text_files/apikey.txt', 'r')
apikey = keyFile.readline() #needed to access the steam servers to retrieve the info
keyFile.close()

#get my steam account # and dota 2 account # from a storage file
steamInfoFile = open('text_files/steamid.txt', 'r')
steamInfoFile.readline()
steamAccountNumber = steamInfoFile.readline() #needed to return a list of my most recent matches
steamInfoFile.readline()
dotaAccountNumber = steamInfoFile.readline() #needed to search for me in specific matches
steamInfoFile.close()

#list of match IDs and match dates that we want to process
idList = []
dateList = []

#create a dictionary that stores the indices associated with each game type
gameDictionary = {'1': "All Pick", '2': "Captains Mode", '3': "Random Draft", '4': "Single Draft", '5': "All Random", '6': "?? INTRO/DEATH ??", '7': "Greeviling", '8': "Reverse Captains Mode", '9': "Greeviling", '10': "Tutorial", '11': "Mid Only", '12': "Least Played", '13': "New Player Pool", '15': "Wraith Night" }

#open the hero IDs file
heroFile = open('text_files/heroesList.txt', 'r')
heroTree = ET.parse(heroFile)
heroRoot = heroTree.getroot()
heroFile.close()

#create a dictionary for all hero names
heroDictionary = {}
for hero in heroRoot.iter('hero'):
	heroDictionary[hero.find('id').text] = hero.find('localized_name').text
heroDictionary['0'] = 'ABANDON' #add an extra hero that indicates if a player abandoned

#loop to do all processing on the match
'''
This loop will go through each match that I have saved and get the details of that match.
It will find me in the file and then it will find the hero I played, my K-D-A, my level at the end of the match
and whether I won or not.
It will compose all of that information into a single string and then write it to a file
'''
xmlTree = ET.parse("matches/" + sys.argv[1])
treeRoot = xmlTree.getroot()
for player in treeRoot.iter('player'):
    date = datetime.datetime.fromtimestamp(int(treeRoot.find('start_time').text)).strftime('%Y-%m-%d %H:%M:%S')
    playID = player.find('account_id').text
    if playID == dotaAccountNumber:
        writeString = "Match on " + date + " ID: " + treeRoot.find('match_id').text + "\nGame Mode: " + gameDictionary[treeRoot.find('game_mode').text] 
        writeString = writeString + "\n" + "Duration: " + convertTime(treeRoot.find('duration').text)
        writeString = writeString + "\n" + "First Blood at " + convertTime(treeRoot.find('first_blood_time').text)
        writeString = writeString + "\n-----------------------------------\n\tI played " + heroDictionary[player.find('hero_id').text]
        writeString = writeString + '\n\tLevel ' + player.find('level').text + ' with K-D-A: ' + player.find('kills').text + '-' 
        writeString = writeString + player.find('deaths').text + '-' + player.find('assists').text        
        writeString = writeString + '\n\tCreep Score: ' + player.find('last_hits').text + '-' + player.find('denies').text        
        writeString = writeString + '\n\tGPM: ' + player.find('gold_per_min').text + '\tXPM: ' + player.find('xp_per_min').text
        writeString = writeString + '\n\tEnding Gold: ' + player.find('gold').text
        writeString = writeString + '\n\tHero Damage: ' + player.find('hero_damage').text
        writeString = writeString + '\n\tDamage per min: ' + statPerMin(treeRoot.find('duration').text, player.find('hero_damage').text)
        writeString = writeString + '\n\tTower Damage: ' + player.find('tower_damage').text
        writeString = writeString + '\n\tHealing Done: ' + player.find('hero_healing').text
        if (player.find('player_slot').text == '128' or player.find('player_slot').text == '129' or player.find('player_slot').text == '130' or player.find('player_slot').text == '131' or player.find('player_slot').text == '132'):
			writeString = writeString + "\n\tTeam: Dire"
        else: 
			writeString = writeString + "\n\tTeam: Radiant"
        if treeRoot.find('radiant_win').text == 'false':
			writeString = writeString + "\n\tVictor: Dire\n"
        else:
			writeString = writeString + "\n\tVictor: Radiant\n"

#file that will hold the results of the match processing
matchDetailsFile = open("details/" + treeRoot.find('match_id').text + '_Details.txt', 'w')
matchDetailsFile.write(writeString)
matchDetailsFile.close()
exit()


