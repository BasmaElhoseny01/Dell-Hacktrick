import torch
import numpy as np
import random

# Fixing the seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)

def save_model(model,name):
    '''
    Save the X-Reporto model to a file.

    Args:
        model(nn): model to be saved
        name (str): Name of the model file.
    '''
    torch.save(model.state_dict(), "models/" + str(RUN) + '/' + name + ".pth")

def load_model(model,name):
    '''
    Load the X-Reporto model from a file.

    Args:
        model(nn): model to be loaded
        name (str): Name of the model file.
    '''
    model.load_state_dict(torch.load("models/" + str(RUN) + '/' + name + ".pth"))

def seed_worker(worker_id):
    """To preserve reproducibility for the randomly shuffled train loader."""
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)



