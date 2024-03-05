from PIL import Image
from transformers import pipeline
import numpy as np
def solve_cv_hard(input: tuple) -> int:
    extracted_question, image = input
    """
    This function takes a tuple as input and returns an integer as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A string representing a question about an image.
        - An RGB image object loaded using the Pillow library.

    Returns:
    int: An integer representing the answer to the question about the image.
    """
    vqa_pipeline = pipeline("visual-question-answering")
    #Q: is model in gpu or not?
    #A: No, it is not in gpu
    #Q: How to make it in gpu?
    #A: I don't know
    answer=vqa_pipeline(image, extracted_question, top_k=1)
    return int(answer[0]['answer'])


# Example usage:
question = "How many cats are there?"
image_path = "E:\MY Work\Dell_Competation\Dell-Hacktrick\Riddles\cv_hard_example\cv_hard_sample_image.jpg"
# Load the image
image = Image.open(image_path)
# calclaute time take by the function
import time
start = time.time()
# Get the answer
result = solve_cv_hard((question,image))

end = time.time()
print(end - start)
print(result)
print("type",type(result))
