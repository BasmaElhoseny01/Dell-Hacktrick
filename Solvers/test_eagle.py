import numpy as np
from Solvers.get_eagle import get_eagle_model
import time

def check_conectiave_ones(y):
    consecutive_ones = 0
    for num in y:
        if num == 1:
            consecutive_ones += 1
            if consecutive_ones >= 10:
                break
        else:
            consecutive_ones = 0
    if consecutive_ones >= 10:
        return True
    else: return False

def select_channel(footprint,eagle):
    '''
    According to the footprint you recieved (one footprint per channel)
    you need to decide if you want to listen to any of the 3 channels or just skip this message.
    Your goal is to try to catch all the real messages and skip the fake and the empty ones.
    Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.        
    '''
    timestamp = str(int(time.time()))
    np.save(f'/content/footprint_{timestamp}.npy', footprint)
    # footprint is a numpy array [(1998,101)]
    # Preprocessing
    footprint[np.isinf(footprint)] = 65500.0
    footprint[np.isinf(footprint)] = 65500.0
    footprint[footprint > 65500.0] = 65500.0
    
    footprint=footprint.astype(np.uint16)
    footprint=footprint.astype(np.float16)/(2.0**16)

    # Remove Last Time step
    footprint=footprint[0:1997,:]

    y=eagle.predict(np.expand_dims(footprint, axis=0))

    # Threshold on the Probability
    y=y[0]>0.5

    consecutive_ones = 0
    for num in y:
        if num == 1:
            consecutive_ones += 1
            if consecutive_ones >= 10:
                break
        else:
            consecutive_ones = 0
    if consecutive_ones >= 10:
        return True
    else: return False
    
def check_result(predictions):
    gold_labels=np.load('./eagle/data/Y_val.npy')

    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0


    for i in range(len(predictions)):
        y_predict=predictions[i]
        y_gold=check_conectiave_ones(gold_labels[i])

        if y_predict and y_gold:
            true_positives += 1
        elif y_predict and not y_gold:
            false_positives += 1
        elif not y_predict and y_gold:
            false_negatives += 1
        else:
            true_negatives += 1
    print("Validation")
    print("False Positives:", false_positives)
    print("False Negatives:", false_negatives)
    print("True Positives:", true_positives)
    print("True Negatives:", true_negatives)

    # Compute recall
    recall = true_positives / (true_positives + false_negatives)

    # Compute precision
    precision = true_positives / (true_positives + false_positives)

    print("Recall:", recall)
    print("Precision:", precision)




def submit_eagle_attempt():
    prediction = np.array([], dtype=np.float64)
    # Get Eagle Model Before Initializing the Game :D
    eagle_model=get_eagle_model()
    # Getting foot prints from val set
    footprints=np.load('./eagle/data/X_val.npy')

    for footprint in footprints:
        y=select_channel(footprint,eagle_model)
        prediction=np.append(prediction,y)

    check_result(prediction)

submit_eagle_attempt()