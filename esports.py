import requests
import json
import tls_client
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

requests = tls_client.Session(
    client_identifier="chrome112",
)

response1 = requests.get('https://api.prizepicks.com/projections')

prizepicks = response1.json()

request = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines")

underdog = request.json()



#underdog players name
udlist = []
pplist = []
#seperate list for matching ud names == prizepicks names
matchingnames = []

#looping over the array
for appearances in underdog["over_under_lines"]:
    #title is equal to players name/// using split method to only get first name
    underdog_title = ' '.join(appearances["over_under"]["title"].split()[1:2])
    #display stat is equal to prop// ex map 1 kills
    UDdisplay_stat = f"{appearances['over_under']['appearance_stat']['display_stat']}"
    #stat value is equal to the prop value ex 5.5 /// so on
    UDstat_value = f"{appearances['stat_value']}"
    #filter out names for esports only
    if UDdisplay_stat =='Kills on Map 1' or UDdisplay_stat == 'Kills on Map 1+2' or UDdisplay_stat== 'Kills in Game 1+2':
    #creating a dictionary
        uinfo = {"Name": underdog_title.lower(), "Stat": UDdisplay_stat, "Line": UDstat_value}
        udlist.append(uinfo)
#start if prizepicks//loop array
for included in prizepicks['included']:
    #get id we will match this later o
    PPname_id = included['id']
    #getting prizepicks prop name
    PPname = included['attributes']['name'] 
    #nested loop must go thru data
    for data1 in prizepicks['data']:
        #ppid will match this to id to get correct information
        PPid = data1['relationships']['new_player']['data']['id']
        #getting pp line //ex map 1-2 kills
        PPprop_value = data1['attributes']['line_score']
        #gettting value// ex 7.5 kills
        PPprop_type = data1['attributes']['stat_type']
        #filtering esports props only
        if PPname_id == PPid and PPprop_type == 'MAPS 1-2 Kills' or PPprop_type == 'Map 1 Kills':
            ppinfo ={"Name": PPname.lower(), "Stat": PPprop_type, "Line": PPprop_value}
            pplist.append(ppinfo)
for udn in udlist:
    for ppn in pplist:
        if udn["Name"] == ppn["Name"]:
            final = {"Name": udn["Name"] , "Stat": udn["Stat"],"Underdog->": udn["Line"], "Prizepicks->": ppn["Line"] }
            matchingnames.append(final)
            print(final)
