'''Alpha version 1.1 Added sorting for rating'''

import requests
import json
import time

def main():
    
    queryList=[]
    run = True
    print('Enter a movie title to find similar movies you might like, or press "Enter" to quit the app.\n')
    
    while run:
        #print('Enter a movie title to find similar movies you might like, or press "Enter" to quit the app.\n')
        print("Movie you like: ", end="")
        movieInput = input()
        if movieInput=="":
            print("\nEnjoy your movies!")
            time.sleep(5)
            break
        print()
        
        # Initialize movie query.
        queryList.append(Suggester(movieInput))
        queryList[-1].setTastediveMovies()
        queryList[-1].extractMovieTitles()
        #print(trial.getSuggestionList())
        
        # Add IMDB rating.
        queryList[-1].setSuggestionDict()
        
        # Display suggestions with movie rating.
        queryList[-1].displaySuggestions()

        print()

''' The Suggester class initializes from a movie input. An instance of the class can be called to find similar movies
 as well as the rating for the similar movies. The class relies on the Taste Dive API and OMDB API which offer free
 keys for limited use. Bands and TV Shows can also be added as a search functionality in later versions.'''

class Suggester:
    
    ''' Class variables, change API keys to your own API keys that can be obtained for free'''
    tastediveURL__="https://tastedive.com/api/similar"
    tastediveKey__="363963-MovieSug-I9NNJU5GH"
    ombdURL__="http://www.omdbapi.com/"
    omdbKey__="f8a641aef"
    omdbID__="tt38961984"

    ''' Initialize an instance from a movie'''
    def __init__(self, movie):
        self.movie__=movie
        self.suggestionList__=[]
        self.suggestionDict__={}

    ''' set movie suggestion list'''
    def setTastediveMovies(self):
        parameters = {"q": self.movie__, "type": "movies", "limit": "5"}
        tastediveResponse = requests.get(self.tastediveURL__, parameters)
        self.tastediveResponse__ = json.loads(tastediveResponse.text)

    ''' scrape movie titles from a query to TasteDive '''
    def extractMovieTitles(self):
        returnList = []
        for item in self.tastediveResponse__["Similar"]["Results"]:
            self.suggestionList__.append(item["Name"])

    ''' return suggestionList for debugging '''
    def getSuggestionList(self):
        return self.suggestionList__

    ''' return suggestionDict for debugging '''
    def getSuggestionDict(self):
        return self.suggestionDict__

    ''' Display the movie suggestions and their related IMDB Rating from highest to lowest rated '''
    def displaySuggestions(self):
        titlesDict = self.suggestionDict__
        sortedTitlesDict = sorted(titlesDict.keys(), key= lambda a: (titlesDict[a], a), reverse=True) # Sort keys into a list based off of the imdb float ranking
        if len(sortedTitlesDict)!=0:
            count=0                          # Count only for display purposes
            for item in sortedTitlesDict:
                count+=1
                if titlesDict[item]!="N/A":
                    print(str(count) + ") " + item + "; IMDB Rating: " + titlesDict[item] + "/10")
                else:    # Format for movies with no rating
                    print(str(count) + ") " + item + "; IMDB Rating: " + titlesDict[item])
        else:
            print(self.movie__ + " was not found. Maybe it is too old, obscure, or mispelled?")
        
    ''' Query OMDB for a movie's information from a movie title '''
    def getMovieRating(self, movieTitle):
        parameters = {"i": self.omdbID__, "apikey": self.omdbKey__, "t": movieTitle, "type": "movie", "r": "json"}
        requestDict = requests.get(self.ombdURL__, parameters)
        return json.loads(requestDict.text)

    ''' Add key:value pair of each movie and its rating to the suggestionDict '''
    def setSuggestionDict(self):
        for movie in self.suggestionList__:
            requestDict = self.getMovieRating(movie)
            try:
                self.suggestionDict__[movie]=requestDict["imdbRating"]

            except:    # if imdb rating not available for some reason, catch the error and set rating to "N/A"
                self.suggestionDict__[movie]="N/A"   

if __name__=="__main__":
    main()
