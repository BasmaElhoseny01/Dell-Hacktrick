import requests
import numpy as np
import random
from LSBSteg import encode
from Solvers.riddle_solvers import riddle_solvers, reddle_points

api_base_url = None
#TODO: Set the api_base_url to the base url of the API when Ready
# api_base_url = "http://3.70.97.142:5000"
# team_id= "hAaIrJk"
team_id= ""

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
        # Convert the carrier image to a NumPy array
        image_carrier = np.array(image_carrier)
    else:
        # Print an error message if the request was not successful
        return None, None

    return secret_message, image_carrier 
    

def generate_message_array(message, image_carrier,num_of_fake_messages):  
    '''
    In this function you will need to create startegy to trick . That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide which chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    i=0
    real_messages=[]
    while i<len(message):
        random_index=random.choice([1, 2, 3,4])
        real_messages.append(message[i:i+random_index])
        i+=random_index
    #encode real messages 
    array_messages = []
    entities_messages = []
    count_fake_used=1
    for real_message in real_messages:
        #intialize the encoded message with the original image carrier
        array_message = [0, 1, 2]
        entities_message=["E","E","E"]
        #choose a random image carrier to encode the message
        image_carrier_real_index = random.choice([0,1,2])
        #encode the message in the image carrier
        encoded_message=encode(image_carrier[image_carrier_real_index], real_message).tolist()
        array_message[image_carrier_real_index] = encoded_message
        entities_message[image_carrier_real_index] = "R"

        #check if want to insert fake message in the other two channels
        if len(real_message)>1 and num_of_fake_messages!=0 and count_fake_used<=12:
            # append Fake message in the other two channels
            fake_message_index = [0,1,2]
            fake_message_index.remove(image_carrier_real_index)
            if len(real_message)<2:
                random_element = random.choice(fake_message_index)
                fake_message_index.remove(random_element)
            #intialize fake message with the original image carrier
            for i in fake_message_index:
                fake_messag_encode=encode(image_carrier[i], "Dell").tolist()
                array_message[i] =fake_messag_encode
                entities_message[i] = "F"
                num_of_fake_messages-=1
                count_fake_used+=1
        #insert empty message
        for i, entity in enumerate(entities_message):
            if entity=="E":
                empty_messag_encode=encode(image_carrier[i], "").tolist()
                array_message[i] =empty_messag_encode

        entities_messages.append(entities_message)
        array_messages.append(array_message)

    return array_messages ,entities_messages



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
    response = requests.post(url, json=payload)
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
                "message_entities":message_entities
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
    # if response.status_code == 200 or response.status_code == 201:
    #     #TODO: Parse the JSON response
    #     response_data = response
        # save the response in txt file
    with open("end_game_response.txt", "w") as file:
        file.write(str(response.text))
    # else:
    #     # Print an error message if the request was not successful
    #     with open("end_game_response.txt", "w") as file:
    #         file.write(str(response_data))
    #     print("Error:", response.text)

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
    num_of_fake_messages=0
    for riddle_id in riddle_solvers:
        try:
            test_case ,riddle_exist= get_riddle(team_id, riddle_id)
            if not riddle_exist:
                continue
            solution,fake_num = riddle_solvers[riddle_id](test_case)
            status, total_budget, budget_increase,Done = solve_riddle(team_id, solution)
            #TODO:
            if Done and status:
                num_of_fake_messages+=reddle_points[riddle_id]
        except:
            continue
    #3. Make your own Strategy of sending the messages in the 3 channels
    #4. Make your own Strategy of splitting the message into chunks
    array_messages ,entities_messages = generate_message_array(message, image_carriers ,num_of_fake_messages)
    #5. Send the messages
    for i in range(len(array_messages)):
        try:
            status = send_message(team_id, array_messages[i], entities_messages[i])
        except:
            continue
    #6. End the Game
    end_fox(team_id)
    

submit_fox_attempt(team_id)