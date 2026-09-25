# Bengali SMS Phishing Detection

A generalization evaluation framework for **parameter-efficient** Bengali SMS phishing detection using LoRA-adapted XLM-RoBERTa.

---

## 📄 Paper

**Beyond Memorization: A Generalization Evaluation Framework for Parameter-Efficient Bengali SMS Phishing Detection**

*Paper link to be added upon publication.*

---

## 🎯 Overview

This repository contains code, models, and evaluation artifacts for detecting Bengali SMS phishing (smishing), with a focus on **generalization under distribution shift** rather than random-split accuracy.

SMS phishing (smishing) is an increasingly common cyber threat targeting Bengali-speaking users through deceptive messages containing fraudulent links, phone numbers, and social-engineering tactics. While recent machine learning and transformer-based approaches report very high performance on random train/test splits, their behavior under distribution shift has received limited systematic evaluation in Bengali smishing detection. This framework evaluates models under multiple forms of distribution shift, counterfactual transformations, and adversarial perturbations.

---

## 🧠 Main Contributions

### 1. Component Holdouts

Evaluate robustness when previously unseen components appear at test time:

- **URL Holdout** — training data excludes URLs; testing contains URL-bearing messages
- **Phone Holdout** — training data excludes phone numbers; testing contains phone-number-bearing messages

These tests examine whether models depend excessively on specific surface indicators.

### 2. Lexical-Template Holdouts

Lexical-template-level evaluation using character-level TF-IDF representations and K-Means clustering of smishing messages. Two configurations are provided:

- **Distant Holdout** — clusters selected to maximize separation
- **Template Holdout** — clusters selected at intermediate similarity rank

These splits assess performance on template distributions different from those observed during training.

### 3. Counterfactual Evaluation Protocol

A structured five-variant counterfactual framework evaluates model dependence on:

- URLs
- Phone numbers
- Message templates
- Remaining contextual content

The protocol produces four aggregate interpretive metrics:

| Metric | Meaning |
|--------|---------|
| **CRR** | Context Retention Ratio |
| **TDS** | Template Dependence Score |
| **PS**  | Prediction Stability |
| **CCR** | Context Contribution Ratio |

### 4. Adversarial Robustness Analysis

Robustness is evaluated using controlled text perturbations and the **RDR (Robustness Degradation Ratio)** metric from recent smishing robustness literature.

### 5. Parameter-Efficient Deployment

The proposed model uses:

- **XLM-RoBERTa-base** with **LoRA (Low-Rank Adaptation)**
- **3.25M trainable parameters** (1.15% of total)
- **13 MB task-specific adapter**
- **4 GB VRAM** for training
- **1125 MB frozen base checkpoint** required for inference

---

## 📊 Dataset

Experiments are conducted using the publicly available **Bengali SMS Smishing Dataset**.

- **Total messages:** 7,005
- **Smish:** 2,809
- **Normal:** 2,488
- **Promotional:** 1,708

Language varieties include:

- Bengali
- English
- Banglish
- Code-Mixed SMS

**Dataset source:**

```python
from datasets import load_dataset

dataset = load_dataset(
    "shariul-islam/bengali-sms-smishing-dataset"
)
```

---

## 🧪 Evaluation Splits

### In-Distribution (ID)
Standard stratified train/test split.

### Out-of-Distribution (OOD)
Training: Bengali + English · Testing: Banglish + Code-Mixed
This evaluates cross-script and cross-language generalization.

### URL Holdout
Training data excludes URLs · Testing contains URL-bearing messages.

### Phone Holdout
Training data excludes phone numbers · Testing contains phone-number-bearing messages.

### Distant Lexical-Template Holdout
Training and testing clusters are selected to maximize separation.

### Template Lexical-Template Holdout
Held-out clusters at intermediate similarity rank to training clusters.

### Cross-Dataset Evaluation
Models trained on the Bengali SMS Smishing Dataset are evaluated on the **BanglaBarta** corpus to assess transferability across datasets.

---

## 🧩 Model Zoo

| Model | Trainable Parameters |
|-------|---------------------:|
| TF-IDF + Logistic Regression | ~0 |
| BanglaBERT + LoRA | 2.68M |
| IndicBERT + LoRA | 2.68M |
| MuRIL + LoRA | 1.80M |
| XLM-R + LoRA (ours) | **3.25M** |

---

## 📈 Main Results

### Macro F1 Comparison

| Model | ID | OOD | UA | URL | Phone | Template | Distant |
|-------|-----|-----|-----|-----|-------|----------|---------|
| TF-IDF + LR | 0.968 | 0.947 | 0.833 | 0.594 | 0.533 | 0.970 | 0.960 |
| BanglaBERT + LoRA | 0.876 | 0.715 | 0.811 | 0.716 | 0.750 | 0.896 | 0.885 |
| IndicBERT + LoRA | 0.889 | 0.873 | 0.837 | 0.761 | 0.840 | 0.901 | 0.892 |
| MuRIL + LoRA | 0.837 | 0.658 | 0.761 | 0.658 | 0.759 | 0.823 | 0.836 |
| **XLM-R + LoRA (ours)** | **0.986** | **0.967±0.004** | **0.986** | **0.952±0.005** | **0.969±0.007** | **0.986** | **0.978** |

*XLM-R values on OOD, URL, and Phone report mean ± std over five training seeds.*

---

## 🔬 Counterfactual Analysis

### Counterfactual Conditions

| Variant | Description |
|---------|-------------|
| **V1** | Original message |
| **V2** | URL placeholder removed |
| **V3** | Phone placeholder removed |
| **V4** | URL + phone placeholders removed |
| **V5** | Non-template context removed (only URL/phone retained) |

### Aggregate Metrics

| Metric | Value |
|--------|------:|
| CRR | 0.933 |
| TDS | 0.017 |
| PS  | 0.972 |
| CCR | 0.950 |

---

## 🛡️ Adversarial Robustness

Robustness is evaluated using:

- Character repetition
- Character deletion (15% random drop)
- Heavy typographical noise (20% adjacent swap)
- Case flipping
- Mixed perturbations

Performance degradation is quantified using:

```
RDR = (F1_clean − F1_perturbed) / F1_clean
```

| Perturbation | F1 | RDR |
|--------------|-----|-----|
| Clean | 0.986 | 0.000 |
| Character repeat | 0.982 | 0.004 |
| Random char drop (15%) | 0.902 | 0.086 |
| Heavy typo (20% swap) | 0.867 | 0.122 |
| Case flip | 0.860 | 0.128 |
| Mixed (typo + drop) | 0.732 | **0.258** |

Maximum RDR: **0.258**, below the heuristic 0.30 interpretation threshold.

---

## ⚡ Efficiency

| Metric | Value |
|--------|------:|
| Adapter size (task-specific) | 13 MB |
| Frozen base checkpoint | 1125 MB |
| Trainable parameters | 3.25M |
| Training time | ~10 minutes |
| Batch-32 latency | 3.22 ms/SMS |
| Single-message latency | 20.37 ms |

**Hardware:** NVIDIA RTX 2050 (4 GB VRAM)

---

## 📁 Repository Structure

```
bengali-smishing-detection/
├── README.md
├── requirements.txt
├── LICENSE
├── notebooks/          # Experiment notebooks
├── src/                # Source scripts
├── configs/            # Training configuration files
├── data/
│   └── processed/      # Preprocessed datasets
├── results/
│   ├── figures/        # Paper figures
│   └── *.json          # Evaluation result files
└── paper/              # LaTeX source
```

---

## ⚙️ Installation

```bash
git clone https://github.com/3jibon/bengali-smishing-detection.git
cd bengali-smishing-detection
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Data Preparation

```bash
python src/data_prep.py
```

Generated files:

```
data/processed/
├── cleaned.csv
├── train_id.csv
├── test_id.csv
├── train_ood.csv
├── test_ood.csv
├── train_campaign_distant.csv
├── test_campaign_distant.csv
├── train_campaign_template.csv
└── test_campaign_template.csv
```

### 2. Train XLM-R + LoRA

```bash
python src/train_lora.py \
    --config configs/lora_v2.yaml
```

Default configuration:

- Base model: `xlm-roberta-base`
- LoRA rank: 16
- Alpha: 32
- Dropout: 0.1
- Epochs: 5
- Learning rate: 3e-4
- Batch size: 8
- Gradient accumulation: 2
- FP16 enabled

### 3. Evaluate

```bash
python src/evaluate.py \
    --splits id ood ua url phone template distant
```

### 4. Counterfactual Evaluation

```bash
python src/counterfactual.py
```

### 5. Adversarial Robustness

```bash
python src/adversarial.py
```

---

## 🔁 Reproducibility

**Environment:**

- Python 3.10+
- PyTorch 2.0+
- Transformers 4.35+
- PEFT 0.6+

**Hardware:**

- NVIDIA RTX 2050 (4 GB VRAM)
- CUDA 12.x

**Random seed:** `42`

**Repeated-seed experiments use seeds:** `42, 43, 44, 45, 46`

---

## 📖 Citation

If you use this code in your research, please cite:

```bibtex
@misc{anonymous2026beyond,
  title={Beyond Memorization: A Generalization Evaluation Framework for Parameter-Efficient Bengali SMS Phishing Detection},
  author={Anonymous},
  year={2026}
}
```

---

## 🙏 Acknowledgments

- Bengali SMS Smishing Dataset contributors
- XLM-RoBERTa
- Hugging Face Transformers
- PEFT / LoRA
- BanglaBarta Dataset

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
