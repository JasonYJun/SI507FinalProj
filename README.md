# SI507FinalProj
No special packages are included in the project. All packages include:
import csv
import requests
import json
import re
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

Data Structure
I defined a new class called “MOVIE_TREE”, which can be connected to each other and become a tree that contained the movie information. The leaves were arranged in the order of the movie’s NETFLIX rating ranking. 

The interaction will be done by user input through command line prompts. 

Initially, the user need to decide how much movie will be put into the local data base to deliver the results later on. After deciding the scale of movie data, 4 user options will appear:
Firstly, user can type in “1” to activate the first function, which is a search function to search for information of a movie by its name. When user input a movie name, all relevant information including release year, director and plot will be feed back to the user. 
In addition, user can type in “2” to get a list of ranked movies that goes from the highest ranking to the lowest, each with specific movie information included. 
Moreover, user can type in 3 to find out what kind of plot keyword is the most attractive to the audience. More specifically,  the program will parse the “movie description” data in each movie, and find which words appear most often in high ranking movies. 
Lastly, user can type in “4” to receive a list of highest ranking directors who produced most high ranking films. 
