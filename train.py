import tensorflow as tf
import numpy as np

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Reshape the input data to have shape (num_samples, 784)
x_train = x_train.reshape((x_train.shape[0], 784))
x_test = x_test.reshape((x_test.shape[0], 784))

# Normalize the input data to have values between 0 and 1
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Define x and y
x = x_train
y = y_train
# Create a Sequential model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),  # specify input shape
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),  # specify input shape
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)  # assume 10-class classification problem
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Print the model summary
model.summary()

# Make predictions on the first sample of the training set
predictions = model(x_train[:1]).numpy()
print(tf.nn.softmax(predictions).numpy())

# Fit the model to the training data for 5 epochs
model.fit(x_train, y_train, epochs=5)

# Evaluate the model on the test data
model.evaluate(x_test, y_test, verbose=2)

# Create a new model that wraps the original model and adds a softmax layer
probability_model = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()
])

# Make predictions on the first 5 samples of the test set using the probability_model
probability_model(x_test[:5])