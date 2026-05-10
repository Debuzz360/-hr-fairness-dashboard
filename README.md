# FairHire Audit Tool

**MSc Business Analytics and Technology — University of Greater Manchester**

*Reducing Bias in Machine Learning Algorithms for HR Recruitment: A Socio-Technical Schema for Ethical Data Analytics in UK Financial Services*

**Author:** Lawal Adeniyi (Student ID: 2314657)
**Supervisor:** Bren Tighe
**Submission:** May 2026
**Live App:** https://fairhire-audit.streamlit.app/

---

## Overview

The FairHire Audit Tool is a web-based governance instrument developed as part of an MSc dissertation investigating algorithmic bias in ML-based recruitment systems within UK financial services. It operationalises the four-layer socio-technical governance framework developed in the dissertation, translating empirical fairness findings into an accessible audit interface for HR practitioners and compliance teams.

The tool allows users to:

- Upload any recruitment CSV and receive a five-metric fairness audit report
- Explore interactive visualisations of the dissertation Chapter 4 findings
- Identify proxy discrimination variables using SHAP-based feature importance analysis
- Compare three bias mitigation techniques: Reweighting, ExponentiatedGradient, and ThresholdOptimizer
- Validate findings across two independently sourced datasets

---

## Dissertation Context

This tool accompanies a dissertation that:

- Trained and evaluated three ML classifiers (Logistic Regression, Random Forest, XGBoost) against five fairness metrics across two recruitment datasets
- Identified RecruitmentStrategy_1 as the dominant proxy variable (SHAP value: 1.0013), signalling indirect discrimination risk under the Equality Act 2010
- Found education bias to be the most severe finding, with Disparate Impact Ratios as low as 0.5364 in Logistic Regression — well below the 0.80 four-fifths rule practical benchmark
- Demonstrated that ThresholdOptimizer achieved the best mitigation results, achieving full compliance with the four-fifths rule benchmark on gender bias in Random Forest (DIR: 0.8622)
- Developed a four-layer socio-technical governance framework aligned with the Equality Act 2010, UK GDPR, FCA Consumer Duty 2023, and ICO AI Guidance

**Note:** The 0.80 DIR threshold is drawn from the US EEOC four-fifths rule and is used throughout as a practical benchmark in fairness auditing. It is not a statutory threshold under the Equality Act 2010.

---

## Repository Structure

```
fairhire_audit/
├── app.py                          # Home page and navigation
├── requirements.txt                # Python dependencies
├── CHAPTER4biasanalysisLAWAL.ipynb # Full Colab analysis notebook
├── .streamlit/
│   └── config.toml                 # Navy and gold theme
├── data/
│   ├── recruitment_data.csv        # Primary dataset (1,500 records)
│   ├── 2025-fairness-recruitment-dataset.csv  # Secondary dataset (225 records)
│   ├── fairness_results.csv
│   ├── shap_values.csv
│   └── mitigation_results.csv
├── models/
│   ├── model_lr.pkl
│   ├── model_rf.pkl
│   └── model_xgb.pkl
└── pages/
    ├── 01_overview.py
    ├── 02_bias_audit.py
    ├── 03_dissertation_results.py
    ├── 04_shap_analysis.py
    ├── 05_mitigation_simulator.py
    └── 06_cross_dataset_validation.py
```

---

## Datasets

| Dataset | Records | Source | Purpose |
|---------|---------|--------|---------|
| recruitment_data.csv | 1,500 | Kaggle (open licence) | Primary analysis |
| 2025-fairness-recruitment-dataset.csv | 225 | Kaggle (open licence) | Cross-dataset validation |

Both datasets are publicly available, fully anonymised, and contain no personally identifiable information. They are used solely for research and demonstration purposes.

---

## Fairness Metrics Used

| Metric | Abbreviation | Purpose |
|--------|-------------|---------|
| Statistical Parity Difference | SPD | Overall selection rate gap between groups |
| Disparate Impact Ratio | DIR | Ratio of selection rates — benchmark: 0.80 |
| Equal Opportunity Difference | EOD | Gap in true positive rates for qualified candidates |
| PPV Parity | PPV | Positive predictive value parity across groups |
| FPR Parity | FPR | False positive rate parity across groups |

---

## Running Locally

### Step 1 — Clone the repository
```bash
git clone https://github.com/Debuzz360/-hr-fairness-dashboard.git
cd -hr-fairness-dashboard
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

The app will open at http://localhost:8501

---

## Running the Colab Analysis

To reproduce the full dissertation analysis:

1. Open CHAPTER4biasanalysisLAWAL.ipynb in Google Colaboratory
2. Upload recruitment_data.csv and 2025-fairness-recruitment-dataset.csv to the Colab environment
3. Run all cells in sequence
4. Export the results CSV files and model pickle files to the data/ and models/ folders

---

## Key Findings

| Protected Group | Classifier | Baseline DIR | Post-Mitigation DIR (Best) | Technique |
|----------------|-----------|-------------|--------------------------|-----------|
| Gender | Logistic Regression | 0.9057 | 0.9148 | ThresholdOptimizer |
| Gender | Random Forest | 0.7674 | 0.8622 | ThresholdOptimizer |
| Gender | XGBoost | 0.7435 | 0.7585 | ThresholdOptimizer |
| Education | Logistic Regression | 0.5364 | 0.6012 | Reweighting |
| Education | XGBoost | 0.7274 | 0.7957 | ThresholdOptimizer |

Random Forest gender DIR of 0.8622 achieved full compliance with the 0.80 four-fifths rule practical benchmark.

---

## Four-Layer Socio-Technical Governance Framework

| Layer | Focus | Key Components |
|-------|-------|----------------|
| Layer 1 | Data Governance and Bias Detection | Pre-processing audit, protected attribute retention, baseline fairness metrics |
| Layer 2 | Explainability and Proxy Detection | SHAP analysis, proxy variable identification, feature importance ranking |
| Layer 3 | Mitigation and Model Governance | Reweighting, ExponentiatedGradient, ThresholdOptimizer, fairness-accuracy trade-off evaluation |
| Layer 4 | Governance and Regulatory Synthesis | Equality Act 2010, UK GDPR, FCA Consumer Duty 2023, ICO AI Guidance alignment |

---

## Tech Stack

- Python 3.11 — core language
- Streamlit — web application framework
- scikit-learn — ML classifiers and preprocessing
- XGBoost — gradient boosting classifier
- AIF360 — fairness metrics and Reweighting
- Fairlearn — ExponentiatedGradient and ThresholdOptimizer
- SHAP — explainability and proxy detection
- Matplotlib / Plotly — visualisation
- Google Colaboratory — analysis environment
- GitHub — version control

---

## Academic Use and Citation

This tool and the accompanying dissertation are submitted in partial fulfilment of the requirements for the award of an MSc in Business Analytics and Technology at the University of Greater Manchester (May 2026).

If referencing this work, please cite:

Adeniyi, L. (2026). Reducing Bias in Machine Learning Algorithms for HR Recruitment: A Socio-Technical Schema for Ethical Data Analytics in UK Financial Services. MSc Dissertation, University of Greater Manchester.

---

## Contact

Lawal Adeniyi
Email: Princelawaladeniyi@gmail.com
LinkedIn: linkedin.com/in/adeniyi-lawal-3034a8265
GitHub: github.com/Debuzz360
