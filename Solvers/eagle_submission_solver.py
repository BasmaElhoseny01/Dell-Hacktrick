import numpy as np
from LSBSteg import decode
import requests

from get_eagle import get_eagle_model

api_base_url = None
#TODO: Set the api_base_url to the base url of the API when Ready
# api_base_url = "http://3.70.97.142:5000/"
# team_id=None
team_id="hAaIrJk"
DEBUG = True

def init_eagle(team_id):
    '''
    In this fucntion you need to hit to the endpoint to start the game as an eagle with your team id.
    If a sucessful response is returned, you will recive back the first footprints.
    '''
    # /eagle/start
    # send post request to the server to start the game as an eagle
    url = api_base_url + "eagle/start"
    # Request payload
    payload = {"teamId": team_id}
    # Make the API request
    response = requests.post(url, json=payload)
    if DEBUG:
        # Print the response
        try:
            
            print("init eagle: ",response.text)
            print("init eagle: ",response.json())
        except Exception as e:
            print(e)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        # Extracting the secret message and carrier image
        footprints = response_data.get("footprint")
        return footprints
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
    return None


def select_channel(footprint,eagle):
    '''
    According to the footprint you recieved (one footprint per channel)
    you need to decide if you want to listen to any of the 3 channels or just skip this message.
    Your goal is to try to catch all the real messages and skip the fake and the empty ones.
    Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.        
    '''
    # footprint is a numpy array [(1998,101)]
    # Preprocessing
    footprint[np.isinf(footprint)] = 65500.0

    # Remove Last Time step
    footprint=footprint[0:1997,:]

    y=eagle.predict(np.expand_dims(footprint, axis=0))

    # Threshold on the Probability
    y=y[0]>0.5

    consecutive_ones = 0
    for num in y:
        if num == 1:
            consecutive_ones += 1
            if consecutive_ones >= 10:
                break
        else:
            consecutive_ones = 0
    if consecutive_ones >= 10:
        return True
    else: return False

def skip_msg(team_id):
    '''
    If you decide to NOT listen to ANY of the 3 channels then you need to hit the end point skipping the message.
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.
    '''
    # /eagle/skip-message
    # send post request to the server to skip the message
    url = api_base_url + "eagle/skip-message"
    # Request payload
    payload = {"teamId": team_id}
    # Make the API request
    response = requests.post(url, json=payload)
    if DEBUG:
        # Print the response
        try:
            
            print("skip eagle: ",response.text)
            print("skip eagle: ",response.json())
        except Exception as e:
            print(e)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        # Extracting the secret message and carrier image
        # check if the response_data has the key "footprint"
        footprints = response_data.get("footprint")
        return footprints
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
    return None


def request_msg(team_id, channel_id):
    '''
    If you decide to listen to any of the 3 channels then you need to hit the end point of selecting a channel to hear on (1,2 or 3)
    '''
    # /eagle/request-message
    # send post request to the server to request the message
    url = api_base_url + "eagle/request-message"
    # Request payload
    payload = {"teamId": team_id, "channelId": channel_id}
    # Make the API request
    response = requests.post(url, json=payload)
    if DEBUG:
        # Print the response
        try:
            
            print("request_msg eagle: ",response.text)
            print("request_msg eagle: ",response.json())
        except Exception as e:
            print(e)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        # Extracting the secret message and carrier image
        secret_message = response_data.get("encodedMsg")

        # convert to numpy array
        secret_message = np.array(secret_message)
        return secret_message
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
    return None

def submit_msg(team_id, decoded_msg):
    '''
    In this function you are expected to:
        1. Decode the message you requested previously
        2. call the api end point to send your decoded message  
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.
    '''
    #/eagle/submit-message
    # send post request to the server to submit the message
    url = api_base_url + "eagle/submit-message"
    # Request payload
    payload = {"teamId": team_id, "decodedMsg": decoded_msg}
    # Make the API request
    response = requests.post(url, json=payload)
    if DEBUG:
        # Print the response
        try:
            
            print("submit_msg eagle: ",response.text)
            print("submit_msg eagle: ",response.json())
        except Exception as e:
            print(e)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        # check if the response_data has the key "footprint"
        try:    
            footprints = response_data.get("nextFootprint")
        except:
            footprints = None
        return footprints
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
  
def end_eagle(team_id):
    '''
    Use this function to call the api end point of ending the eagle  game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    '''
    # /eagle/end-game
    # send post request to the server to end the game as an eagle
    url = api_base_url + "eagle/end-game"
    # Request payload
    payload = {"teamId": team_id}
    # Make the API request
    response = requests.post(url, json=payload)
    if DEBUG:
        # Print the response
        try:
            
            print("end eagle: ",response.text)
            print("end eagle: ",response.json())
        except Exception as e:
            print(e)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # response is a string of the status not a json object
        response_data = response.json()
        print(response_data)
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
    return None

def submit_eagle_attempt(team_id):
    '''
     Call this function to start playing as an eagle. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as an Eagle In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve the footprints to know which channel to listen on if any.
        3. Select a channel to hear on OR send skip request.
        4. Submit your answer in case you listened on any channel
        5. End the Game
    '''
    # Get Eagle Model Before Initializing the Game :D
    eagle_model=get_eagle_model()
    
    footprints = init_eagle(team_id)
    # check if the footprints is None
    if footprints is None:
        return False
    
    try:
        break_loop = False
        while True:
            if break_loop:
                break
            listen = False
            channel_id = 0

            #TODO: change this logic so that select channel that has highest probability 
            #      of having a message if more than one channel has > 0.5 probability to have a message
            for i in range(1,4):
                spectogram = footprints[str(i)]
                # convert to numpy array
                spectogram = np.array(spectogram)
                # check if the spectogram is empty
                # call select_channel to decide if to listen on the channel or not
                if select_channel(spectogram,eagle_model):
                    listen = True
                    channel_id = i
                    break
            if listen:
                # call request_msg to get the message
                secret_message = request_msg(team_id, channel_id)
                # check if the secret_message is None
                if secret_message is None:
                    return False
                # decode the message
                decoded_msg = decode(secret_message)

                # print the decoded message
                print("decoded message: ",decoded_msg)
                # call submit_msg to submit the message
                footprints = submit_msg(team_id, decoded_msg)
                # check if the footprints is None
                if footprints is None:
                    break_loop = True
            else:
                # call skip_msg to skip the message
                footprints = skip_msg(team_id)
                # check if the footprints is None
                if footprints is None:
                    break_loop = True
    except Exception as e:
        # send end game request
        print("Exception: error")
        print(e)
        end_eagle(team_id)
        return False
    # send end game request
    end_eagle(team_id)


submit_eagle_attempt(team_id)

