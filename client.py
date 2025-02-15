import zmq

# Create a ZeroMQ context
context = zmq.Context()

# Create a socket and connect to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")  

while True:
    # Get input from user- movie title, release-year, and data choice (plot, actors list, or rating)
    movieTitle = input("Please enter the movie title: ")
    movieReleaseYear = input("Please enter the movie's release year: ")
    dataChoice = input("Enter 'plot' to receive the movie plot, 'actors' to receive a sorted list of the movie's "
                        "actors, or 'rating' to receive the rating of the movie: ")
    print()
    requested_data = movieTitle.lower() + "," + movieReleaseYear.lower().strip() + "," + dataChoice.lower().strip()

    # Send the requested data list
    socket.send_string(requested_data)

    # Receive movie data from the server
    movie_data = socket.recv().decode()
    print(movie_data)
    print()