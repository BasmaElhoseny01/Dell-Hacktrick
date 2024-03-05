from SteganoGAN.utils import *
import cv2
def read_image(file_path):
    # Read the image using OpenCV
    image = cv2.imread(file_path)
    return image
img=read_image("C:/Users/engah/Downloads/GP/Dell/HackTrick24-main/Dell-Hacktrick/sample_example/encoded.png")
# change img to tensor
img = torch.tensor(img,dtype=torch.float32)
print(img.shape)
img=img.permute(2,0,1)
img=img.unsqueeze(0)
str=decode(img)
print(str)
print(type(str))