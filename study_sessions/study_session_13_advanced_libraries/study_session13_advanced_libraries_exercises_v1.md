# Bioinformatics Machine Learning Exercises:

AI disclaimer:

Most of this file was generated with the use of AI. 
Edits were made to fix errors and add clarity.

## Table of Contents
- [Exercise 1: Differential Expression Analysis](#exercise-1)
- [Exercise 2: Tumor Classification](#exercise-2)
- [Exercise 3: Variant Impact Prediction](#exercise-3)
- [Exercise 4: Protein Secondary Structure Prediction](#exercise-4)
- [Exercise 5: Protein Annotation Retrieval](#exercise-5)

---

## Exercise 1: Differential Expression Analysis (GSE3744 Microarray Dataset)

### Stepwise Guide
1. Load GSE3744 Affymetrix microarray dataset from NCBI GEO database
2. Format data matrix: rows = 54,613 probes, columns = 47 patient samples
3. Assign clinical phenotype labels: 40 Tumor ('T'), 7 Normal Breast ('NB')
4. Apply vectorized Wilcoxon rank-sum test (non-parametric) for each probe
5. Perform Bonferroni multiple testing correction across all probes
6. Run Welch's t-test comparison (parametric) and interpret differences

### Data Description
- **Rows**: Affymetrix probe IDs (short DNA sequences targeting transcripts)
- **Columns**: Patient sample IDs with log2-normalized fluorescence intensities
- **Goal**: Identify probes differentially expressed between tumor vs normal tissue

### Key Functions & Parameters
- `pd.read_csv(url, sep='\t', comment='!', header=0, index_col=0)`  
- `multipletests(pvals, method='bonferroni', alpha=0.05)`  
- `ttest_ind(group1, group2, axis=1, equal_var=False)`  

### Result Interpretation
- Wilcoxon is robust to non-normality but conservative.
- Welch's t-test is more powerful but assumes normality and equal variance.

### Next Steps
- Probe → gene annotation  
- GO/KEGG enrichment pathway analysis  
- Volcano plots visualization  
- Survival analysis and clinical correlations  

---

## Exercise 2: Tumor Classification (Breast Cancer Dataset)

### Stepwise Guide
1. Load Wisconsin Breast Cancer dataset (569 samples × 30 tumor features)
2. Split 70/30 train/test with stratification
3. Normalize features using StandardScaler
4. Train LogisticRegression classifier on training set
5. Evaluate accuracy on test set

### Data Description
- Quantitative tumor features like texture, shape, size
- Binary target: benign (0) or malignant (1)

### Key Functions & Parameters
- `train_test_split(test_size=0.3, stratify=y, random_state=42)`  
- `StandardScaler()`  
- `LogisticRegression(max_iter=1000, random_state=42)`  

### Result Interpretation
- High accuracy (~95%) shows good feature predictiveness.
- Logistic regression provides interpretable coefficients for clinical assays.

### Next Steps
- Apply k-fold cross-validation  
- Feature importance ranking (coefficients, LASSO)  
- Clinical outcome prediction models  
- ROC/AUC curve plotting  
- Model interpretability using SHAP values  

---

## Exercise 3: Variant Impact Prediction (Neural Network Regression)

### Stepwise Guide
1. Simulate variant features capturing biological metrics
2. Define continuous impact/pathogenicity scores
3. Split data into training/testing sets (80/20)
4. Build simple feedforward Keras model (8 input features)
5. Train with Adam optimizer and MSE loss
6. Evaluate test MAE metric

### Data Description
- Synthetic conservation, allele frequency, function-related features
- Continuous target scores (0-1) stand for pathogenic impact

### Key Functions & Parameters
- `Sequential([Input(8), Dense(32, 'relu'), Dense(1)])`  
- `model.compile(optimizer='adam', loss='mse', metrics=['mae'])`  
- `model.fit(...)`  

### Result Interpretation
- MAE measures average absolute error; lower indicates better regression fit.

### Next Steps
- Replace with real variant databases like ClinVar, gnomAD  
- Test advanced architectures (CNNs, LSTMs, Transformers)  
- Benchmark against state-of-the-art predictors (AlphaMissense)  
- Develop ensemble models for improved robustness  

---

## Exercise 4: Protein Secondary Structure Prediction (PyTorch Classification)

### Stepwise Guide
1. Generate synthetic residue AA probability features (20 features)
2. Assign 3-class secondary structure labels randomly
3. Perform stratified train/test split (80/20)
4. Define custom nn.Module with 20→32→3 neurons
5. Train using CrossEntropyLoss and Adam optimizer (5 epochs)
6. Evaluate test accuracy

### Data Description
- Features model PSSM profiles of residues
- Labels correspond to secondary structures: helix, sheet, coil

### Key Functions & Parameters
- `ProteinNet(nn.Module)` class definition  
- Optimizer: `optim.Adam(model.parameters())`  
- Loss: `nn.CrossEntropyLoss()`  

### Result Interpretation
- Accuracy shows ability to predict structure states
- Random labels yield low meaningful accuracy; real data needed

### Next Steps
- Use curated PSSM datasets (CASP, CB513)  
- Experiment with CNN and RNN models  
- Integrate with AlphaFold predictions for 3D structure  
- Explore transfer learning for improved accuracy  

---

## Exercise 5: Protein Annotation Retrieval (UniProt REST API)

### Stepwise Guide
1. Select UniProt protein accession code (e.g., P69905)
2. Construct REST URL for JSON metadata
3. HTTP GET request with timeout and error handling
4. Parse JSON to extract protein name, organism, sequence length
5. Display information

### Data Description
- JSON response includes curated protein functional and taxonomic data

### Key Functions & Parameters
- `requests.get(url, timeout=10)`  
- `response.raise_for_status()`  
- Nested `.get()` dictionary safely access JSON keys

### Result Interpretation
- Provides rapid programmatic access to rich protein annotations
- Error handling enables robust computational pipelines

### Next Steps
- Batch protein annotation queries via API scripts  
- Map annotations to pathways and 3D structures  
- Integrate protein-protein interaction networks for systems biology  

---

## Advanced Extensions

- Hyperparameter tuning (GridSearchCV, Optuna, Bayesian optimization)  
- Cross-validation (k-fold, stratified, time-series)  
- Model interpretability (SHAP, LIME, permutation importance)  
- Ensemble learning (XGBoost, stacking, voting classifiers)  
- Pipeline deployment (FastAPI, Docker containers, MLflow)  
- Using real-world large datasets (TCGA, GTEx, UK Biobank)  
- Workflow automation tools (Snakemake, Nextflow, Apache Airflow)  

---


