# SOLUTION WITH COMMENTS

import requests
# used for Application Program Interface (API) calls
from pymongo import MongoClient
# used for connection to the backend database
import os
# used for reading .env file
from dotenv import load_dotenv
# used for reading .env file
from pprint import pprint
# used to print results to the console
load_dotenv()
# used for reading .env file


class InitialSearch:
    # class for searching through existing and previously hosted exhibitions at the Cleveland Metropolitan Museum of Art (CMA)
    def __init__(self):
        # used to instantiate class with necessary variables
        self.keyword = ""
        # user defined keyword search
        self.exhibition_data = []
        # used to store the data generated from the /exhibitions CMA API endpoint
        self.highlight_id = ""
        # used to store the id of a user selected piece of art from the generated exhibitions
        self.highlight_options = {
            'culture': "",
            'technique': "",
            'type': "",
            'artist': "",
            'tags': []
        }
        # used to store metadata associated with the user selected highlight piece

    def get_initial_collection(self):
        # function to gather information about CMA exhibitions based off of user generated input
        url = 'https://openaccess-api.clevelandart.org/api/exhibitions'
        # API endpoint
        params = {
            'title': self.keyword,
            'limit': 50,
            'has_image': 1
        }
        # API parameters with some controlled by user and some predetermined by the function
        r = requests.get(url=url, params=params)
        # call to the API endpoint
        data = r.json()
        # serialization of data into JavaScript Object Notation (JSON) format
        for collection in data['data']:
            # loop to check that exhibition meets minimum criteria
            if collection['artworks'].__len__() > 8:
                # checks if exhibition holds at least eight pieces of artwork
                self.exhibition_data.append(collection)
                # if the exhibition has at least eight pieces of artwork the exhibition is added into the list of available options for the user to select from
        if self.exhibition_data.__len__() == 0:
            # check if the user search generated any exhibitions
            print("\nCast a Wider Search Net\n")
            # alerts the user that their search was too narrow and didn't generate any results
            return
            # opportunity for recursion

    def print_collection_data(self):
        # prints the exhibition information generated from the get_initial_collection() method to the console
        print(f"\nFound {self.exhibition_data.__len__()} Pieces\n")
        # prints the exhibition information to the console
        pprint(self.exhibition_data)
        # prints the exhibition information to the console

    def prompt_user(self):
        # prompts the user for a search term to generate exhibitions from
        user_search = input("\nEnter an exhibition search term:\n")
        # console input that accepts user determined input
        self.keyword = user_search.lower().strip()
        # standardizing of user input to eliminate extra whitespace and put the string to lowercase
        self.get_initial_collection()
        # calls the API endpoint via the get_initial_collection() method (see comments above for functionality)
        self.print_collection_data()
        # prints the data generated from the get_initial_collection() method to the console

    def get_artwork_metadata(self):
        # retrieves metadata about a specific piece of artwork from the CMA /artworks API endpoint from a user selected piece of art
        url = f"https://openaccess-api.clevelandart.org/api/artworks/{self.highlight_id}"
        # /artworks API endpoint
        r = requests.get(url=url)
        # calling of the API endpoint
        data = r.json()
        # serialization of data into JSON format
        info = data['data']
        # grabbing necessary nested data
        self.highlight_options = {
            # setting highlight options for the user
            'culture': info['culture'],
            # culture option i.e. Spanish / French / etc
            'technique': info['technique'],
            # technique used in the creation of the piece i.e. gelatin silver print
            'type': info['type'],
            # the type of art i.e. Photograph / Oil on Canvas / etc
            'artist': info['creators'][0]['description'].split("(")[0].strip(),
            # the name of the artist of the work of art
            'tags': info['artists_tags']
            # any tags associated with the creator of the work of art
        }

    def print_keywords(self):
        # prints the highlighted metadata generated from the get_artwork_metadata() method to the console
        print("\nYour highlighted item metadata is\n")
        # prints the highlighted metadata to the console
        pprint(self.highlight_options)
        # prints the highlighted metadata to the console

    def user_selects_art_piece(self):
        # prompts the user to select a single piece of art to 'highlight'
        selected_id = input(
            "\nEnter the specific id of a piece of art to create a custom collection:\n")
        # accepts a user determined id from the console input
        self.highlight_id = selected_id.strip()
        # strips away any trailing or leading whitespace from the input
        self.get_artwork_metadata()
        # gets metadata from the selected 'highlight' piece
        self.print_keywords()
        # prints the metadata to the console


class RelatedSearch:
    # class used to generate a customized exhibition based off of metadata generated from a user selected highlight piece from the InitialSearch class
    def __init__(self):
        # used to instantiate the initial class
        self.keyword = ''
        # keyword variable used to store information specified by the user from a highlight piece's metadata
        self.exhibition_name = ''
        # variable used to store the user specified name of their custom exhibition
        self.exhibition_data = []
        # variable used to store the exhibition data

    def get_related_artworks(self):
        # calls the /artworks endpoint of the CMA API to generate a custom collection of five pieces of art that contain an image
        url = "https://openaccess-api.clevelandart.org/api/artworks"
        # /artworks API endpoint
        params = {
            # API parameters, some specified by user, some predetermined
            'q': self.keyword,
            # search term specified by the user
            'has_image': 1,
            # ensuring that the exhibition only contains pieces of art with images
            'limit': 5
            # limiting the results to five pieces
        }
        r = requests.get(url=url, params=params)
        # calling the /artworks API endpoint
        data = r.json()
        # converting the API response to JSON format
        if data['info']['total'] < 5:
            # check to ensure that there are at least five pieces in the exhibition
            print('Not Enough Artwork Found for an Exhibition Cast a Wider Net')
            # prints an error message to the console
            return
            # early return statement to ensure further functionality doesn't ensure
        for artwork in data['data']:
            # loop to clean / remove unnecessary data from the response generated by the API endpoint
            self.exhibition_data.append({
                # appending only necessary data to the class' exhibition data variable
                'athena_id': artwork['id'],
                # setting the athena_id from the unique athena_id of the piece of art
                'accession_number': artwork['accession_number'],
                # setting the accession_number from the unique accession_number of the piece of art
                'tombstone': artwork['tombstone'],
                # setting the tombstone variable of the piece of art
                'image': artwork['images']['web']['url'],
                # setting the image variable to the url of the piece of art
                'criteria': self.keyword
                # setting the criteria variable to the search term specified by the user
            })

    def print_related_pieces(self):
        # prints the exhibition data generated from the get_related_artworks() method to the console
        print("\nYour custom exhibition\n")
        # prints the exhibition data to the console
        pprint(self.exhibition_data)
        # prints the exhibition data to the console

    def prompt_user(self):
        # prompts the user for search information from metadata generated by their selection of a specific piece of art which is called in the InitialSearch.print_related_pieces() method
        user_search = input(
            "\nEnter a piece of metadata from your highlighted item to find similar works\n")
        # prompt for a search term
        self.keyword = user_search.lower().strip()
        # removing any trailing or leading whitespace and standardizing input to lowercase characters
        self.get_related_artworks()
        # calling the get_related_artworks() method to generate a custom exhibition
        self.print_related_pieces()
        # printing the information to the console via the print_related_pieces() method

    def save_to_backend(self):
        # function to allow the user to save their custom exhibition for future reference
        client = MongoClient(os.environ.get('ATLAS_URI'))
        # creation of a client to interact with a MongoDB backend
        db = client[os.environ.get('DB_NAME')]
        # directs the client to use a specific database
        collection = db['community_exhibitions']
        # generates if doesn't exist already, or utilize the 'community_exhibitions' collection
        res = collection.insert_one({
            # inserts the exhibition to the database
            'name': self.exhibition_name,
            # names the exhibition based off of user input
            'artwork': self.exhibition_data
            # puts the exhibition artwork data into an array with a key of 'artwork'
        })
        print(
            f"\nYour exhibition has been saved with an id of {res.inserted_id}\n")
        # prints the unique identifier of the exhibition to the console

    def name_exhibition(self):
        # gives the user the option to save and name their custom exhibition to a persisted MongoDB Atlas database
        save = input("\nWish to save your exhibition (Y / N) ?\n")
        # prompt to ensure that the user wants to save the data
        if save.capitalize().strip() == "Y":
            # check if the user confirms
            name = input("What's your exhibition name?\n")
            # prompts the user to name their exhibition
            self.exhibition_name = name.strip()
            # removes any trailing or leading white space from the user input
            self.save_to_backend()
            # saves the custom exhibition to a 'community_exhibitions' collection in an ATLAS MongoDB


class Searches:
    # combines the classes above to allow the code to be called with one line
    def __init__(self):
        # instantiation of internal variables which will hold the functions based within the classes defined above
        self.initial_search = InitialSearch()
        # sets the initial search variable to an instance of the InitialSearch class
        self.related_search = RelatedSearch()
        # sets the related search variable to an instance of the RelatedSearch class

    def run(self):
        # function used to call all of the functionality
        self.initial_search.prompt_user()
        # calls the initial user prompt method within the InitialSearch class
        self.initial_search.user_selects_art_piece()
        # allows the user to select a unique piece of art 'highlight' piece
        self.related_search.prompt_user()
        # prompts the user for metadata to search for related pieces of art
        self.related_search.name_exhibition()
        # prompts the user to name and save their exhibition


Searches().run()
# calls the program
