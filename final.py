# //////////////////////////////// Try to collect API data /////////////////////////////////
import csv
import requests
import json

RANK_LENGTH = 100

# Below is csv manipulation process
Netflix_File = open("BestMoviesNetflix.csv")
netflix_reader = csv.reader(Netflix_File)
Raw_File = open("raw_titles.csv")
raw_reader = csv.reader(Raw_File)

ROWS = []
for row in netflix_reader:
    ROWS.append(row)
ROWS.pop(0)
# Find top ranking 100 movie names
TOP_100_NAME = []
for i in range(RANK_LENGTH):
    TOP_100_NAME.append(ROWS[i][0])
# print(TOP_100_NAME) # This is used for testing

# Below is to stop requesting for existing data
open_json = open('DataCache.json','r')
json_content = open_json.read()
# print(type(json_content)) # This is for testing
json_list_of_dict = json.loads(json_content)
# print(type(json_list_of_dict)) # This is for testing
open_json.close()

# Below is API request and manipulation process
BASE_URL = 'http://www.omdbapi.com/?apikey=211f3137&t='
data_cache = []
EXIST = False
for name in TOP_100_NAME:
    for song in json_list_of_dict:
        try:
            if song["Title"] == name:
                EXIST = True
        except: EXIST = False
    if EXIST == False:
        NAME_URL = name
        FULL_URL = BASE_URL + NAME_URL
        web_connection = requests.get(FULL_URL)
        # print("Web Connection Status: ",web_connection) # This is to check the connection status
        web_json = web_connection.json()
        # print(web_json) # This is used for testing
        data_cache.append(web_json)

# online data will be downloaded to a json file, a list of dictionaries
with open('DataCache.json','w') as f:
    f.write(json.dumps(data_cache,indent=2))
    f.close()

# Below is to define a class of tree for later use
class MOVIE_TREE():
    def __init__(self, json_dict="None", ranking="None", title="None",  year="None", child_left="None", child_right="None"):
        self.ranking = ranking
        self.child_left = child_left
        self.child_right = child_right
        try:
            self.title = json_dict["Title"]
            self.year = json_dict["Year"]
        except:
            self.title = title
            self.year = year

    def append_tree(self, new_movie):
        if new_movie.ranking > self.ranking:
            if self.child_right == "None":
                self.child_right = new_movie
            else:
                self.child_right.append_tree(new_movie)
        else:
            if self.child_left == "None":
                self.child_left = new_movie
            else:
                self.child_left.append_tree(new_movie)

# This function is used to print a tree in ranking order
def print_tree(movie_tree):
    if movie_tree.child_left != "None":
        print_tree(movie_tree.child_left)

    print_song_info(movie_tree)
    
    if movie_tree.child_right != "None":
        print_tree(movie_tree.child_right)
    else:
        return

# This function is used for testing tree generation correctness
def test_tree(movie_tree):
    print_song_info(movie_tree)
    if movie_tree.child_left != "None":
        test_tree(movie_tree.child_left)
    if movie_tree.child_right != "None":
        test_tree(movie_tree.child_right)


# This function prints class info
def print_song_info(movie):
    print("The Title is: ", movie.title)
    print("The Ranking is: ", movie.ranking)

VALID_MOVIE_LIST = []
for i in range(len(json_list_of_dict)):
    # print(json_list_of_dict[i]) # This is for testing
    try:
        NEWMOVIE = MOVIE_TREE(json_list_of_dict[i], i+1)
        # print_song_info(NEWMOVIE)
        VALID_MOVIE_LIST.append(NEWMOVIE)
    except:
        print("Song Not Found!")

tree_root = VALID_MOVIE_LIST[round(len(json_list_of_dict)/2)]
VALID_MOVIE_LIST.pop(round(len(json_list_of_dict)/2))

for movie in VALID_MOVIE_LIST:
    tree_root.append_tree(movie)

print_tree(tree_root)
# test_tree(tree_root)



# ////////////////////////////////////// Try To Scrape Data /////////////////////////////////////////
# import requests
# from bs4 import BeautifulSoup
# from itertools import cycle
# WEB_URL = 'https://www.artstation.com/channels/comic_art?sort_by=trending&dimension=2d'
# list_proxy = [
#                 'http://Username:Password@IP1:20000',
#                 'http://Username:Password@IP2:20000',
#                 'http://Username:Password@IP3:20000',
#                 'http://Username:Password@IP4:20000',
#               ]
# proxy_cycle = cycle(list_proxy)
# proxy = next(proxy_cycle)

# for i in range(1, 10):
#     proxy = next(proxy_cycle)
#     print(proxy)
#     proxies = {
#       "http": proxy,
#       "https":proxy
#     }
#     response = requests.get(WEB_URL, proxies=proxies)
#     print(response)

# soup = BeautifulSoup(response.text, 'html5lib')
# print(soup.prettify())
# print(soup.find(class_='wrapper'))

# picture_parent = soup.find('div', class_='gallery-grid size-large ng-trigger ng-trigger-animateBlocks')
# print(type(picture_parent))
# picture_items = picture_parent.find_all('projects-list-item', recursive=False)
# for picture_item in picture_items:
#     image = picture_item.find('img')
#     image_name = image['alt']
#     print("Name is: "+image_name)


# /////////////////////////////////////// Try to API data /////////////////////////////////////////////
# import requests

# url = "https://www.artstation.com/artwork/8w8LVm"

# headers = {
#     'X-RapidAPI-Key': '2a7a5b7057msh6a6e2e07c32057ep11dc0djsn53bf2c8c0307',
#     'X-RapidAPI-Host': 'artstation.p.rapidapi.com'
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)


# //////////////////////////////// Try Spotify ///////////////////////////////////
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])


