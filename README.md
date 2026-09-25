# Bengali SMS Phishing Detection

A generalization evaluation framework for parameter-efficient Bengali SMS phishing detection using LoRA-adapted XLM-RoBERTa.

---

## Paper

**Beyond Memorization: A Generalization Evaluation Framework for Parameter-Efficient Bengali SMS Phishing Detection**

*Paper link to be added upon publication.*

---

## Overview

This repository contains code, models, and evaluation artifacts for detecting Bengali SMS phishing (smishing), with a focus on **generalization under distribution shift** rather than random-split accuracy.

### Key Contributions

1. **Component holdouts** (URL, phone) — expose substantial TF-IDF vulnerability under component shift
2. **Lexical-template holdouts** via character-level TF-IDF + k-means — test template variation
3. **Counterfactual protocol** with 5 unique variants (V1–V5) and 4 metrics (CRR, TDS, PS, CCR)
4. **Adversarial robustness** under 5 character-level perturbations
5. **Cross-dataset transfer** to BanglaBarta and repeated-seed stability evaluation

---

## Key Results

### Seven-Split Generalization (Macro F1)

| Model | ID | OOD | UA | URL | Phone | Template | Distant |
|-------|-----|-----|-----|-----|-------|----------|---------|
| TF-IDF + LR | 0.968 | 0.947 | 0.833 | 0.594 | 0.533 | 0.970 | 0.960 |
| BanglaBERT + LoRA | 0.876 | 0.715 | 0.811 | 0.716 | 0.750 | 0.896 | 0.885 |
| IndicBERT + LoRA | 0.889 | 0.873 | 0.837 | 0.761 | 0.840 | 0.901 | 0.892 |
| MuRIL + LoRA | 0.837 | 0.658 | 0.761 | 0.658 | 0.759 | 0.823 | 0.836 |
| **XLM-R + LoRA (ours)** | **0.986** | **0.967±0.004** | **0.986** | **0.952±0.005** | **0.969±0.007** | **0.986** | **0.978** |

*XLM-R values for OOD, URL, and Phone are mean ± std over five training seeds.*

### Counterfactual Metrics (OOD Test Set)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| CRR (Context Retention Ratio) | 0.933 | > 0.80 | ✓ |
| TDS (Template Dependence Score) | 0.017 | < 0.10 | ✓ |
| PS (Prediction Stability) | 0.972 | > 0.75 | ✓ |
| CCR (Context Contribution Ratio) | 0.950 | > 0.75 | ✓ |

### Adversarial Robustness

| Perturbation | F1 | RDR |
|--------------|-----|-----|
| Clean | 0.986 | 0.000 |
| Character repeat | 0.982 | 0.004 |
| Random char drop (15%) | 0.902 | 0.086 |
| Heavy typo (20% swap) | 0.867 | 0.122 |
| Case flip | 0.860 | 0.128 |
| Mixed (typo + drop) | 0.732 | 0.258 |

**Max RDR = 0.258** (below the heuristic 0.30 robustness threshold)

### Efficiency

- **Adapter size:** 13 MB (FP32) — task-specific adapter only
- **Base model:** 1125 MB frozen XLM-R checkpoint (required for inference)
- **Trainable parameters:** 3.25M (1.15% of total)
- **Inference:** 3.22 ms/SMS at batch size 32 (RTX 2050, 4 GB VRAM)

---

## Repository Structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_split_prep.ipynb
│   ├── 03_hard_splits.ipynb
│   ├── 04_campaign_holdout.ipynb
│   ├── 04_lora_transformer.ipynb
│   ├── 05_lora_v2.ipynb
│   ├── 06_revision_experiments.ipynb
│   ├── 06_token_analysis.ipynb
│   ├── bengali_smishing_baselines.ipynb
│   ├── bengali_smishing_cv.ipynb
│   ├── bengali_smishing_muril.ipynb
│   ├── bengali_smishing_robustness.ipynb
│   ├── cross_dataset_bangalabarta.ipynb
│   ├── random_vs_unseen.ipynb
│   └── verification_bootstrap.ipynb
│
├── data/
│   └── processed/
│       ├── cleaned.csv
│       ├── train_*.csv
│       └── test_*.csv
│
├── results/
│   ├── figures/
│   │   ├── main_comparison.png
│   │   ├── counterfactual_evaluation_fixed.png
│   │   ├── adversarial_robustness_fixed.png
│   │   └── cv_stability.png
│   └── *.json
│
└── paper/
    ├── main.tex
    └── figures/
```

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/3jibon/bengali-smishing-detection.git
cd bengali-smishing-detection
```

### 2. Install Dependencies

```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run Experiments

```bash
jupyter notebook
```

Navigate to:
- `notebooks/01_eda.ipynb` — Data exploration
- `notebooks/02_split_prep.ipynb` — Seven-split preparation
- `notebooks/05_lora_v2.ipynb` — Main LoRA training
- `notebooks/06_revision_experiments.ipynb` — Counterfactual evaluation
- `notebooks/bengali_smishing_robustness.ipynb` — Adversarial robustness
- `notebooks/bengali_smishing_cv.ipynb` — Repeated-seed stability
- `notebooks/cross_dataset_bangalabarta.ipynb` — Cross-dataset transfer

---

## Dataset

- **Source:** Bengali SMS Smishing Dataset
- **Size:** 7,005 SMS
- **Labels:** normal, promo, smish
- **Languages:** Bengali, English, Banglish, CodeMix
- **Preprocessing:** Text normalization + URL/phone masking (`[URL]`, `[PHONE]`)

### Seven Evaluation Splits

1. **ID** — In-distribution random split
2. **OOD** — Out-of-distribution (different script mix)
3. **UA** — Unseen attack (new smishing templates)
4. **URL** — URL holdout
5. **Phone** — Phone holdout
6. **Template** — Lexical-template holdout
7. **Distant** — Distant lexical-template holdout (hardest)

---

## Requirements

- Python 3.9+
- PyTorch 2.1+
- Transformers 4.35+
- PEFT 0.6+
- CUDA 12.1 (recommended)

See `requirements.txt` for the full list.

---

## Citation

If you use this code in your research, please cite:

```bibtex
@article{anonymous2026bengali,
  title={Beyond Memorization: A Generalization Evaluation Framework for Parameter-Efficient Bengali SMS Phishing Detection},
  author={Anonymous},
  year={2026}
}
```

---

## Contact

For questions, please contact the authors.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Hugging Face for model hosting and datasets
- The Bengali SMS smishing dataset contributors
- The open-source community behind PyTorch, Transformers, and PEFT
