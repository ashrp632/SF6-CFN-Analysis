import requests
import pandas as pd
import json
import os

def cfnRanks(key, character_id = 'luke', character_filter = '1', league_rank = '36', page_num = '1'):
    headers = {'Cookie': 'buckler_r_id=d4b73cd7-9371-423a-93b8-c2c07fca0d0b; buckler_id=sdCzchrDMI9MkaR_HD7KOkuCM4_F1srjp7kyjso6cf0iuDLTbDyCZIaP8UZdn7Oq; buckler_praise_date=1705501718562',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Host': 'www.streetfighter.com',}

    #These headers are required to access the URL when trying to make a get request. You can find these headers by inspecting
    #the browser. 

    urlToken = key #You can get this by going to en.json in network browser console and looking at the URL.
    characterID = character_id
    characterFilter = character_filter #1 doesn't specify a character and only goes by rank instead. 4 does specify a character, meaning you will only get data on that character.
    leagueRank = league_rank #This corresponds to master rank. 35 corresponds to diamond 5. 34 corresponds to diamond 4 and so on.
    pageNum = page_num #You will need pageNum in order to parse through multiple pages. These json docs only has the info of 20 players at a time.
    df = pd.DataFrame()
    dfLoc = pd.DataFrame()
    dfHome = pd.DataFrame()
    dfRanks = pd.DataFrame()
    #Initialize dataframe from pandas library

    url = 'https://www.streetfighter.com/6/buckler/_next/data/{}/en/ranking/league.json?character_filter={}&character_id={}&platform=1&user_status=1&home_filter=1&home_category_id=0&home_id=1&league_rank={}&page={}'.format(urlToken, characterFilter, characterID, leagueRank, pageNum)
    url3 = 'https://www.streetfighter.com/6/buckler/ranking/league'
    print(url)
    #url is a direct link to the json files. You can see in url1 that there are customizable options that you can fill the string
    #such as changing the character_id/filter, home platform, league_rank, page-number,and more. Changing this url or finding it on the
    #actual buckler website and inputting it here will give you more specified search results, such as the rankings of only diamond
    #users and more. Character_id attribute will not work unless character filter is 4. 

    #Url2 is the site that feeds off of the json. It requires a bit more searching in order to find the data.
    #This is all available by going to the website and inspecting through browser console.

    response = requests.get(url=url, headers = headers)
    jsonText = response.json()

    maxPages = jsonText['pageProps']['league_point_ranking']['total_page']
    maxPlayers = jsonText['pageProps']['league_point_ranking']['total_count']
    homeRegions = jsonText['pageProps']['home_category_id']
    regionLoc = jsonText['pageProps']['home_id']
    ranks = jsonText['pageProps']['league_rank']

    dfLoc = pd.concat([df, pd.json_normalize(regionLoc)])
    dfHome = pd.concat([df, pd.json_normalize(homeRegions)])
    dfRanks = pd.concat([df, pd.json_normalize(ranks)])

    print(maxPages)
    print(maxPlayers)

    maxPage = 2

    #This is the value of the page in the json doc. Making it a dynamic parameter here allows us to change the json doc players
    #to another page. This allows us to get 20 more players.

    while pageNum < maxPage:
        
        response = requests.get(url=url, headers = headers)
        jsonText = response.json()
        
    #If using URL1, you can instead collect the json directly using jsonText = response.json() afterwards without using beautiful soup.
    #When using URL2, you must inspect the elements in the browser console and find the json there. I will be using URL2
    #since the json is more updated over there. URL2 is also more readable than URL1, but less customizable.

    #response = response.text

    #soup = BeautifulSoup(response, 'html.parser')

    #file = soup.find('script', {'id': '__NEXT_DATA__'})
    #jsonText = json.loads(file.get_text())

    #We load the data from the site into a local variable here in json format. You can usually find json documents in the browser
    #console from application.json after finding the id as seen when in the script variable.


    #This is how many pages and players there are in total in the specifications when using url1. 
    #There are millions of players, so I suggest sectioning off or narrowing the scope if you don't want a huge CSV file.

        players = jsonText['pageProps']['league_point_ranking']['ranking_fighter_list']
    #This grabs the specific section of the json doc that we want to look at, which is player data.
    #Interestingly enough, 'props' does not appear when using URL1 so make sure to remove it when trying to grab page data.

        df = pd.concat([df, pd.json_normalize(players)])
    #We use the dataframe initialized earlier to put the json into dataframe format. We concatenate these frames together.

        df = df.loc[:, ['fighter_banner_info.personal_info.fighter_id',
                                        'character_name',
                                        'league_point',
                                        'fighter_banner_info.home_name',
                                        'fighter_banner_info.max_content_play_time.play_time'
                                        ]]
        df.to_csv('C:/Users/ashrp/Documents/SideProjects/master.csv', index=False, header=False)
        
        pageNum += 1

if __name__ == "__main__":
    urlToken = "8oIEgbWL-bru1udjO0sqL" #You can get this by going to en.json in network browser console and looking at the URL.
    characterID = 'luke'
    characterFilter = 1 #1 doesn't specify a character and only goes by rank instead. 4 does specify a character, meaning you will only get data on that character.
    leagueRank = 36 #This corresponds to master rank. 35 corresponds to diamond 5. 34 corresponds to diamond 4 and so on.
    pageNum = 1 
    cfnRanks(urlToken, characterID, characterFilter, leagueRank, pageNum)
