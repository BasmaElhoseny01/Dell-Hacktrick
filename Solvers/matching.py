import cv2
import numpy as np
import matplotlib.pyplot as plt

def reconstruct_image(shredded_strips):
    reconstructed_image = [shredded_strips[0]]  # Initialize with the first strip

    # create boolean array to keep track of the strips that have been used
    used = [False] * len(shredded_strips)
    used[0] = True
    output = [0]
    while len(reconstructed_image) < len(shredded_strips):
        last_strip = reconstructed_image[-1]
        # loop through the strips to find the best match and mark it as used in the used array as index
        # and add it to the reconstructed image and add its index to the output array

        # create array to store match result of the last strip with all remaining strips
        match_result = []
        for j in range(len(shredded_strips)):
            if not used[j]:
                match_result.append( (match_strips(last_strip[:,-1], shredded_strips[j][:,0]),j,0))
        
        # add reversed strips to the match result array
        # for j in range(len(shredded_strips)):
        #     if not used[j]:
        #         # check rotated strip of 180 degree
        #         strip = np.flip(shredded_strips[j][:,-1])
        #         match_result.append( (match_strips(last_strip[:,-1], strip),j,1))
        # sort the match result array of tuples by the first element of the tuple
        
        match_result.sort(key=lambda x: x[0])
        print(match_result)
        best_match = match_result[0]
        used[best_match[1]] = True
        output.append(best_match[1])
        if best_match[2] == 1:
            reconstructed_image.append(rotate_strip(shredded_strips[best_match[1]]))
        else:
            reconstructed_image.append(shredded_strips[best_match[1]])

    return output,reconstructed_image

def rotate_strip(strip):
    # Rotate the strip 180 degrees using numpy
    strip = np.array(strip)
    width,height = strip.shape
    new_strip = np.zeros((width,height))
    for i in range(width):
        for j in range(height):
            new_strip[i][j] = strip[width-1-i][height-1-j]
    return new_strip



def match_strips(strip1, strip2):
    # Compare the rightmost pixels of strip1 with the leftmost pixels of strip2

    # Check if the pixels are within the specified tolerance
    tolerance = 0
    for i in range(len(strip1)):
        tolerance += abs(strip1[i] - strip2[i])
    return tolerance  # Pixels are within tolerance, return the match score

def solve():
    # Read the input image
    input_image = cv2.imread('../Riddles/cv_easy_example/shredded.png')
    output_image = cv2.imread('../Riddles/cv_easy_example/actual.jpg')

    # Convert the input image to grayscale
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)

    input_image = np.array(input_image)
    output_image = np.array(output_image)
    # Split the input image into strips of equal width = 64 pixels
    shredded_strips = [input_image[:, i:i+64] for i in range(0, input_image.shape[1], 64)]

    # Reconstruct the image
    output,image = reconstruct_image(shredded_strips)
    print(output)
    # Display the reconstructed image
    image = np.array(image)
    # convert image shape of (12,64,64) to (64,768)
    image = np.concatenate(image,axis=1)
    plt.imshow(np.array(image))
    plt.show()
    #[0, 11, 7, 1, 8, 9, 3, 5, 6, 4, 10, 2]
    # assert the reconstructed image equal the actual image 
    assert np.array_equal(np.array(image),np.array(output_image))
    print("Reconstructed image is correct")
solve()
