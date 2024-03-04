import tensorflow as tf
import keras
from keras.models import load_model


@keras.saving.register_keras_serializable()
# Define weighted binary cross-entropy loss function
def weighted_binary_crossentropy(y_true, y_pred):
    class_weights = {0: 1.0, 1: 20.0}  # Example class weights
    # Clip predicted values to prevent log(0) and log(1) cases
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)

    # Compute weighted binary cross-entropy
    weights = tf.constant([class_weights[i] for i in range(len(class_weights))])
    bce = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    return tf.reduce_mean(bce(y_true, y_pred) * weights)

def get_eagle_model():
    loaded_model = load_model('./eagle/models/model_v6.h5')
    return loaded_model

# loaded_model=get_eagle_model()
# loaded_model.summary()
