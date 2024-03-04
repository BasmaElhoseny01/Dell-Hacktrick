
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.ndimage import gaussian_filter

import sys

def preprocessing(data_spectrogram):
  # Numpy batch_tx_f
  # Replace infinity values with zeros
  data_spectrogram[np.isinf(data_spectrogram)] = 65500.0

  # Replace NaN values with zeros
  # data_spectrogram[np.isnan(data_spectrogram)] = 65500.0

  # Compute the Gaussian average
  # gaussian_avg_spectrogram = gaussian_filter(data_spectrogram, sigma=1)
  return data_spectrogram

def Split_Data(real_dataset_path:str,fake_dataset_path:str,train_val_test_ratio:tuple=(0,0,0)):
  #TODO fix ratio of split
  # Load the spectrogram data from the .npz file
  real_data = np.load(real_dataset_path)
  real_data_spectrogram =real_data['x'][:,:real_data['x'].shape[1]-1,:]
  real_data_labels =real_data['y']
  # x=spectrogram_data_real['x'] #(750, 1998, 101)
  # y=spectrogram_data_real['y'] #(750, 496)

  # Load the spectrogram data from the .npz file
  fake_data = np.load(fake_dataset_path)
  # remove last row in fake data
  fake_data_spectrogram =fake_data['x'][:,:fake_data['x'].shape[1]-1,:]
  fake_data_labels =fake_data['y']


  # X_train, X_test, Y_train, Y_test = train_test_split(spectrogram_data, labels, test_size=0.2, random_state=42)
  X_train_real ,X_test_real, Y_train_real, Y_test_real= train_test_split(real_data_spectrogram, real_data_labels, test_size=0.2, random_state=40)
  X_train_fake ,X_test_fake, Y_train_fake, Y_test_fake= train_test_split(fake_data_spectrogram, fake_data_labels, test_size=0.2, random_state=50)
  # Conatnate real and fake data
  X_train=np.concatenate((X_train_real,X_train_fake),axis=0)
  Y_train=np.concatenate((Y_train_real,Y_train_fake),axis=0)
  X_test=np.concatenate((X_test_real,X_test_fake),axis=0)
  Y_test=np.concatenate((Y_test_real,Y_test_fake),axis=0)

  # shuffle the data
  indices = np.random.permutation(len(Y_train))
  X_train = X_train[indices]
  Y_train = Y_train[indices]
  indices = np.random.permutation(len(Y_test))
  X_test = X_test[indices]
  Y_test = Y_test[indices]




  # # print(real_data_spectrogram.shape)
  # # print(real_data_labels.shape)
  # # print(fake_data_spectrogram.shape)
  # # print(fake_data_labels.shape)
  # # sys.exit()

  # # Combine positive and negative words arrays
  # # spectrogram_data =torch.cat((real_data_spectrogram, fake_data_spectrogram), dim=0)
  # spectrogram_data =np.concatenate((real_data_spectrogram, fake_data_spectrogram), axis=0)

  # # Combine positive and negative labels arrays
  # labels = np.concatenate((real_data_labels, fake_data_labels), axis=0)

  # # Generate permutation indices
  # # indices = torch.randperm(len(labels))
  # indices = np.random.permutation(len(labels))

  # # Shuffle the dataset using permutation indices
  # spectrogram_data = spectrogram_data[indices]
  # labels = labels[indices]



  # Split to Train,test,Validate
  # Split X and Y into training, validation, and testing sets
  # X_train, X_test, Y_train, Y_test = train_test_split(spectrogram_data, labels, test_size=0.2, random_state=42)
  # X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.1, random_state=42)
  X_val=None
  Y_val=None

  return X_train,Y_train,X_val,Y_val,X_test,Y_test
