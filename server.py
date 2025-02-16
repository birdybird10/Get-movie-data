import zmq
import requests
import os
from dotenv import load_dotenv

# load env variable
load_dotenv()

# Create a ZeroMQ context
context = zmq.Context()

# create a socket and connect to client
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")


# request API movie data
def requestAPIData(api_key, movieTitle, movieYear):
    params = {"apikey": api_key, "t": movieTitle, "y": movieYear}
    api_reply = requests.get('http://www.omdbapi.com/?', params=params)
    receivedMovieData = api_reply.json()
    return receivedMovieData


def readRequest():
    while True:
        print("Get-movie-data microservice is listening and ready for requests...")
        print()
        # receive the data the client has requested
        requestedData = socket.recv()
        requestedData = requestedData.decode().split(',')

        # parse what the client sent over
        movieTitle = requestedData[0]
        movieYear = requestedData[1]
        requestType = requestedData[2].lower()

        # display the type of data the client requested
        print("The movie title the client wants to see data for is:", movieTitle)
        print("The release-year for the movie the client wants data on is:", movieYear)
        print("The type of data the client requested is:", requestType)
        print()

        # get data from the api
        api_key = os.environ.get("API_KEY")
        receivedMovieData = requestAPIData(api_key, movieTitle, movieYear)

        # send the type of data the client has requested
        if requestType == 'plot':
            print("Sending to the client the following info: ")
            print(receivedMovieData['Plot'])
            print()
            socket.send_string(receivedMovieData['Plot'])
        elif requestType == 'actors':
            # Sort the list of actors (had to strip each actor and add to a new list, 
            # then add the sorted version to a new list, then turn the list back into 
            # a string to be sent to client)
            data = receivedMovieData['Actors'].split(',')
            actorsList = []
            for actor in data:
                actorsList.append(actor.strip())
            sortedActorsList = sorted(actorsList)  # sort the list of actors alphabetically by first name
            newList = ', '.join(sortedActorsList)
            print("Sending to the client the following info: ")
            print(newList)
            print()
            socket.send_string(newList)
        elif requestType == 'rating':
            print("Sending to the client the following info: ")
            print(receivedMovieData['imdbRating'])
            print()
            socket.send_string(receivedMovieData['imdbRating'])


readRequest()
