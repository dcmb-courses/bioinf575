#!/usr/bin/python
"""
AI disclaimer:

Most of this script was generated with the use of AI. 
Edits were made to fix errors and add clarity.
__________

BIOINFORMATICS STATS AND MACHINE LEARNING STUDY SESSION 
SOLUTION 

This script provides detailed docstrings and inline comments explaining:
- Function calls including parameters
- Class designs and usage
- Data manipulation and machine learning steps

"""

import numpy as np
import pandas as pd
from scipy.stats import ranksums, ttest_ind
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import torch
import torch.nn as nn
import torch.optim as optim
import requests

def vectorized_ranksums(data, group_labels):
    """
    Perform Wilcoxon rank-sum test for each probe comparing two groups in a vectorized manner.

    Parameters
    ----------
    data : pd.DataFrame
        Gene expression matrix with probes as rows and samples as columns.
    group_labels : np.ndarray
        An array of group labels (e.g., 'T' for tumor, 'NB' for normal breast) with length equal to number of samples.

    Returns
    -------
    pd.Series
        P-values from Wilcoxon rank-sum test for each probe.
    """
    # Create boolean masks to select tumor and normal sample columns (vectorized indexing)
    tumor_mask = group_labels == 'T'
    normal_mask = group_labels == 'NB'

    # Select subsets of columns corresponding to tumor and normal samples
    tumor_samples = data.loc[:, tumor_mask]
    normal_samples = data.loc[:, normal_mask]

    def ranksum_probe(row):
        """
        Inner function to apply the Wilcoxon rank-sum test for one probe.
        Drops missing values in each group to ensure valid test statistic.
        Returns p-value or 1.0 if insufficient data.
        """
        vals1 = row[tumor_samples.columns].dropna()
        vals2 = row[normal_samples.columns].dropna()

        # Only perform test if both groups have at least 2 samples (requirement for ranksums)
        if len(vals1) >= 2 and len(vals2) >= 2:
            # scipy.stats.ranksums returns a namedtuple with statistic and pvalue
            return ranksums(vals1, vals2).pvalue
        return 1.0  # Conservative default p-value if insufficient data

    # Apply ranksum_probe function row-wise (axis=1) to the expression data
    # This computes rank-sum test for each probe across sample groups
    return data.apply(ranksum_probe, axis=1)

def ex1_scipy():
    """Exercise 1: Microarray differential expression analysis with detailed result interpretation."""
    print("\n" + "="*80)
    print("1️⃣ EXERCISE 1: Differential Expression Analysis (GSE3744 Microarray Dataset)")
    print("="*80)
    print("\nStepwise Guide:")
    print("1. Load the microarray dataset from GEO.")
    print("2. Assign group labels (Tumor 'T' and Normal Breast 'NB').")
    print("3. Perform Wilcoxon rank-sum test for all probes.")
    print("4. Correct for multiple testing using Bonferroni method.")
    print("5. Compare results with a parametric t-test.")
    print("6. Interpret findings considering assumptions and test conservativeness.\n")

    # Load tab-delimited GEO series data, skip GEO metadata comments (lines starting with '!')
    # header=0 ensures first line with sample names used as columns; index_col=0 sets probe IDs as row index
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE3nnn/GSE3744/matrix/GSE3744_series_matrix.txt.gz"
    raw_data = pd.read_csv(url, sep='\t', comment='!', header=0, index_col=0)

    # Define sample group labels manually: "T" for tumor (40 samples), "NB" for normal breast (7 samples)
    groups = ["T"] * 40 + ["NB"] * 7
    group_mask = np.array(groups)

    print("Data snippet (first 5 probes × first 5 samples):")
    print(raw_data.iloc[:5, :5])
    print(f"\nData shape: {raw_data.shape} (probes × samples)\n")

    print("Performing Wilcoxon rank-sum test...")
    # Vectorized ranksums test returns p-values per probe comparing tumor vs normal
    pvals = vectorized_ranksums(raw_data, group_mask)
    print("Top 5 uncorrected p-values:")
    print(pvals.nsmallest(5).round(6).to_string())
    print()

    # Multipletests performs multiple hypothesis test correction:
    # method='bonferroni' applies Bonferroni correction which divides alpha (0.05) by number of tests (probes)
    reject, corrected_pvals, _, _ = multipletests(pvals, method='bonferroni', alpha=0.05)
    print("Top 5 Bonferroni-corrected p-values:")
    # Align corrected p-values with original probe indices for display
    print(pd.Series(corrected_pvals, index=pvals.index).nsmallest(5).round(6).to_string())
    print(f"\nNumber of significant probes (Bonferroni corrected α=0.05): {np.sum(reject)} of {len(pvals)}")
    print("Interpretation: Wilcoxon test is non-parametric and generally conservative.\n")

    print("Running Welch's T-test (parametric alternative)...")
    # Welch's t-test compares means assuming unequal variances
    # axis=1 applies test gene-wise across samples
    ttest_pvals = ttest_ind(
        raw_data.loc[:, group_mask == "T"],
        raw_data.loc[:, group_mask == "NB"],
        axis=1,
        equal_var=False  # Welch adjustment for unequal variance
    ).pvalue

    reject_ttest, corrected_pvals_ttest, _, _ = multipletests(ttest_pvals, method='bonferroni', alpha=0.05)
    print("Top 5 uncorrected t-test p-values:")
    print(np.sort(ttest_pvals)[:5])
    print("Top 5 Bonferroni-corrected t-test p-values:")
    print(np.sort(corrected_pvals_ttest)[:5])
    print(f"\nNumber of significant probes (T-test, Bonferroni corrected α=0.05): {np.sum(reject_ttest)} of {len(ttest_pvals)}")
    print("Interpretation: T-test is less conservative but assumes normality and equal variance, which may inflate false positives.\n")

def ex2_sklearn():
    """Exercise 2: Breast cancer classification with logistic regression and interpretation."""
    print("\n" + "="*80)
    print("2️⃣ EXERCISE 2: Breast Cancer Classification (Logistic Regression)")
    print("="*80)

    data = load_breast_cancer()
    # Convert numpy array of features to pandas DataFrame with feature names for clarity
    df = pd.DataFrame(data.data, columns=data.feature_names)

    print("Data snippet (first 5 samples × first 5 features):")
    print(df.head())
    print(f"\nData shape: {df.shape} (samples × features)")
    # Count of each target (0=benign, 1=malignant) for class balance inspection
    print(f"Label distribution (benign, malignant): {np.bincount(data.target)}\n")

    # Split dataset into 70% training and 30% testing with stratification to maintain class ratio
    # random_state=42 fixes random seed for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(
        data.data,
        data.target,
        test_size=0.3,
        stratify=data.target,
        random_state=42,
    )

    # StandardScaler normalizes features by removing the mean and scaling to unit variance
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)  # Fit scaler only on training data
    X_test_scaled = scaler.transform(X_test)        # Apply same scaling to test data

    # LogisticRegression with max_iter=1000 to ensure convergence, random_state for reproducibility
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)  # Train classifier on normalized training data

    predictions = model.predict(X_test_scaled)  # Predict labels for test set
    accuracy = accuracy_score(y_test, predictions)  # Compute classification accuracy
    print(f"Test Accuracy: {accuracy:.3f}")
    print("Interpretation: The logistic regression model shows strong ability to classify malignant vs benign tumors based on biopsy features.\n")

def ex3_keras():
    """Exercise 3: Variant impact prediction with neural network, including data snippet and result interpretation."""
    print("\n" + "="*80)
    print("3️⃣ EXERCISE 3: Variant Impact Prediction Using Neural Network")
    print("="*80)

    # Seed for reproducible pseudo-random number generation
    np.random.seed(42)
    # Define biologically relevant synthetic feature names for rows in DataFrame display
    feat_names = [
        "conservation",
        "allele_freq",
        "func_class",
        "splice_dist",
        "gc_content",
        "motif_score",
        "evol_rate",
        "constraint",
    ]
    # Generate synthetic feature matrix of 200 variants × 8 features from standard normal distribution
    X = np.random.randn(200, 8)  
    # Synthetic target: non-linear mapping of first 4 features absolute sum through tanh scaled between 0 and 1
    y = np.tanh(np.abs(np.sum(X[:, :4], axis=1)))  

    print("Data snippet (first 5 variants):")
    print(pd.DataFrame(X[:5], columns=feat_names).round(3))
    print("Target pathogenicity scores (first 5):")
    print(pd.Series(y[:5]).round(3))
    print()

    # Split data into training (80%) and testing (20%) subsets for unbiased evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define feedforward neural network with Keras sequential API:
    # Input layer matches 8 input features, hidden layer with 32 ReLU neurons, and single output neuron for regression
    model = Sequential(
        [
            Input(shape=(8,)),
            Dense(32, activation="relu"),
            Dense(1),  # Regression output (continuous)
        ]
    )

    # Compile model to use Adam optimizer and mean squared error loss; track mean absolute error metric
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    # Train model silently for 20 epochs with batch size 16 for mini-batches optimization
    model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=0)

    # Evaluate model on test set, extracting MAE to gauge average error magnitude
    mae = model.evaluate(X_test, y_test, verbose=0)[1]
    print(f"Test MAE: {mae:.3f}")
    print(
        "Interpretation: Mean Absolute Error (MAE) quantifies average prediction error magnitude; lower values indicate better predictions.\n"
    )

def ex4_pytorch():
    """Exercise 4: Protein secondary structure classification with PyTorch NN, including data snippet and interpretation."""
    print("\n" + "="*80)
    print("4️⃣ EXERCISE 4: Protein Secondary Structure Prediction (PyTorch NN)")
    print("="*80)

    # Seed NumPy RNG for reproducibility
    np.random.seed(42)
    n_samples = 2000

    # Define amino acid single letter codes for column naming
    aa_labels = list("ACDEFGHIKLMNPQRSTVWY")

    # Generate synthetic residue features; each residue represented by 20-dimensional AA probability vector
    X = np.random.rand(n_samples, 20)  
    # Generate synthetic structure labels for helix(0), sheet(1), coil(2)
    y = np.random.choice([0, 1, 2], n_samples)  

    print("Data snippet (first 5 residues):")
    print(pd.DataFrame(X[:5], columns=aa_labels).round(3))
    print("Secondary structure labels (0=helix, 1=sheet, 2=coil):")
    print(pd.Series(y[:5]).map({0: "helix", 1: "sheet", 2: "coil"}))
    print()

    # Stratified split to preserve class proportions in train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2
    )

    class ProteinNet(nn.Module):
        """Two-layer feedforward neural network for secondary structure classification."""

        def __init__(self):
            # Initialize nn.Module parent class
            super().__init__()
            # Fully connected first layer from 20 input features to 32 neurons
            self.fc1 = nn.Linear(20, 32)  
            # Final output layer mapping 32 neurons to 3 classes (helix, sheet, coil)
            self.fc2 = nn.Linear(32, 3)  

        def forward(self, x):
            # Apply ReLU non-linearity after first layer, then linear output layer (logits)
            x = torch.relu(self.fc1(x))
            return self.fc2(x)  

    # Instantiate neural network model
    model = ProteinNet()
    # Adam optimizer for gradient descent updates
    optimizer = optim.Adam(model.parameters())

    # Convert training data to PyTorch tensors
    X_train_t = torch.FloatTensor(X_train[:1000])  # Limit size for demonstration speed
    y_train_t = torch.LongTensor(y_train[:1000])

    # Simple training loop over 5 epochs
    for epoch in range(5):
        optimizer.zero_grad()  # Zero previous gradients
        logits = model(X_train_t)  # Get network outputs (logits)
        # Calculate cross-entropy loss between predicted logits and true labels
        loss = nn.CrossEntropyLoss()(logits, y_train_t)
        loss.backward()  # Backpropagate gradients
        optimizer.step()  # Gradient descent update of parameters

    # Evaluate on test data without gradient tracking for efficiency
    with torch.no_grad():
        X_test_t = torch.FloatTensor(X_test[:500])
        y_test_t = torch.LongTensor(y_test[:500])
        pred = model(X_test_t).argmax(1)  # Predicted class as max logit index
        accuracy = (pred == y_test_t).float().mean()  # Calculate average correct predictions

    print(f"Test Accuracy: {accuracy:.3f}")
    print(
        "Interpretation: Accuracy reflects how well the NN predicts secondary structure states from AA probability features. Random labels limit performance.\n"
    )

def ex5_uniprot():
    """Exercise 5: Retrieve protein annotation from UniProt API; robust error handling and interpretation."""
    print("\n" + "="*80)
    print("5️⃣ EXERCISE 5: UniProt Protein Annotation via REST API")
    print("="*80)

    protein_id = "P69905"  # Human hemoglobin alpha chain
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"

    try:
        # Send HTTP GET request to UniProt REST API; timeout after 10 seconds
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx/5xx)
        data = response.json()  # Parse JSON from response body

        # Safely extract nested dictionary keys with .get() to avoid errors on missing fields
        name = (
            data.get("proteinDescription", {})
            .get("recommendedName", {})
            .get("fullName", {})
            .get("value", "N/A")
        )
        organism = data.get("organism", {}).get("scientificName", "N/A")
        length = data.get("sequence", {}).get("length", "N/A")

        print("Protein Annotation:")
        print(f"Name: {name}")
        print(f"Organism: {organism}")
        print(f"Sequence Length: {length} amino acids\n")
    except requests.exceptions.RequestException as e:
        # Catch network problems, timeouts, or HTTP errors gracefully
        print(f"API request failed: {e}")


if __name__ == "__main__":
    # Run all exercises sequentially
    ex1_scipy()
    ex2_sklearn()
    ex3_keras()
    ex4_pytorch()
    ex5_uniprot()

    print("🎓 COMPLETE BIOINFORMATICS ML PIPELINE - ALL EXERCISES EXECUTED")
