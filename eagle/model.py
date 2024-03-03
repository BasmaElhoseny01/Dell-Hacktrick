import torch.nn as nn
from torchsummary import summary
import torch
class GRU(nn.Module):
    def __init__(self, Tx=1998, n_freq=101):
        super(GRU, self).__init__()
        self.conv1d = nn.Conv1d(in_channels=n_freq, out_channels=196, kernel_size=15, stride=4)
        self.batchnorm1 = nn.BatchNorm1d(num_features=196)
        self.relu = nn.ReLU()
        self.dropout1 = nn.Dropout(p=0.8)

        # input_size parameter specifies the number of expected features in the input.
        self.gru1 = nn.GRU(input_size=196, hidden_size=128, num_layers=2,bidirectional=False, batch_first=True)
        # self.dropout2 = nn.Dropout(0.8)
        self.batchnorm2 = nn.BatchNorm1d(128)

        # self.gru2 = nn.GRU(128, 128, bidirectional=False, batch_first=True)
        # self.dropout3 = nn.Dropout(0.8)
        # self.batchnorm3 = nn.BatchNorm1d(128)
        # self.dropout4 = nn.Dropout(0.8)
        # self.dense = nn.Linear(128, 3)
        # # self.softmax = nn.Softmax()

    def forward(self, x):
        print(x.shape)
        # if x.ndim == 4:
        #     x=x[0,:,:,:]
        # Convolutional layer
        x = self.conv1d(x)
        print(x.shape)
        x = self.batchnorm1(x)
        print(x.shape)
        x = self.relu(x)
        print(x.shape)
        x = self.dropout1(x)
        print(x.shape)



        # First GRU layer
        x, _ = self.gru1(x)  
        x = self.batchnorm2(x)
        x = self.dropout2(x)
        print(x.shape)


        # print(x.shape)
        # # Second GRU layer
        # x, _ = self.gru2(x)
        # x = self.batchnorm3(x)
        # x = self.dropout3(x)

        # x = self.dropout4(x)

        # # Time-distributed dense layer
        # # x = self.dense(x)
        # # x = self.softmax(x)

        return x


# # Initialize the model
model = GRU()
model.to('cuda')

random_data = torch.randn((2, 101,5511))  # Batch size, in_channels, input_length
random_data=random_data.to('cuda')
model(random_data)


# # # Print the model summary
# summary(model, input_size=(2, 101, 1998))