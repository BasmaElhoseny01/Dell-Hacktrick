import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split


# Fixing the seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)
 

class FootPrintDataSet(Dataset):
      def __init__(self, spectrogram_data: torch,labels: torch,transform_type:str ='train'):
        self.spectrogram_data =spectrogram_data
        self.labels = labels


        # self.transform_type=transform_type
   
      def __len__(self):
        return len(self.labels)
      
      def __getitem__(self, idx):
        #  TODO if to apply Transformation
        return self.spectrogram_data [idx],self.labels[idx]

        

def Split_Data(real_dataset_path:str,fake_dataset_path:str,train_val_test_ratio:tuple=(0.72,0.08,0.2)):
  #TODO fix ratio of split
  # Load the spectrogram data from the .npz file
  real_data = np.load(real_dataset_path)
  real_data_spectrogram =torch.tensor(real_data['x'])
  real_data_labels =torch.tensor(real_data['y'])
  # x=spectrogram_data_real['x'] #(750, 1998, 101)
  # y=spectrogram_data_real['y'] #(750, 496)

  # Load the spectrogram data from the .npz file
  fake_data = np.load(fake_dataset_path)
  fake_data_spectrogram =torch.tensor(fake_data['x'])
  fake_data_labels =torch.tensor(fake_data['y'])

  # Combine positive and negative words arrays
  spectrogram_data =torch.cat((real_data_spectrogram, fake_data_spectrogram), dim=0)

  # Combine positive and negative labels arrays
  labels = torch.cat((real_data_labels, fake_data_labels), dim=0)

  # Generate permutation indices
  indices = torch.randperm(len(labels))

  # Shuffle the dataset using permutation indices
  spectrogram_data = spectrogram_data[indices]
  labels = labels[indices]



  # Split to Train,test,Validate
  # Split X and Y into training, validation, and testing sets
  X_train, X_test, Y_train, Y_test = train_test_split(spectrogram_data, labels, test_size=0.2, random_state=42)
  # X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.1, random_state=42)
  X_val=None  
  Y_val=None  

  return X_train,Y_train,X_val,Y_val,X_test,Y_test


# X_train,Y_train,X_val,Y_val,X_test,Y_test=Split_Data(real_dataset_path='data/real.npz',fake_dataset_path='data/fake.npz')
# print(X_train.shape)
# print(Y_train.shape)
# print(X_val.shape)
# print(Y_val.shape)
# print(X_test.shape)
# print(Y_test.shape)


# data_set=FootPrintDataSet(spectrogram_data=X_train,labels=Y_train)

# print(len(data_set))
# print(data_set[0])



            

