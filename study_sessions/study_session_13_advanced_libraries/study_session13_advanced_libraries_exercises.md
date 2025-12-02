# Bioinformatics Machine Learning Exercises:

AI disclaimer:

Most of this file was generated with the use of AI. 
Edits were made to fix errors and add clarity.

## Table of Contents
- [Exercise 1: Differential Expression Analysis](#exercise-1-differential-expression-analysis)
- [Exercise 2: Tumor Classification](#exercise-2-tumor-classification)
- [Exercise 3: Variant Impact Prediction](#exercise-3-variant-impact-prediction)
- [Exercise 4: Protein Secondary Structure Prediction](#exercise-4-protein-secondary-structure-prediction)
- [Exercise 5: Protein Annotation Retrieval](#exercise-5-protein-annotation-retrieval)

## Exercise 1: Differential Expression Analysis Using Microarray Data (GSE3744)

### Stepwise Guide
1. Load GSE3744 dataset from GEO (Affymetrix microarray).
2. Format data: rows represent microarray probe IDs, columns represent patient samples.
3. Assign samples into two groups: Tumor (T; 40 samples), Normal Breast (NB; 7 samples).
4. Use vectorized Wilcoxon rank-sum test to identify probes differentially expressed between groups.
5. Apply Bonferroni correction for multiple testing to control false discovery rate.
6. Interpret significant probes for downstream functional analysis.

### Data Description
- Dataset contains fluorescence intensity values for 54,613 probes across 47 patients.
- Each probe is a short DNA fragment used to target transcripts (not direct gene symbols).
- Intensities reflect gene expression levels (log2-normalized).
- Samples are split between tumor tissues and normal breast tissues.

### Next Steps
- Annotate significant probes → gene symbols → genomic locations using platform annotation files
- Pathway analysis (KEGG, Reactome) & Gene Ontology (GO) enrichment on significant genes
- Visualize with volcano plots, heatmaps, MA-plots
- Apply linear models (limma) or edgeR for more robust DE analysis
- Integrate with RNA-seq/proteomics for multi-omics validation
- Batch effect correction if technical variation detected

---

## Exercise 2: Tumor Classification via Logistic Regression (Breast Cancer Dataset)

### Stepwise Guide
1. Load Wisconsin Breast Cancer diagnostic dataset with 30 tumor-related features.
2. Split dataset into training (70%) and testing (30%) sets, stratifying to preserve class balance.
3. Apply feature scaling (zero mean, unit variance) to improve model convergence.
4. Train logistic regression classifier on training data.
5. Evaluate predictive accuracy on held-out test data.

### Data Description
- 569 patient samples, 30 tumor features from biopsy images
- Features: radius, texture, perimeter, area, smoothness (mean, std, worst)
- Target: 0=benign, 1=malignant (357 benign, 212 malignant)
- Classic ML benchmark dataset

### Next Steps
- Hyperparameter tuning (GridSearchCV) & k-fold cross-validation
- Advanced classifiers: Random Forest, XGBoost, SVM, neural networks
- Feature importance analysis & SHAP values for biological interpretation
- External validation on independent cohorts
- Clinical outcome prediction (survival, recurrence risk)
- Feature engineering from additional omics data

---

## Exercise 3: Variant Impact Prediction with Neural Networks

### Stepwise Guide
1. Generate synthetic data mimicking genetic variants with 8 genomic features each.
2. Compute synthetic continuous "impact" scores simulating pathogenicity ranging from 0 to 1.
3. Split the data into training (80%) and test (20%) subsets.
4. Build a simple artificial neural network with one hidden layer.
5. Train with mean squared error loss using Adam optimizer.
6. Evaluate via mean absolute error on test data.

### Data Description
- Features represent conservation scores, allele frequency, functional class, splice distance,
  GC content, motif scores, evolutionary constraint metrics.
- Targets are continuous scores indicating predicted variant impact on gene function.

### Next Steps
- Replace synthetic data with real datasets (ClinVar, gnomAD, UK Biobank)
- Add features: protein domains, splice effects, regulatory regions
- Advanced architectures: CNNs, transformers, deep learning ensembles
- Benchmark against established predictors (REVEL, PrimateAI)
- Uncertainty quantification & confidence intervals
- Predict regulatory/splicing effects beyond coding variants

---

## Exercise 4: Protein Secondary Structure Prediction Using PyTorch

### Stepwise Guide
1. Simulate protein residues with 20-dimensional one-hot encoding representing amino acid probabilities.
2. Assign synthetic secondary structure class labels (helix, sheet, coil).
3. Split residues into training (80%) and test (20%) groups, preserving label distributions.
4. Define a small neural network with two fully connected layers and ReLU activations.
5. Train using cross-entropy loss and Adam optimizer.
6. Evaluate classification accuracy on the test subset.

### Data Description
- Input data samples represent individual amino acid residues.
- Each input feature vector encodes probability distribution over 20 amino acids.
- Class labels correspond to three-state secondary structure types.

### Next Steps
- Use real datasets: CASP, CB513, DSSP, PISCES
- Extract PSSM/HMM profiles from multiple sequence alignments
- Implement convolutional/recurrent architectures for sequence context
- Data augmentation & transfer learning from AlphaFold
- Benchmark against PSIPRED, JPred, AlphaFold2
- Predict solvent accessibility, torsion angles, 8-state structures

---

## Exercise 5: Protein Annotation Retrieval from UniProt API

### Stepwise Guide
1. Select a protein accession ID (e.g., P69905 for human hemoglobin alpha).
2. Query UniProt REST API to obtain JSON-formatted protein annotation.
3. Parse key metadata like protein name, organism, and sequence length.
4. Display retrieved information for interpretation.

### Data Description
- UniProt JSON API response containing comprehensive protein annotation
- Fields: accession, protein name, organism, sequence, function, domains
- Example: P69905 = Human hemoglobin subunit alpha

### Next Steps
- Batch retrieval for protein sets/pathways
- Extract domains, PTMs, interaction partners, disease associations
- Integrate with PDB for 3D structure visualization
- Link to KEGG/Reactome pathways & drug targets
- Prioritize proteins for experimental validation
- Combine with STRING API for protein-protein interactions

---

