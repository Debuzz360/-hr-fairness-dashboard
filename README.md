# FairHire Audit Tool

**MSc Business Analytics & Technology — University of Greater Manchester**
*Reducing Bias in ML Algorithms for HR Recruitment: A Socio-Technical Schema for Ethical Data Analytics in UK Financial Services*

---

## Overview

This Streamlit application accompanies the dissertation and provides:

- **Live Bias Audit** — upload any recruitment CSV and receive a five-metric fairness report
- **Dissertation Results** — interactive visualisation of Chapter 4 fairness findings
- **SHAP Proxy Analysis** — feature importance analysis highlighting proxy discrimination
- **Mitigation Simulator** — compare Reweighting, ExponentiatedGradient, ThresholdOptimizer
- **Cross-Dataset Validation** — primary (n=1,500) vs secondary (n=225) dataset findings

---

## Project Structure

```
fairhire_audit/
├── app.py                          # Home page and navigation
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Navy and gold theme
├── data/
│   ├── primary_dataset.csv
│   ├── secondary_dataset.csv
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

## Running Locally

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add your data files
Copy your exported Colab files into the `data/` and `models/` folders.

### Step 3 — Run the app
```bash
cd fairhire_audit
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Deploying to Streamlit Cloud

### Step 1 — Push to GitHub
Create a new GitHub repository and push the entire `fairhire_audit/` folder.

```bash
git init
git add .
git commit -m "Initial FairHire app"
git remote add origin https://github.com/YOUR_USERNAME/fairhire-audit.git
git push -u origin main
```

### Step 2 — Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Select your repository, branch (`main`), and set the main file to `app.py`
5. Click **Deploy**

Streamlit Cloud will install dependencies from `requirements.txt` automatically.

### Step 3 — Add data files
If your data files are not committed to GitHub (recommended for large files),
use Streamlit Cloud's **Secrets** feature or upload via the Streamlit Cloud UI.

Alternatively, for dissertation demo purposes, commit the CSV files directly
to the repository (they are not sensitive synthetic/anonymised data).

---

## Data File Formats

### fairness_results.csv
```
Model, Group, SPD, DIR, EOD, PPV_Parity, FPR_Parity, F1_Score
Logistic Regression, Gender, -0.082, 0.741, ...
```

### shap_values.csv
```
Feature, Mean_SHAP_Value, Is_Proxy
RecruitmentStrategy_1, 0.312, True
SkillScore, 0.187, False
```

### mitigation_results.csv
```
Model, Technique, SPD_Gender, DIR_Gender, F1_Score
Logistic Regression, Baseline, -0.082, 0.741, 0.811
Logistic Regression, Reweighting, -0.041, 0.798, 0.803
```

---

## Notes

- Pages display **placeholder representative data** if CSV files are missing from `data/`
- Replace placeholder data with your actual Colab exports for the viva demonstration
- The app theme (navy #0A1628, gold #C9A84C) is consistent with dissertation figures
