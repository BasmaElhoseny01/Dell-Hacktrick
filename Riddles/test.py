from Solvers.riddle_solvers import solve_sec_medium
from SteganoGAN.utils import *
from PIL import Image
from torchvision import transforms

def read_image(file_path):
    # Read the image using OpenCV
    image = Image.open(file_path)
    return image

img=read_image("C:/Users/engah/Downloads/GP/Dell/HackTrick24-main/Dell-Hacktrick/sample_example/encoded.png")

print(solve_sec_medium(img))

# if len(img.shape)==4:
#     img=transforms.ToTensor()(img)
# elif img.shape[0]!=3:
#     img=img.permute(2,0,1)
#     img=transforms.ToTensor()(img)
#     img=img.unsqueeze(0)
# else:
#     img=transforms.ToTensor()(img)
#     img=img.unsqueeze(0)

# str=decode(img)
# print(str)