dota2Py
=======
This is a script I wrote in Python that processes match information from the game Dota 2.

The filename specified on line 7 is the name of a file that I retrieved previously that contains a list of my most recent 100 matches. This script opens that file, and three other files that are all necessary before the processing actually begins.

apikey.txt -- This file contains the api key given to me by Valve that allows me to retrieve data from their servers. 

steamid.txt -- This file contains my Steam account number and my Dota2 player account number. My Steam account number is needed to limit the search of matches to those that I participated in. My Dota2 player account number is needed to find myself in a specific match.

The file is of this form
steam account id
XXXXXXXX
dota2 player account id
XXXXXXXX

heroesList.txt -- This file contains a list of heroes in the game. This file is used to create a python dictionary of heroes of the form
heroId -> heroName

The first two files are included in this directory but the actual values of the IDs have been replaced with placeholder text that you can replace with your information.

Finally, the actual processing of match details extracts the hero I played, the date of the match, my K-D-A with that hero, and the level I was at the end of the match and writes it to a file.
