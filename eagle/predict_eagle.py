
import tensorflow as tf
from data import *
import keras
from keras.models import load_model

# real_dataset_path='/content/drive/MyDrive/Footprints Datasets/real.npz'
real_dataset_path='./eagle/data/real.npz'

# fake_dataset_path='/content/drive/MyDrive/Footprints Datasets/fake.npz'
fake_dataset_path='./eagle/data/fake.npz'
_,_,_,_,X_val,Y_val=Split_Data(real_dataset_path=real_dataset_path,fake_dataset_path=fake_dataset_path)


print("Minimum value",  np.min(X_val))
print("Maximum value", np.max(X_val))
X_val=preprocessing(X_val)
print("Minimum value",  np.min(X_val))
print("Maximum value", np.max(X_val))

class_weights = {0: 1.0, 1: 20.0}  # Example class weights
@keras.saving.register_keras_serializable()
# Define weighted binary cross-entropy loss function
def weighted_binary_crossentropy(y_true, y_pred):
    # Clip predicted values to prevent log(0) and log(1) cases
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)

    # Compute weighted binary cross-entropy
    weights = tf.constant([class_weights[i] for i in range(len(class_weights))])
    bce = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    return tf.reduce_mean(bce(y_true, y_pred) * weights)


loaded_model = load_model('./eagle/model_v6.h5')
loaded_model.summary()

loss, acc = loaded_model.evaluate(X_val, Y_val)
print(loss)
print(acc)
