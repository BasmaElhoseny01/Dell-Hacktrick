import random
import numpy as np

import torch
import torch.optim as optim
from torch.utils.data import  DataLoader
from sklearn.model_selection import train_test_split


from dataset import FootPrintDataSet,Split_Data

from config import *


# Fixing the seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)

def seed_worker(worker_id):
    """To preserve reproducibility for the randomly shuffled train loader."""
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)

class EagleTrainer():
    def __init__(self, model,real_dataset_path: str,fake_dataset_path: str):
        self.model = model

        # Move to device
        # self.model.to(DEVICE)

        # create adam optimizer
        # self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE, betas=(BETA_1, BETA_2), weight_decay=WEIGHT_DECAY)

        # create learning rate scheduler
        # self.lr_scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=SCHEDULAR_STEP_SIZE, gamma=SCHEDULAR_GAMMA)

        # Split_Data
        X_train,Y_train,X_val,Y_val,X_test,Y_test=Split_Data(real_dataset_path=real_dataset_path,fake_dataset_path=fake_dataset_path)


        self.train_dataset=FootPrintDataSet(spectrogram_data=X_train,labels=Y_train,transform_type='train')
        self.val_dataset=FootPrintDataSet(spectrogram_data=X_val,labels=Y_val,transform_type='val')
        self.test_dataset=FootPrintDataSet(spectrogram_data=X_test,labels=Y_test,transform_type='test')

        # create data loader
        g = torch.Generator()
        g.manual_seed(SEED)
        self.data_loader_train = DataLoader(dataset=self.train_dataset,batch_size=BATCH_SIZE, shuffle=True,  num_workers=8, worker_init_fn=seed_worker, generator=g)
        self.data_loader_val   = DataLoader(dataset=self.val_dataset  ,batch_size=BATCH_SIZE, shuffle=False, num_workers=8)
        self.data_loader_test  = DataLoader(dataset=self.test_dataset ,batch_size=BATCH_SIZE, shuffle=False, num_workers=8)


        # initialize the best loss to a large value
        self.best_loss = float('inf')

    def train(self):
        pass



eagle_model=None

trainer=EagleTrainer(model=eagle_model,real_dataset_path='data/real.npz',fake_dataset_path='data/fake.npz')

trainer.train()





    
