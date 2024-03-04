# import numpy as np
# from get_eagle import get_eagle_model


# def select_channel(footprint,eagle):
#     '''
#     According to the footprint you recieved (one footprint per channel)
#     you need to decide if you want to listen to any of the 3 channels or just skip this message.
#     Your goal is to try to catch all the real messages and skip the fake and the empty ones.
#     Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.        
#     '''
#     # footprint is a numpy array [(1998,101)]
#     # Preprocessing
#     footprint[np.isinf(footprint)] = 65500.0
#     y=eagle.predict(np.expand_dims(footprint, axis=0))

#     # Threshold on the Probability
#     y=y[0]>0.5
#     print(y.T *1)

#     consecutive_ones = 0
#     for num in y:
#         if num == 1:
#             consecutive_ones += 1
#             if consecutive_ones >= 10:
#                 break
#         else:
#             consecutive_ones = 0
#     if consecutive_ones >= 10:
#         return True
#     else: return False
#     pass

# eagle_model=get_eagle_model()
# footprint=np.load('./eagle/data/X_train.npy')[0]
# print(np.shape(footprint))
# print(select_channel(footprint,eagle_model))

# print("Gold",np.load('./eagle/data/Y_train.npy')[0])
