import requests
import numpy as np
import random
from LSBSteg import encode
from riddle_solvers import riddle_solvers

api_base_url = None
#TODO: Set the api_base_url to the base url of the API when Ready
# api_base_url = "http://3.70.97.142:5000/"
# team_id= "hAaIrJk"

def init_fox(team_id):
    '''
    In this function you need to hit to the endpoint to start the game as a fox with your team id.
    If a sucessful response is returned, you will recive back the message that you can break into chunkcs
      and the carrier image that you will encode the chunk in it.
    '''
    # API endpoint
    url = api_base_url + "/fox/start"
    # Request payload
    payload = {"teamId": team_id}
    # Make the API request
    response = requests.post(url, json=payload)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        # Extracting the secret message and carrier image
        secret_message = response_data.get("msg")
        image_carrier = response_data.get("carrier_image")
    else:
        # Print an error message if the request was not successful
        return None, None

    #TODO: return the secret message and the carrier image
    # image_carrier is List???
    return secret_message, image_carrier 
    

def generate_message_array(message, image_carrier):  
    '''
    In this function you will need to create startegy to trick . That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide which chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    def split_message_part(part, choice):
        num_parts = len(part) // choice
        return [part[i * choice: (i + 1) * choice] for i in range(num_parts)]

    first_part = message[:12]
    second_part = message[12:20]

    first_choice = random.choice([1, 2, 4, 3, 6, 12])
    second_choice = random.choice([1, 2, 4, 8])
    
    real_messages = split_message_part(first_part, first_choice)
    real_messages.extend(split_message_part(second_part, second_choice))

    array_messages = []
    image_carrier_messages = []
    for real_message in real_messages:
        #intialize the encoded message with the original image carrier
        array_message = image_carrier
        image_carrier_message=["E","E","E"]
        #choose a random image carrier to encode the message
        image_carrier_real_index = random.choice([0,1,2])
        #encode the message in the image carrier
        encoded_message=encode(image_carrier[image_carrier_real_index], real_message)
        array_message[image_carrier_real_index] = encoded_message
        image_carrier_message[image_carrier_real_index] = "R"
        #check if want to insert fake message in the other two channels
        if random.choice([True, False]):
        # append Fake message in the other two channels
            fake_message_index = [0,1,2]
            fake_message_index.remove(image_carrier_real_index)
            random_element = random.choice(fake_message_index)
            fake_message_index.remove(random_element)
            #intialize fake message with the original image carrier
            fake_messag_encode=encode(image_carrier[random_element], "Fake Message")
            array_message[fake_message_index[0]] =fake_messag_encode
            image_carrier_message[fake_message_index[0]] = "F"

        image_carrier_messages.append(image_carrier_message)
        array_messages.append(array_message)

    # choose 2 random posions to insert [F,E,E] message in array_messages 
    if random.choice([True, False]):
        for i in range(2):
            random_index = random.choice([0,1,2])
            fake_messages = image_carrier
            fake_messages[0] = encode(image_carrier[0], "Fake Message")
            image_carrier_message= ["F","E","E"]
            array_messages.insert(random_index,fake_messages)
            image_carrier_messages.insert(random_index,image_carrier_message)

    return array_messages ,image_carrier_messages



def get_riddle(team_id, riddle_id):
    '''
    In this function you will hit the api end point that requests the type of riddle you want to solve.
    use the riddle id to request the specific riddle.
    Note that: 
        1. Once you requested a riddle you cannot request it again per game. 
        2. Each riddle has a timeout if you didnot reply with your answer it will be considered as a wrong answer.
        3. You cannot request several riddles at a time, so requesting a new riddle without answering the old one
          will allow you to answer only the new riddle and you will have no access again to the old riddle. 
    '''
    # API endpoint
    url = api_base_url + "/fox/get-riddle"
    # Request payload
    payload = {"teamId": team_id,
               "riddleId":riddle_id
               }
    # Make the API request
    response = requests.get(url, json=payload)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        test_case = response_data.get("test_case")
    else:
        # Print an error message if the request was not successful
        return None,False

    return test_case,True


def solve_riddle(team_id, solution):
    '''
    In this function you will solve the riddle that you have requested. 
    You will hit the API end point that submits your answer.
    Use te riddle_solvers.py to implement the logic of each riddle.
    '''
     # API endpoint
    url = api_base_url + "/fox/solve-riddle"
    # Request payload
    payload = {"teamId": team_id,
               "solution":solution
               }
    # Make the API request
    response = requests.post(url, json=payload)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        budget_increase = response_data.get("budget_increase")
        total_budget = response_data.get("total_budget")
        status=response_data.get("status")
    else:
        # Print an error message if the request was not successful
        return None,None,None,None,False
    if status == "success":
        # return True  and total budget and additional budget
        return True, total_budget, budget_increase,True
    else:
        # return False and the correct solution
        return False, total_budget, budget_increase,True

def send_message(team_id, messages, message_entities=['F', 'E', 'R']):
    '''
    Use this function to call the api end point to send one chunk of the message. 
    You will need to send the message (images) in each of the 3 channels along with their entites.
    Refer to the API documentation to know more about what needs to be send in this api call. 
    '''
    # API endpoint
    url = api_base_url + "/fox/send-message"
    # Request payload
    payload = {"teamId": team_id,
               "messages":messages,
                "message entities":message_entities
               }
    # Make the API request
    response = requests.post(url, json=payload)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        # Parse the JSON response
        response_data = response.json()
        status = response_data.get("status")
    else:
        # Print an error message if the request was not successful
        False
    if status == "success":
        return True
    else:
        return False

   
def end_fox(team_id):
    '''
    Use this function to call the api end point of ending the fox game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    2. Calling it without sending all the real messages will also affect your scoring fucntion
      (Like failing to submit the entire message within the timelimit of the game).
    '''
    # API endpoint
    url = api_base_url + "/fox/end-game"
    # Request payload
    payload = {"teamId": team_id}
    # Make the API request
    response = requests.post(url, json=payload)
    # Check if the request was successful (status code 200)
    if response.status_code == 200 or response.status_code == 201:
        #TODO: Parse the JSON response
        response_data = response
        print( response_data)
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)

def submit_fox_attempt(team_id):
    '''
     Call this function to start playing as a fox. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as a Fox In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve riddles 
        3. Make your own Strategy of sending the messages in the 3 channels
        4. Make your own Strategy of splitting the message into chunks
        5. Send the messages 
        6. End the Game
    Note that:
        1. You HAVE to start and end the game on your own. The time between the starting and ending the game is taken into the scoring function
        2. You can send in the 3 channels any combination of F(Fake),R(Real),E(Empty) under the conditions that
            2.a. At most one real message is sent
            2.b. You cannot send 3 E(Empty) messages, there should be atleast R(Real)/F(Fake)
        3. Refer To the documentation to know more about the API handling 
    '''
    #1. Initialize the game as fox
    message ,image_carriers= init_fox(team_id)
    #2. Solve riddles
    # iterate on ridele_solvers
    for riddle_id in riddle_solvers:
        test_case = get_riddle(team_id, riddle_id)
        solution = riddle_solvers[riddle_id](test_case)
        budget_increase ,total_budget,status = solve_riddle(team_id, solution)
    #3. Make your own Strategy of sending the messages in the 3 channels
    #4. Make your own Strategy of splitting the message into chunks
    array_messages ,image_carrier_messages = generate_message_array(message, image_carriers)
    #5. Send the messages
    for i in range(len(array_messages)):
        status = send_message(team_id, array_messages[i], image_carrier_messages[i])
    #6. End the Game
    end_fox(team_id)
    
    


submit_fox_attempt(team_id)