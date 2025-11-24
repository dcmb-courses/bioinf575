# Script created with the use of perplexity.ai.
# Checked and updated for correctness and clarity.

# ============================================================
# Exercise 1: SciPy -- ANOVA on Iris Data
# ============================================================

print("EXERCISE 1")
print("Checking for differences between the sepal lengths of 3 species of iris flowers.")
print("Data set contains 50 flowers of each species and measurements for: petal and sepal length, and petal and sepal width.")

# Step 1: Load the Iris dataset.
# We use load_iris() from scikit-learn, which gives us a well-known flower dataset
# already split into features (measurements) and labels (species).
from sklearn.datasets import load_iris

# Call load_iris() to actually get the data object.
# 'data.data' holds the numeric measurements, and 'data.target' holds the species codes (0,1,2).
data = load_iris()
X = data.data      # All numeric measurements for each flower
y = data.target    # Species label for each flower
print("All numeric measurements for each flower:")
print(X)
print()
print("Species label for each flower:")
print("0-setosa, 1-versicolor, 2-virginica")
print(y)
print()

# Step 2: Import the one-way ANOVA function.
# f_oneway() from scipy.stats compares the means of 2+ groups and tells us if at least
# one group mean is different (via an F-statistic and p-value).
from scipy.stats import f_oneway

# Step 3: Build separate groups for each species.
# Here we filter rows of X using y == 0, y == 1, y == 2 to get sepal length only.
# X[:, 0] selects the first column (sepal length).
group_1 = X[y == 0, 0]  # Sepal length of setosa
group_2 = X[y == 1, 0]  # Sepal length of versicolor
group_3 = X[y == 2, 0]  # Sepal length of virginica

# Step 4: Run one-way ANOVA on the three groups.
# f_oneway() takes each group as a separate argument and returns:
#   stat: the F-statistic (how large the between-group variance is vs within-group variance)
#   p:    the p-value (how likely such a difference is under "no real difference")
stat, p = f_oneway(group_1, group_2, group_3)

# Step 5: Print the results so we can see them.
# print() writes text and values to the console so students can inspect the output.
print("SciPy Exercise: Iris Sepal Length ANOVA")
print("F-statistic:", stat, "p-value:", p)
# Interpretation note:
# If the p-value is very small (for example < 0.05), it suggests at least one species
# has a different average sepal length from the others.


# ============================================================
# Exercise 2: scikit-learn -- KNN Classification on Iris Data
# ============================================================

print("EXERCISE 2")
print("Creating a classifier on a dataset of three species of iris flowers.")
print("Data set contains 50 flowers of each species and measurements for: petal and sepal length, and petal and sepal width.")

# Step 1: Split data into training and test sets.
# train_test_split() randomly divides X and y into a part used to train the model
# and a separate part used to test how well it generalizes.
from sklearn.model_selection import train_test_split

# Use train_test_split() with 70% for training, 30% for testing.
# random_state fixes the shuffle so we get the same split every time (reproducibility).
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.7, random_state=42
)

print("\nscikit-learn Exercise: Data Split")
print("Training samples:", len(X_train), "Testing samples:", len(X_test))
# Reason for splitting:
# We want to detect overfitting by evaluating performance on data not seen during training.

# Step 2: Import the KNN classifier.
# KNeighborsClassifier implements the k-nearest neighbors algorithm, a simple method
# that classifies a point based on the majority class of its closest neighbors.
from sklearn.neighbors import KNeighborsClassifier

# Step 3: Create a KNN model object.
# We set n_neighbors=5, meaning we will look at the 5 closest training points
# to decide the class of a new point.
knn = KNeighborsClassifier(n_neighbors=5)

# Step 4: Train (fit) the KNN classifier.
# The fit() method lets the model "learn" from the training data (here it stores
# the samples so it can compute neighbors later).
knn.fit(X_train, y_train)

# Step 5: Make predictions on the test set.
# predict() takes new feature vectors (X_test) and returns the model's guessed labels.
y_pred = knn.predict(X_test)
print("Predicted test labels:", y_pred)
print("Real lables:", y_test)
print("0-setosa, 1-versicolor, 2-virginica")
print()

# Step 6: Evaluate model accuracy.
# accuracy_score() compares the true labels (y_test) with the predicted labels (y_pred)
# and returns the fraction of correct predictions.
from sklearn.metrics import accuracy_score

acc = accuracy_score(y_test, y_pred)
print("Test set accuracy:", acc)
# A high accuracy means this simple KNN model works well on the Iris dataset.


# ============================================================
# Exercise 3: Keras -- MNIST Image Classification with CNN
# ============================================================

# MNIST dataset is a dataset of 60,000 28x28 grayscale images of the 10 digits, along with a test set of 10,000 images. 
# Pixel values: Grayscale values from 0 (black) to 255 (white).
# Labels: An integer from 0 to 9 for each image. 

print("EXERCISE 3")
print("Creating a classifier on a handwritten image dataset.")

# Step 1: Load the MNIST dataset.
# mnist.load_data() returns training and test images (28x28 grayscale digits) and labels (0–9).
from keras.datasets import mnist

(X_train_mnist, y_train_mnist), (X_test_mnist, y_test_mnist) = mnist.load_data()
print("\nKeras Exercise: MNIST Data Loaded")
print("Training data shape:", X_train_mnist.shape, "Test data shape:", X_test_mnist.shape)
# MNIST is a standard dataset to practice image classification.

# Visualize an image.
# Select the first element in the train_set collection.
# import matplotlib 
# use imshow function from pyplot with the selected element 
# use plt.show() to display the image

image_to_visualize = X_train_mnist[0]

from matplotlib import pyplot as plt

plt.imshow(image_to_visualize, cmap='gray')
plt.show()

# Step 2: One-hot encode labels and normalize images.
# to_categorical() turns integer class labels (0–9) into one-hot vectors (length 10),
# which is the usual format for multi-class classification in neural networks.
from keras.utils import to_categorical

# Reshape images to (-1, 28, 28, 1) to add a channel dimension and scale pixel values into [0, 1].
# Dividing by 255.0 converts raw 0–255 pixel values to floats between 0 and 1,
# which helps training converge more smoothly.
X_train_mnist = X_train_mnist.reshape(-1, 28, 28, 1) / 255.0
X_test_mnist = X_test_mnist.reshape(-1, 28, 28, 1) / 255.0

# One-hot encode the labels so each label is a vector indicating the correct class.
# use the to_categorical function
y_train_mnist = to_categorical(y_train_mnist)
y_test_mnist = to_categorical(y_test_mnist)
print("Data normalized and labels one-hot encoded.")

# Step 3: Import model and layer classes.
# Sequential lets us build a model layer-by-layer in a list.
# Conv2D, MaxPooling2D, Flatten, and Dense are standard building blocks of CNNs.
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Step 4: Define a simple CNN.
# We pass a list of layers to Sequential, in the order data flows through them.
# Conv2D: learns small filters to detect patterns in the image.
# parameters are: 8, kernel_size=3, activation='relu', input_shape=(28, 28, 1)
# MaxPooling2D: reduces spatial size, keeps strongest activations.
# parameter: 2
# Flatten: converts 2D feature maps into a 1D vector.
# Dense: standard fully connected layer; last one uses softmax to output probabilities over 10 digits.
# parameters: 32, activation='relu'
# parameters: 10, activation='softmax'

mnist_model = Sequential([
    Conv2D(8, kernel_size=3, activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(2),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(10, activation='softmax')
])

# Step 5: Compile the model.
# compile() tells Keras which optimizer, loss function, and metrics to use.
# 'adam' is a popular optimizer; 'categorical_crossentropy' is standard for multi-class,
# and 'accuracy' is a metric easy to interpret so we use it in the list of metrics.
mnist_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 6: Train the model.
# fit() runs the training loop for a given number of epochs and batch size.
# validation_data lets us monitor performance on held-out data after each epoch.
# Use 3 epochs and a batch size of 64.
mnist_history = mnist_model.fit(
    X_train_mnist,
    y_train_mnist,
    epochs=3,
    batch_size=64,
    validation_data=(X_test_mnist, y_test_mnist)
)

# Step 7: Inspect validation accuracy from the training history.
# history.history is a dictionary; 'val_accuracy' is a list, one value per epoch.
print("CNN Validation accuracy after 3 epochs:")
print(mnist_history.history['val_accuracy'][-1])
print()
# This tells us how well the CNN recognizes digits on unseen test images.


# ============================================================
# Exercise 4: PyTorch -- DNA Sequence Classification (Bioinformatics)
# ============================================================

# Step 1: Import PyTorch and NumPy utilities.
# torch is the main PyTorch library; nn has neural network layers and losses;
# optim has optimizers; numpy is used to generate and handle synthetic data easily.
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Step 2: Define a data generator for synthetic DNA sequences.
# This function creates random DNA sequences and labels them based on whether they
# contain a specific motif ('TATA'). It also converts sequences into one-hot encodings.
def generate_dna_data(samples=1000, seq_len=50):
    np.random.seed(42)  # Fix random seed to make results repeatable.

    # Randomly select nucleotides A/C/G/T for each position in each sequence.
    seqs = np.random.choice(list("ACGT"), size=(samples, seq_len))

    # For labels: 1 if sequence contains 'TATA', otherwise 0.
    # We join characters into a string per sequence and check if 'TATA' is present.
    labels = np.array(['TATA' in ''.join(seq) for seq in seqs], dtype=int)

    # One-hot encode nucleotides:
    # mapping gives each base an index; we make a 3D array [samples, seq_len, 4].
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    onehot = np.zeros((samples, seq_len, 4), dtype=np.float32)
    for i in range(samples):
        for j in range(seq_len):
            onehot[i, j, mapping[seqs[i, j]]] = 1.0

    return onehot, labels

# Step 3: Generate the dataset.
# X is the one-hot encoded sequences, y is the 0/1 labels.
X_dna, y_dna = generate_dna_data()
print("\nPyTorch Exercise: Synthetic DNA Data")
print("Sample shape:", X_dna.shape, "Labels shape:", y_dna.shape)
# Each sequence becomes a matrix of length 50 with 4 channels for A/C/G/T.

# Step 4: Split into training and test sets (80/20).
# We manually compute the split index and slice arrays.
split = int(0.8 * X_dna.shape[0])
X_train_dna, X_test_dna = X_dna[:split], X_dna[split:]
y_train_dna, y_test_dna = y_dna[:split], y_dna[split:]

# Step 5: Convert NumPy arrays into PyTorch tensors.
# torch.tensor() creates tensors from NumPy arrays so they can be used in PyTorch models.
# unsqueeze(1) adds a column dimension for the label data after calling the float method.
X_train_t = torch.tensor(X_train_dna)
y_train_t = torch.tensor(y_train_dna).float().unsqueeze(1)  
X_test_t = torch.tensor(X_test_dna)
y_test_t = torch.tensor(y_test_dna).float().unsqueeze(1)

# Step 6: Define a simple 1D CNN for sequence classification.
# We create a subclass of nn.Module; this is the standard way to define custom models in PyTorch.
class DNAClassifierCNN(nn.Module):
    # __init__ sets up the layers once.
    def __init__(self):
        super().__init__()
        # Conv1d scans along the sequence length dimension.
        # in_channels=4 because we one-hot encoded 4 bases; out_channels=8 means 8 filters;
        # kernel_size=4 means each filter looks at 4 positions at a time.
        self.conv = nn.Conv1d(in_channels=4, out_channels=8, kernel_size=4)
        # After convolution, we flatten and use a fully connected layer.
        # (50-4+1) is the length after valid convolution; multiply by 8 channels.
        self.fc = nn.Linear((50 - 4 + 1) * 8, 1)

    # forward(x) defines how data flows through the layers when we call model(x).
    def forward(self, x):
        # Input x is [batch, seq_len, channels]; Conv1d expects [batch, channels, seq_len],
        # so we transpose the last two dimensions.
        x = x.transpose(1, 2)
        # Apply convolution followed by ReLU nonlinearity.
        x = torch.relu(self.conv(x))
        # Flatten to [batch, features].
        x = x.view(x.size(0), -1)
        # Final linear layer + sigmoid to get probability between 0 and 1.
        x = torch.sigmoid(self.fc(x))
        return x

# Step 7: Create the model, loss function, and optimizer.
# DNAClassifierCNN() instantiates our defined network.
dna_model = DNAClassifierCNN()

# BCELoss (binary cross-entropy) is suitable for binary classification with outputs in [0, 1].
criterion = nn.BCELoss()

# SGD is a basic optimizer that updates model parameters using gradients.
# We pass model.parameters() so it knows what to update, and set a small learning rate.
optimizer = optim.SGD(dna_model.parameters(), lr=0.01)

# Step 8: Train the model for several epochs.
for epoch in range(10):
    # Zero gradients from the previous step; this is required before backprop in PyTorch.
    optimizer.zero_grad()

    # Forward pass: compute model predictions on the training data.
    y_pred_dna = dna_model(X_train_t)

    # Compute the loss between predicted probabilities and true labels.
    loss = criterion(y_pred_dna, y_train_t)

    # Backward pass: compute gradients of loss with respect to model parameters.
    loss.backward()

    # Apply one optimization step to update parameters.
    optimizer.step()

    print(f"Epoch {epoch+1}: Training loss = {loss.item():.4f}")

# Step 9: Evaluate on the test set.
# no_grad() tells PyTorch we are only doing inference, so it skips gradient tracking for speed.
with torch.no_grad():
    # run the dna model on the test data
    dna_predictions = dna_model(X_test_t)
    # Convert probabilities to class predictions by thresholding at 0.5.
    predicted_classes = (dna_predictions > 0.5).float()
    # Compare predicted_classes to y_test_t to compute accuracy.
    test_acc = (predicted_classes.eq(y_test_t)).float().mean().item()
    print("DNA classification test accuracy:", test_acc)
# A good accuracy indicates the model has learned to detect the 'TATA' motif.


# ============================================================
# Exercise 6: Subprocess - Running External Bioinformatics Software from Python
# ============================================================

# Goal:
# Show how Python can call external command-line bioinformatics tools and
# then read their output into Python structures (like pandas DataFrames).

# Step 1: Import helper libraries.
# subprocess lets Python run shell commands as if typed in a terminal.
import subprocess

# pandas is a data analysis library; DataFrame is its main table-like structure.
import pandas as pd

# Note:
# You must have 'seqkit' installed separately (for example via conda) for this to work.
# Example: conda install -c bioconda seqkit

# Step 2: Define the input FASTA file.
# This should be a file on disk containing DNA sequences in FASTA format.
fasta_file = "example.fasta"

# Step 3: Build the command we want to run.
# We put each part of the command in a list so subprocess can handle spaces safely.
# This corresponds to: seqkit stats example.fasta
command = ["seqkit", "stats", fasta_file]

# Step 4: Run the command from Python.
# subprocess.run() executes the external command.
# capture_output=True tells it to keep the command's output instead of printing it directly.
# text=True tells it to decode bytes into a regular Python string (result.stdout).
result = subprocess.run(command, capture_output=True, text=True)

# Step 5: Check if the command succeeded and handle output.
# result.returncode == 0 means the command completed without error.
if result.returncode == 0:
    print("\nSubprocess Exercise: Sequence file stats")
    # Print the raw text output from seqkit so students can see what the tool prints.
    print(result.stdout)

    # Step 6: Convert the text output into a pandas DataFrame.
    # StringIO wraps the text so read_csv() can read it as if it were a file.
    data_io = io.StringIO(result.stdout)

    # read_csv() reads tabular data into a DataFrame.
    # We specify '\n' because rows are separated by new lines
    # break the string into lines
    l = result.stdout.strip().split("\n")
    # break the lines into individual elements
    ll = [s.split() for s in l]
    # create dataframe from list of lists
    df = pd.DataFrame(ll)
    # reset header to first row
    # save first row data in a variable
    new_header = df.iloc[0]
    # remove forst row - subset not using the first row
    df = df[1:] 
    # reset index so row lablels are not misslabeled
    df = df.reset_index(drop=True)
    # set the new header
    df.columns = new_header
    print("Display resulting dataframe size and content.")
    print(df.shape)
    print(df)
    # Now df can be filtered, plotted, or merged with other data in Python.
else:
    # If something went wrong, show an error message and the stderr output.
    print("Error running seqkit. Ensure 'seqkit' is installed and 'example.fasta' exists.")
    print(result.stderr)

# Explanation of why we use subprocess here:
# Many important bioinformatics tools only exist as command-line programs.
# The subprocess module lets a Python script call those tools, capture their output,
# and integrate them with Python-based analysis, enabling automated and reproducible pipelines.
