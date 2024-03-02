import torch

DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


LEARNING_RATE=0.0001
BETA_1=0.9
BETA_2=0.999
WEIGHT_DECAY=0.01
SCHEDULAR_STEP_SIZE=1
SCHEDULAR_GAMMA=0.8


SEED=42
BATCH_SIZE=2


