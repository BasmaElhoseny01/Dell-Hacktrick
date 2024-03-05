def select_channel_new(footprints,channel_ids,eagle):
    '''
    According to the footprint you recieved (one footprint per channel)
    you need to decide if you want to listen to any of the 3 channels or just skip this message.
    Your goal is to try to catch all the real messages and skip the fake and the empty ones.
    Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.
    '''
    # Check Empty Channels
    if(len(channel_ids)==0): return False,None

    # footprint is a numpy array [(1998,101)]
    # Preprocessing
    footprints[np.isinf(footprints)] = 65500.0

    # Remove Last Time step
    footprints=footprints[:,0:1997,:]

    y=eagle.predict(footprints) # y is batch of 3 channels

    # Threshold on the Probability
    y_mask=y>0.5


    listen_array=np.zeros((len(channel_ids)))
    for i,mask in enumerate(y_mask):
      listen_array[i]= check_consecutive_ones(mask)
    print("listen_array",listen_array)

    if(np.sum(listen_array))==0:
        print("Select Channel(0)")
        return False,None

    if (np.sum(listen_array))>1:
        sum_masked = np.sum(y * y_mask, axis=1)
        # print("sum_masked",sum_masked)

        # Compute the count of non-zero values along the second axis
        count_nonzero = np.sum(y_mask, axis=1)

        mean_values = sum_masked / np.where(count_nonzero > 0, count_nonzero, 1)
        print("mean_values",mean_values)
        
        channel_index = np.argmax(mean_values)

        # Select the channel with the highest probability
        channel_id=channel_ids[channel_index]
        
        print("Select Channel(1)")
        return True,int(channel_id)

    else:    
        # Select the channel with the highest probability
        channel_id = channel_ids[np.argmax(listen_array)]
        print("Select Channel(1)")
        # Return the channel_id as integer
        return True,int(channel_id)
    