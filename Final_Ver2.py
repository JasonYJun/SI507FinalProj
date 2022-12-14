import csv
import requests
import json

# Below is to define a class of tree for later use
class MOVIE_TREE():
    def __init__(self, json_dict="None", ranking="None", title="None",  year="None", plot="None", director="None", date="None", child_left="None", child_right="None"):
        self.ranking = ranking
        self.child_left = child_left
        self.child_right = child_right
        try:
            self.title = json_dict["Title"]
            self.year = json_dict["Year"]
            self.plot = json_dict["Plot"]
            self.director = json_dict["Director"]
            self.date = json_dict["Released"]
        except:
            self.title = title
            self.year = year
            self.plot = plot
            self.director = director
            self.date = date

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

    print_movie_info(movie_tree)
    
    if movie_tree.child_right != "None":
        print_tree(movie_tree.child_right)

    return

# This function is used for testing tree generation correctness
def test_tree(movie_tree):
    print_movie_info(movie_tree)
    if movie_tree.child_left != "None":
        test_tree(movie_tree.child_left)
    if movie_tree.child_right != "None":
        test_tree(movie_tree.child_right)


# This function prints class info
def print_movie_info(movie):
    print("The Ranking is: ", movie.ranking)
    print("The Title is: ", movie.title)
    print("The Director is: ", movie.director)
    print("The Release Date is: ", movie.date)
    print("The Plot is: ", movie.plot)
    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    # print("The plot type is: ", type(movie.plot)) # The type is string!


print("////////////////////////////////   Welcome to the Movie Data Base!   ////////////////////////////////")
print("Please enter the scale of the movie list: (Please input a value between 10 and 250)")
in_length = input()
if in_length.isdigit():
    RANK_LENGTH = int(in_length)
else:
    RANK_LENGTH = 50

# This global variable is to set the scale for the data base for the user
# RANK_LENGTH = 100

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
TOP_N_NAME = []
for i in range(RANK_LENGTH):
    TOP_N_NAME.append(ROWS[i][0])
# print(TOP_N_NAME) # This is used for testing

# ////////////////////////////////////     TOP_N_NAME verified     /////////////////////////////////////////////////

# Below is to stop requesting for existing data
open_json = open('DataCache.json','r')
try:
    json_content = open_json.read()
    # print(type(json_content)) # This is for testing
    json_list_of_dict = json.loads(json_content)
    # print(type(json_list_of_dict)) # This is for testing
except:
    json_list_of_dict = []
open_json.close()
# print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

# Below is API request and manipulation process
BASE_URL = 'http://www.omdbapi.com/?apikey=211f3137&t='
data_cache = []
VALID_MOVIE_LIST = []
EXIST = False
RANK = 1
# If the song already exist, then do not request again
for name in TOP_N_NAME:
    # print("Go!") # For testing
    EXIST = False
    for movie in json_list_of_dict:
        try:
            if movie["Title"] == name:
                EXIST = True
                NEWMOVIE = MOVIE_TREE(movie, RANK)
                VALID_MOVIE_LIST.append(NEWMOVIE)
                RANK += 1
                # print("already in json!")
        except: 
            pass
    if EXIST == False:
        # print("not in json!")
        NAME_URL = name
        FULL_URL = BASE_URL + NAME_URL
        web_connection = requests.get(FULL_URL)
        # print("Web Connection Status: ",web_connection) # This is to check the connection status
        web_json = web_connection.json()
        NEWMOVIE = MOVIE_TREE(web_json, RANK)
        VALID_MOVIE_LIST.append(NEWMOVIE)
        RANK += 1
        # print(web_json) # This is used for testing
        data_cache.append(web_json)

json_list_of_dict = json_list_of_dict + data_cache # This is important for the cache to constantly over writing with the new data and the old data combined
# print(json_list_of_dict) # For testing   # The list can be generated!

# online data will be downloaded to a json file, a list of dictionaries
with open('DataCache.json','w') as f:
    f.write(json.dumps(json_list_of_dict,indent=2))
    f.close()

# print(VALID_MOVIE_LIST[round(RANK_LENGTH/2)].title)
tree_root = VALID_MOVIE_LIST[round(RANK_LENGTH/2)]
VALID_MOVIE_LIST.pop(round(RANK_LENGTH/2))

for movie in VALID_MOVIE_LIST:
    tree_root.append_tree(movie)

# print_tree(tree_root)
# test_tree(tree_root)
# print(tree_root.title)

# /////////////////////////////////////////////////     above realize the top n movie function     ///////////////////////////////////////////////////////////////

# The following code will try to do a most popular plot keyword search
def get_total_plot(tree):
    plot_string = ""
    if tree.child_left != "None":
        plot_string = plot_string + get_total_plot(tree.child_left)
    
    if tree.plot != "None":
        plot_string = plot_string + tree.plot

    if tree.child_right != "None":
        plot_string = plot_string + get_total_plot(tree.child_right)

    return plot_string
    
total_plot = get_total_plot(tree_root)
# print(total_plot) # This is used to test whether all plot was put together
# print_movie_info(tree_root) # This is used to test whether the tree root has a plot attribute

# Prepare for string manipulatioin
import re
from nltk.corpus import stopwords
plot_none_punct = re.split('\W+',total_plot)
plot_none_punct.pop()
plot_none_sw = [word.lower() for word in plot_none_punct if not word.lower() in set(stopwords.words('english'))]

# print(plot_none_sw) # This is to test the new word list generation

def get_word_order(word_list):
    word_count={}
    for word in word_list:
        if word in word_count:
            word_count[word]+=1
        else:
            word_count[word]=1
    # print(word_count) # This is used to test word count
    sorted_plot = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = dict(sorted_plot)
    # to_sort=list(word_count.values())
    # to_sort.sort(reverse=True)
    # output=[]
    # for i in range(len(to_sort)):
    #     index = list(word_count.values()).index(to_sort[i])
    #     word_keys = word_count.keys()
    #     output.append((list(word_keys)[index]))
    # del word_count[list(word_keys)[index]]
    return sorted_dict

plot_word_order_dict = get_word_order(plot_none_sw)
# print(list(plot_word_order_dict.items())[:10]) # This is the top 10 keyword list

x_list = []
y_list = []
for i in range(5):
    x = list(plot_word_order_dict.items())[i][0]
    y = list(plot_word_order_dict.items())[i][1] 
    x_list.append(x)
    y_list.append(y)
# print(x_list) # This is used for testing x_list

import matplotlib.pyplot as plt
# plt.bar(plot_word_order_dict.keys(), plot_word_order_dict.values(), 2, color='g') # This is the first ploting test
plt.bar(x_list, y_list)
# plt.show() # This is to show the graph

# Director ranking
def get_total_direct(tree):
    direct_list = []
    if tree.child_left != "None":
        direct_list = direct_list + get_total_direct(tree.child_left)
    
    if tree.plot != "None":
        direct_list.append(tree.director) 

    if tree.child_right != "None":
        direct_list = direct_list + get_total_direct(tree.child_right)

    return direct_list
    
total_direct = get_total_direct(tree_root)
director_order = get_word_order(total_direct)
# print(list(director_order.items())[:10])

print("Your have the following options: ")
print("Please input '1' to start to search information of a specific movie.")
print("Please input '2' to view a top ",RANK_LENGTH," movie ranking list.")
print("Please input '3' to view a movie plot keyword ranking.")
print("Please input '4' to view a top director ranking list.")
print("Please enter 'quit' to exit.")

quit=False
while(quit == False):
    keyin = input()
    if keyin == "quit":
        quit = True
    else:
        if keyin == "1":
            print("Please enter the movie name: ")
            name = input()
            FULL_URL = BASE_URL + name
            web_connection = requests.get(FULL_URL)
            web_json = web_connection.json()
            # generate a movie_tree obj
            result_tree = MOVIE_TREE(web_json)
            print("We find the following result: ")
            print("The title is: ", result_tree.title)
            print("The release year is: ", result_tree.year)
            print("The director is: ", result_tree.director)
            print("The plot is: ", result_tree.plot)
        if keyin == "2":
            print_tree(tree_root)
        if keyin == "3":
            plt.show()
        if keyin == "4":
            direct_rank = list(director_order.items())[:10]
            print("Top Director from High to Low is: ")
            for i in direct_rank:
                print(i[0])
        print("")
        # print("////////////////////////////////   Welcome to the Movie Data Base!   ////////////////////////////////")
        print("Your have the following options: ")
        print("Please input '1' to start to search information of a specific movie.")
        print("Please input '2' to view a top ",RANK_LENGTH," movie ranking list.")
        print("Please input '3' to view a movie plot keyword ranking.")
        print("Please input '4' to view a top director ranking list.")
        print("Please enter 'quit' to exit.")
