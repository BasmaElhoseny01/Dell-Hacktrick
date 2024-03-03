import random
import numpy as np

import torch
import torch.optim as optim
from torch.utils.data import  DataLoader
from sklearn.model_selection import train_test_split


from eagle.dataset import FootPrintDataSet,Split_Data
from eagle.model import GRU

from eagle.config import *
from eagle.utils import *
import sys

# Fixing the seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)

class EagleTrainer():
    def __init__(self, model,real_dataset_path: str,fake_dataset_path: str):
        self.model = model

        # Move to device
        self.model.to(DEVICE)

        # create adam optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE, betas=(BETA_1, BETA_2), weight_decay=WEIGHT_DECAY)

        # create learning rate scheduler
        self.lr_scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=SCHEDULAR_STEP_SIZE, gamma=SCHEDULAR_GAMMA)

        # Split_Data
        X_train,Y_train,X_val,Y_val,_,_=Split_Data(real_dataset_path=real_dataset_path,fake_dataset_path=fake_dataset_path)


        self.train_dataset=FootPrintDataSet(spectrogram_data=X_train,labels=Y_train,transform_type='train')
        self.val_dataset=FootPrintDataSet(spectrogram_data=X_val,labels=Y_val,transform_type='val')
        # self.test_dataset=FootPrintDataSet(spectrogram_data=X_test,labels=Y_test,transform_type='test')

        # create data loader
        g = torch.Generator()
        g.manual_seed(SEED)
        self.data_loader_train = DataLoader(dataset=self.train_dataset,batch_size=BATCH_SIZE, shuffle=True,  num_workers=8, worker_init_fn=seed_worker, generator=g)
        self.data_loader_val   = DataLoader(dataset=self.val_dataset  ,batch_size=BATCH_SIZE, shuffle=False, num_workers=8)
        # self.data_loader_test  = DataLoader(dataset=self.test_dataset ,batch_size=BATCH_SIZE, shuffle=False, num_workers=8)


        # initialize the best loss to a large value
        self.best_loss = float('inf')

    def train(self):
        if DEBUG:
            print("Start Training")
        # self.model.train()
        for epoch in range(EPOCHS):
            epoch_loss=0
            for batch_index , (batch_x,batch_y) in enumerate(self.data_loader_train):
                # Move to Device
                batch_x=batch_x.to(DEVICE)
                batch_y=batch_y.to(DEVICE)

                # Forward Pass
                losses=self.model(batch_x,batch_y)
                sys.exit()
                epoch_loss+=losses

                if DEBUG:
                    print(f'epoch: {epoch+1}, Batch {batch_index + 1}/{len(self.data_loader_train)} losses: {losses:.4f}')

                # Backward pass
                losses.backward()

                # Learning
                if (batch_index+1) %ACCUMULATION_STEPS==0:
                    # update the parameters
                    self.optimizer.step()
                    # zero the parameter gradients
                    self.optimizer.zero_grad()
                    if DEBUG:
                        # print(f'[Accumlative Learning after {batch_index+1} steps ] Update Weights at  epoch: {epoch+1}, Batch {batch_index + 1}/{len(self.data_loader_train)} ')
                        pass
                
                # Average Epoch Loss
                if (batch_index+1)%100==0:
                    # Every 100 Batch print Average Loss for epoch till Now
                    print(f'[Every 100 Batch]: Epoch {epoch+1}/{EPOCHS}, Batch {batch_index + 1}/{len(self.data_loader_train)}, Average Cumulative Epoch Loss : {epoch_loss/(batch_index+1):.4f}')
                   

                    
               
            # validate the model no touch :)
            self.model.eval()
            validation_average_loss= self.validate_during_training() 
            if DEBUG:
                print(f'Validation Average Loss: {validation_average_loss:.4f}')
            self.model.train()     

            # Learning Rate Schedular
            self.lr_scheduler.step()

            # Save Model
            self.save_model(model=self.model,name="eagle",epoch=epoch,validation_loss=validation_average_loss)
        
        if DEBUG:
            print("Training Done")

    def validate_during_training(self): 
        with torch.no_grad():
            validation_average_loss=0
            for batch_index , (batch_x,batch_y) in enumerate(self.data_loader_val):
                # Move to Device
                batch_x=batch_x.to(DEVICE)
                batch_y=batch_y.to(DEVICE)

                # Forward Pass
                losses=self.model(batch_x,batch_y)
                validation_average_loss+=losses

            validation_average_loss/=(len(self.data_loader_val))
            return validation_average_loss
        
    def save_model(self,model:torch.nn.Module,name:str,epoch:int,validation_loss:float):
        '''
        Save the current state of model.
        '''
        if DEBUG:
            print("Saving "+name+"_epoch "+str(epoch+1))
        save_model(model=model,name=name+"_epoch_"+str(epoch+1))
        self.check_best_model(epoch,validation_loss,name,model)  

    def check_best_model(self,epoch:int,validation_loss:float,name:str,model:torch.nn.Module):
        '''
        Check if the current model is the best model
        '''
        if(validation_loss<=self.best_loss) :
                self.best_loss=validation_loss
                save_model(model=model,name=name+"_best")
                if DEBUG:
                    print(f"Best Model Updated: {name}_best at epoch {epoch+1} with Average validation loss: {self.best_loss:.4f}")


    # def test(self):
    #     if DEBUG:
    #         print("Testing Started")

    #     self.model.eval()
    #     with torch.no_grad():
    #         for batch_index , (batch_x,batch_y) in enumerate(self.data_loader_test):
    #             pass
    #             # # Move to Device
    #             # batch_x=batch_x.to(DEVICE)
    #             # batch_y=batch_y.to(DEVICE)

    #             # # Forward Pass
    #             # losses=self.model(batch_x,batch_y)
            
    #             # TODO add metric
            
    #     if DEBUG:
    #         print("Testing Done")








eagle_model=GRU()

trainer=EagleTrainer(model=eagle_model,real_dataset_path='data/real.npz',fake_dataset_path='data/fake.npz')

trainer.train()
# trainer.test()





    
