import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def read_image(file_path):
    # Read the image using OpenCV
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return image


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


# Example usage
file_path = 'E:\MY Work\Dell_Competation\Dell-Hacktrick\Riddles\cv_easy_example\shredded.jpg'
shred_width = 64

image = read_image(file_path)
# Display the image
plt.imshow(image)
plt.axis('off')  # Turn off axis labels
plt.show()
test_case=(image,shred_width)
order = solve_cv_easy(test_case)
print(order)
reconstructed_image = np.hstack([image[:, i * shred_width: (i + 1) * shred_width] for i in order])
print(reconstructed_image.shape)
# Display the reconstructed image
# Display the image
plt.imshow(reconstructed_image)
plt.axis('off')  # Turn off axis labels
plt.show()
# cv2.destroyAllWindows()
