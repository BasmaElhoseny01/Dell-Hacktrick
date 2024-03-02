import requests
import numpy as np
api_base_url = "http://localhost:3000"
team_id= "hAaIrJk"
def fox_test(team_id):
    '''
    In this fucntion you need to hit to the endpoint to start the game as a fox with your team id.
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
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        # Extracting the secret message and carrier image
        secret_message = response_data.get("msg")
        image_carrier = response_data.get("carrier_image")
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)

    #TODO: return the secret message and the carrier image
    # image is List???
    return secret_message, image_carrier  


secret_message, image_carrier = fox_test(team_id)
print(type(secret_message), image_carrier)
print("done")
#create np array with inter value in it
np_array = np.ones((2,2,3))
print(np_array)
print(np_array.tolist())