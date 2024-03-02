import torch.nn as nn

class GRU(nn.Module):
    def __init__(self, Tx=1998, n_freq=101):
        super(GRU, self).__init__()
        input_shape=(Tx, n_freq)
        # Define layers
        self.conv1d = nn.Conv1d(input_shape[1], 196, kernel_size=15, stride=4)
        self.batchnorm1 = nn.BatchNorm1d(196)
        self.relu = nn.ReLU()
        self.dropout1 = nn.Dropout(0.8)
        self.gru1 = nn.GRU(196, 128, bidirectional=False, batch_first=True)
        self.dropout2 = nn.Dropout(0.8)
        self.batchnorm2 = nn.BatchNorm1d(128)
        self.gru2 = nn.GRU(128, 128, bidirectional=False, batch_first=True)
        self.dropout3 = nn.Dropout(0.8)
        self.batchnorm3 = nn.BatchNorm1d(128)
        self.dropout4 = nn.Dropout(0.8)
        self.dense = nn.Linear(128, 3)
        self.softmax = nn.Softmax()

    def forward(self, x):
        # Convolutional layer
        x = self.conv1d(x)
        x = self.batchnorm1(x)
        x = self.relu(x)
        x = self.dropout1(x)

        # First GRU layer
        x, _ = self.gru1(x)
        x = self.batchnorm2(x)
        x = self.dropout2(x)

        # Second GRU layer
        x, _ = self.gru2(x)
        x = self.batchnorm3(x)
        x = self.dropout3(x)

        # x = self.dropout4(x)

        # Time-distributed dense layer
        x = self.dense(x)
        x = self.softmax(x)

        return x
