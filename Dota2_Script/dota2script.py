import urllib2
import xml.etree.ElementTree as ET
import datetime
import string

#name of the files we will be working with
processFileName = 'matchFile2.txt'
dataFile = 'processing.txt'

#get my steam api key from a storage file
keyFile = open('apikey.txt', 'r')
apikey = keyFile.readline() #needed to access the steam servers to retrieve the info
keyFile.close()

#get my steam account # and dota 2 account # from a storage file
steamInfoFile = open('steamid.txt', 'r')
steamInfoFile.readline()
steamAccountNumber = steamInfoFile.readline() #needed to return a list of my most recent matches
steamInfoFile.readline()
dotaAccountNumber = steamInfoFile.readline() #needed to search for me in specific matches
steamInfoFile.close()

#open the file and then parse the XML contents
tree = ET.parse(processFileName)
root = tree.getroot()

#list of match IDs and match dates that we want to process
idList = []
dateList = []

#open the hero IDs file
heroFile = open('heroesList.txt', 'r')
heroTree = ET.parse(heroFile)
heroRoot = heroTree.getroot()
heroFile.close()

#create a dictionary for all hero names
heroDictionary = {}
for hero in heroRoot.iter('hero'):
	heroDictionary[hero.find('id').text] = hero.find('localized_name').text
heroDictionary['0'] = 'ABANDON' #add an extra hero that indicates if a player abandoned

#file that will hold the results of the match processing
matchDetailsFile = open('matchDetailsFile.txt', 'w') 

#get two lists of all dates and match ids that I have in storage
for match in root.iter('match'):
	idList.append(str(match.find('match_id').text))
	dateList.append(datetime.datetime.fromtimestamp(int(match.find('start_time').text)).strftime('%Y-%m-%d %H:%M:%S'))

#loop to do all processing on the matches
'''
This loop will go through each match that I have saved and get the details of that match.
It will find me in the file and then it will find the hero I played, my K-D-A, my level at the end of the match
and whether I won or not.
It will compose all of that information into a single string and then write it to a file
'''
for id, date in zip(idList, dateList): 
	resource = urllib2.urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?format=XML&key="+apikey+"&match_id="+id)
	html = resource.read()
	resource.close()
	file = open(dataFile, 'w') #temp file to store info we are working with
	file.write(html)
	file.close()
	xmlTree = ET.parse(dataFile)
	treeRoot = xmlTree.getroot()
	for player in treeRoot.iter('player'):
		if player.find('account_id').text == dotaAccountNumber:
			writeString = "Match on " + date + " ID: " + id + "\n\tI played " + heroDictionary[player.find('hero_id').text] 
			writeString = writeString + '\n\tLevel ' + player.find('level').text + ' with K-D-A: ' + player.find('kills').text + '-' 
			writeString = writeString + player.find('deaths').text + '-' + player.find('assists').text
			if string.atoi(player.find('player_slot').text) < 128 and treeRoot.find('radiant_win').text == 'false':
				writeString = writeString + "\n\tResult: LOSS\n------------------------------------\n"
			else: 
				writeString = writeString + "\n\tResult: WIN\n------------------------------------\n"
			matchDetailsFile.write(writeString)
	print "processing..."
matchDetailsFile.close()
exit()
			


