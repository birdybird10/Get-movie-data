# How to request data from the microservice:

A client must first create a ZeroMQ context, create a socket, and connect to the server:

context = zmq.Context()


socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5557")  

The request parameter for the microservice is a string containing 3 items separated by commas (no spaces). The string will contain the movie title, followed by the movie release-year, followed by the user’s data choice ('plot', 'actors', or 'rating'). An example request parameter is the following string:

“Moana,2016,plot”

Another example:

"Peter Pan,1953,actors"

After requesting the movie title, movie release-year, and data choice (plot, actors, or rating) from the user and connecting to the server via socket.connect("tcp://localhost:5557"), the movie title, release-year, and data choice string can be sent to the microservice in the request socket.send_string("movie title,movie release-year,data choice"). 
The input received via the server will be parsed out to use each part of the string, being title, release-year, and data choice.


# How to receive data from the microservice:

The data type provided by the microservice is a byte string containing movie data (either the plot, sorted actors list, or rating). The byte string can be read with socket.recv().decode(). An example call is:
movie_data = socket.recv().decode()

# UML Diagram:

![Screen Shot 2025-02-15 at 18 24 38 PM](https://github.com/user-attachments/assets/c5fce59b-1fdc-420e-b81e-82f5412e1a3c)




