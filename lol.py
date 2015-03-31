import urllib2
import urllib
import re
import json
from decimal import *

def hit_url_data(url, data):
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)	
    res_page = response.read()
    return res_page

def hit_url_simple(url):
    res_page = urllib2.urlopen(url).read()	
    return res_page

url_championList = "https://na.api.pvp.net/api/lol/na/v1.2/champion?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"
url_championName_prefix = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
url_championName_suffix = "?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"
url_currentPlayers_prefix = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/"
url_currentPlayers_suffix = "?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"
url_playerStat_prefix = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"
url_playerStat_suffix = "/recent?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"
url_championInfo_prefix = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
url_championInfo_suffix = "?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"
url_sumonnerId_prefix = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"
url_summonerId_suffix = "?api_key=b7a22f82-b9d6-491a-9f10-b4446e228fa4"


mySummonerId = 43310476

TS =  [12, 32, 432, 53, 201, 36, 89, 117, 54, 58, 267, 33, 111, 113, 27, 98, 72, 16, 44, 412, 48, 77, 106, 154]

def getSummonerId(summonerName):
    url_summonerId = url_sumonnerId_prefix + summonerName + url_sumonnerId_suffix
    response = hit_url_simple(url_summonerId)
    info = json.loads(response)
    return info['id']

def getChampionList():
    response = hit_url_simple(url_championList)
    champions = json.loads(response)['champions']
    championList = []
    for champion in champions:
        championList.append(champion["id"])

    for i in range(0, len(championList)):                
        url_championName = url_championName_prefix + str(championList[i]) + url_championName_suffix
        res = hit_url_simple(url_championName)
        raw = json.loads(res)
        print  raw['name'] + "\t" + str(championList[i])

def getChampionName(championId):
    url_championInfo = url_championInfo_prefix + str(championId) + url_championInfo_suffix
    response = hit_url_simple(url_championInfo)
    info = json.loads(response)
    return info['name']

def isTS(cid):
    if cid in TS:
        return True
    else:
        return False

def score(cid, minionsKilled, championsKilled, numDeaths, killingSprees, timePlayed, win):
    k_per_d = round(Decimal(championsKilled) / Decimal(numDeaths), 2)
   # print k_per_d
    (a, b, c, d, e) = (1.0, 1.0, 1.0, 1.0, 1.0)
   # print cid, minionsKilled, championsKilled, numDeaths, killingSprees, timePlayed, win
    if isTS(cid):
       (a, b, c) = (2.0, 2.0, 1.2)
    if k_per_d > 1.5 and win == False:
        d = 1.2
    if k_per_d < 0.8 and isTS(cid) == False:
        e = 0.5
    balance = [a, b, c, d, e]    
   # print balance
    add1 = minionsKilled / timePlayed / 2.8 * 20 * balance[0]
    if add1 > 20:
        add1 = 20
    add2 = championsKilled / timePlayed / 0.8 * 25 * balance[1]
    if add2 > 25:
        add2 = 25
    add3 = k_per_d / 2.0 * 45 * balance[2] * balance[3] * balance[4]
    if add3 > 45:
        add3 = 45
    add4 = killingSprees * 2.5
    if add4 > 10:
        add4 = 10    
#    print add1, add2, add3, add4     
    return round(add1 +  + add2 +  add3 + add4, 2)

#print score(77.0, 30.0, 16.0, 10.0, 4.0, 28.0, False)

def getCurrentGamePlayers(summonerId):
    url_currentGamePlayers = url_currentPlayers_prefix + str(summonerId) + url_currentPlayers_suffix
    response = hit_url_simple(url_currentGamePlayers)
    players = json.loads(response)['participants']
    playersInfo = []
    for player in players:
        playerInfo.append((player['teamId'], player['championId'], player['summonerName'], player['summonerId']))
    return playersInfo
    
def getPlayerStatics(summonerId):
    url_playerStat = url_playerStat_prefix + str(summonerId) + url_playerStat_suffix
    response = hit_url_simple(url_playerStat)
    games = json.loads(response)['games']
    statsList = []
    for game in games:
        if game['gameMode'] == 'ARAM':
            stats = game['stats']
            ks = 0
            if 'killingSpree' in stats:
                ks = stats['killingSpree']
            statsList.append((game['championId'], stats['minionsKilled'], stats['championsKilled'], stats['numDeaths'], ks, round(stats['timePlayed']/60), stats['win']))
    return statsList

def showPlayerScores(statsList):
    for stat in statsList:
#        print score(stat[0], stat[1], stat[2], stat[3], stat[4], stat[5], stat[6])
        return score(stat[0], stat[1], stat[2], stat[3], stat[4], stat[5], stat[6])

mySummonerId = 43310476
players = getCurrentGamePlayers(mySummonerId)
team1 = []
team2 = []
for player in players:
    if player['teamId'] == 100:
        team1.append(('team1: ', player['summonerName'], getChampionName(player['championId']), scores = showPlayerScores(getPlayerStatics(player['summonerId'])))
    else:
        team2.append(('team2: ', player['summonerName'], getChampionName(player['championId']), scores = showPlayerScores(getPlayerStatics(player['summonerId'])))
                              
for team in team1:
    print team

print '-----------------------------'

for team in team2:
    print team






