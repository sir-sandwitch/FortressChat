import json
import os
import requests as req
import flask
import datetime

"""

This program sends and receives P2P messages with an IP grabbed from a JSON on an external server.

The JSON on the server is updated by the user's IP address when the program is run.

Said JSON is formatted as follows:

[
    'user_name': 'user_ip',
    'user_name': 'user_ip',
    'user_name': 'user_ip',
    ...
]

"""

# The server's IP address
JSON_ADDR = "http://fortress.us.to/users"

# The user's IP address
USER_IP = req.get('https://api.ipify.org').content.decode('utf8')


def get_user_list():
    """
    Gets the list of users from the server's JSON file.
    returns: The list of users.
    """
    # Get the JSON file from the server
    json_file = req.get(JSON_ADDR).content.decode('utf8')
    # Convert the JSON file to a Python dictionary
    user_list = json.loads(json_file)
    # Return the list of users
    return user_list

def get_user_ip(user):
    """
    Gets the IP address of a user from the server's JSON file.
    user: The user whose IP address is to be retrieved.
    returns: The IP address of the user.
    """
    # Get the list of users
    user_list = get_user_list()
    # Get the IP address of the user
    user_ip = user_list[user]
    # Return the IP address of the user
    return user_ip

def send_msg(user, message):
    """
    Sends a message to a user.
    user: The user to send the message to.
    message: The message to send.
    """
    # Get the IP address of the user
    user_ip = get_user_ip(user)
    # Send the message to the user
    req.get("http://" + user_ip + ":5000/send_message?message=" + message + "&user=" + USER_IP)

async def receive_msg():
    """
    opens a server to receive messages from other users.
    sends the message to a json file.
    json file formatted as follows:
    [
        'user_name' {
            "message": {user, message, time},
            "message": {user, message, time},
            ...
        },
        'user_name' {
            "message": {user, message, time},
            "message": {user, message, time},
            ...
        },
        ...
    ] 
    """

    # Make sure the JSON file exists
    if not os.path.exists("messages.json"):
        # Create the JSON file
        with open("messages.json", "w") as json_file:
            json.dump([], json_file)
        
        # Close the JSON file
        json_file.close()
    
    # Get the JSON file
    with open("messages.json", "r") as json_file:
        # Load the JSON file
        message_list = json.load(json_file)
        
        # Close the JSON file
        json_file.close()
    
    # open socket to scan for messages 
    # Create the Flask app
    app = flask.Flask(__name__)

    # Create the Flask route
    @app.route("/send_message")
    def send_message():
        # Get the message
        message = flask.request.args.get("message")
        # Get the user
        user = flask.request.args.get("user")
        # Add the message to the JSON file
        message_list[user].append([USER_IP, message, str(datetime._IsoCalendarDate.today())])
        # Save the JSON file
        with open("messages.json", "w") as json_file:
            json.dump(message_list, json_file)
            json_file.close()
        # Return the message
        return message
    
    # Run the Flask app
    app.run

def get_msg(user):
    """
    Gets the messages from a user.
    user: The user to get the messages from.
    returns: The messages from the user.
    """
    try:
        # Get the JSON file
        with open("messages.json", "r") as json_file:
            # Load the JSON file
            message_list = json.load(json_file)
            # Close the JSON file
            json_file.close()
    except:
        # Create the JSON file
        with open("messages.json", "w") as json_file:
            json.dump({}, json_file)
            # Close the JSON file
            json_file.close()
        # Get the JSON file
        with open("messages.json", "r") as json_file:
            # Load the JSON file
            message_list = json.load(json_file)
            # Close the JSON file
            json_file.close()
    try:
        # Get the messages from the user
        messages = message_list.get(user)
    except:
        print("user not found")
        # add user to json file
        message_list.update({user: []})
        messages = message_list[0].get(user)
        # Save the JSON file
        with open("messages.json", "w") as json_file:
            json.dump(message_list, json_file)
            json_file.close()
    return messages

if __name__ == "__main__":

    print("import only file")
    