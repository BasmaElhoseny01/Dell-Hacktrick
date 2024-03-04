# Add the necessary imports here
import pandas as pd
import torch
import numpy as np
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from SteganoGAN.utils import *


def solve_cv_easy(test_case: tuple) -> list:
    shredded_image, shred_width = test_case
    shredded_image = np.array(shredded_image)
    """
    This function takes a tuple as input and returns a list as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A numpy array representing a shredded image.
        - An integer representing the shred width in pixels.

    Returns:
    list: A list of integers representing the order of shreds. When combined in this order, it builds the whole image.
    """
    # slice image be shred_width vertically
    sliced_image = [shredded_image[:, i * shred_width: (i + 1) * shred_width] for i in range(shredded_image.shape[1] // shred_width)]
    current_shred = sliced_image[0]
    order = [0]
    while len(order) < len(sliced_image):
        best_match = -1
        best_similarity = 0
        for shred_index in range(len(sliced_image)):
            if shred_index not in order:
                similarity = np.sum(current_shred[:,-1] == sliced_image[shred_index][:,0])
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = shred_index
        order.append(best_match)
        current_shred = sliced_image[best_match]

    return order


def solve_cv_medium(input: tuple) -> list:
    combined_image_array , patch_image_array = input
    combined_image = np.array(combined_image_array,dtype=np.uint8)
    patch_image = np.array(patch_image_array,dtype=np.uint8)
    """
    This function takes a tuple as input and returns a list as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A numpy array representing the RGB base image.
        - A numpy array representing the RGB patch image.

    Returns:
    list: A list representing the real image.
    """
    return []


def solve_cv_hard(input: tuple) -> int:
    extracted_question, image = input
    image = np.array(image)
    """
    This function takes a tuple as input and returns an integer as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A string representing a question about an image.
        - An RGB image object loaded using the Pillow library.

    Returns:
    int: An integer representing the answer to the question about the image.
    """
    return 0


def solve_ml_easy(input: pd.DataFrame) -> list:
    data = pd.DataFrame(input)

    """
    This function takes a pandas DataFrame as input and returns a list as output.

    Parameters:
    input (pd.DataFrame): A pandas DataFrame representing the input data.

    Returns:
    list: A list of floats representing the output of the function.
    """
    # implement time series forecasting using ARIMA model


    return []


def solve_ml_medium(input: list) -> int:
    """
    This function takes a list as input and returns an integer as output.

    Parameters:
    input (list): A list of signed floats representing the input data.

    Returns:
    int: An integer representing the output of the function.
    """
    return 0



def solve_sec_medium(input: torch.Tensor) -> str:
    img = torch.tensor(input)
    """
    This function takes a torch.Tensor as input and returns a string as output.

    Parameters:
    input (torch.Tensor): A torch.Tensor representing the image that has the encoded message.

    Returns:
    str: A string representing the decoded message from the image.
    """
    return decode(img)

def solve_sec_hard(input:tuple)->str:
    """
    This function takes a tuple as input and returns a list a string.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A key 
        - A Plain text.

    Returns:
    list:A string of ciphered text
    """
    # convert input to correct format
    input = tuple(input)
    # implement DES encryption
    key = input[0]
    plaintext = input[1]
    key =   bytes.fromhex(key)
    plaintext = bytes.fromhex(plaintext)
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = plaintext
    ciphertext = cipher.encrypt(padded_text)
    ciphertext = ciphertext.hex()
    ciphertext = ciphertext.upper()
    return ciphertext

def solve_problem_solving_easy(input: tuple) -> list:
    """
    This function takes a tuple as input and returns a list as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A list of strings representing a question.
        - An integer representing a key.

    Returns:
    list: A list of strings representing the solution to the problem.
    """
    # convert input to correct format
    input = tuple(input)
    strings, top_x = input[0],input[1]
    # make dictionary of strings with count of occurence of each string

    unique_strings = {}
    for i in range(len(strings)):
        # if strings[i] in dict keys add one to value
        if unique_strings.get(strings[i],None) is not None:
            unique_strings[strings[i]] += 1
        else:
            unique_strings[strings[i]] = 1
    # sort dictionary by value in descending order and lexigraphically in ascending order if equal
    # unique_strings = dict(sorted(unique_strings.items(), key=lambda item: (-item[1], item[0])))
    unique_strings = sorted(unique_strings.items(), key=lambda item: (-item[1], item[0]))
    unique_strings = unique_strings[:top_x]
    # return strings
    return [k[0] for k in unique_strings]
    # return top x keys of dictionary
    return list(unique_strings.keys())[:top_x]


def solve_problem_solving_medium(input: str) -> str:
    """
    This function takes a string as input and returns a string as output.

    Parameters:
    input (str): A string representing the input data.

    Returns:
    str: A string representing the solution to the problem.
    """
    # ex: of input "3[d1[e2[l]]]"
    # output: "delldelldell"
    # convert input to correct format
    input = str(input)
    stack = []
    # iterate over string
    for i in range(len(input)):
        # if character is not "]" push to stack
        if input[i] != "]":
            stack.append(input[i])
        else:
            # if character is "]" pop from stack until "[" is found
            temp = ""
            while stack[-1] != "[":
                temp = stack.pop() + temp
            stack.pop()
            # pop until digit is found
            num = ""
            while stack and stack[-1].isdigit():
                num = stack.pop() + num
            # push temp * num to stack
            stack.append(temp*int(num))
    # return stack as string
    return ''.join(stack)


def solve_problem_solving_hard(input: tuple) -> int:
    """
    This function takes a tuple as input and returns an integer as output.

    Parameters:
    input (tuple): A tuple containing two integers representing m and n.

    Returns:
    int: An integer representing the solution to the problem.
    """
    # convert input to correct format
    input = tuple(input)
    # given grid of size m x n and only moves allowed are right and down find number of unique paths from top left to bottom right
    m,n = input[0],input[1]
    # create grid of size m x n
    grid = [[0 for i in range(n)] for j in range(m)]
    # fill first row and first column with 1
    for i in range(m):
        grid[i][0] = 1
    for i in range(n):
        grid[0][i] = 1
    # fill grid with sum of top and left cells
    for i in range(1,m):
        for j in range(1,n):
            grid[i][j] = grid[i-1][j] + grid[i][j-1]
    # return bottom right cell
    return grid[-1][-1]

riddle_solvers = {
    # 'cv_easy': solve_cv_easy,
    # 'cv_medium': solve_cv_medium,
    # 'cv_hard': solve_cv_hard,
    # 'ml_easy': solve_ml_easy,
    # 'ml_medium': solve_ml_medium,
    'sec_medium_stegano': solve_sec_medium,
    'sec_hard':solve_sec_hard,
    'problem_solving_easy': solve_problem_solving_easy,
    'problem_solving_medium': solve_problem_solving_medium,
    'problem_solving_hard': solve_problem_solving_hard
}

reddle_points = {
    # 'cv_easy': 1,
    # 'cv_medium': 2,
    # 'cv_hard': 3,
    # 'ml_easy': 1,
    # 'ml_medium': 2,
    'sec_medium_stegano': 2,
    'sec_hard':3,
    'problem_solving_easy': 1,
    'problem_solving_medium': 2,
    'problem_solving_hard': 3
}
