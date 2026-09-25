Beyond Memorization: A Generalization Evaluation Framework for Lightweight Bengali SMS Phishing Detection
Code, experiments, and evaluation framework accompanying the research paper:

Beyond Memorization: A Generalization Evaluation Framework for Lightweight Bengali SMS Phishing Detection MD Farhan Uddin Jibon Department of Computer Science and Engineering Daffodil International University, Bangladesh

Overview
SMS phishing (smishing) is an increasingly common cyber threat targeting Bengali-speaking users through deceptive messages containing fraudulent links, phone numbers, and social-engineering tactics.

While recent machine learning and transformer-based approaches report very high performance on random train/test splits, their behavior under distribution shift has received limited systematic evaluation in Bengali smishing detection.

This repository introduces a generalization evaluation framework designed to assess whether a detector relies on robust contextual understanding or on superficial shortcuts such as URLs, phone numbers, or recurring campaign templates.

The framework evaluates models under multiple forms of distribution shift, counterfactual transformations, and adversarial perturbations.

Main Contributions
1. Component Holdouts
Evaluate robustness when previously unseen components appear at test time:

URL Holdout
Phone Holdout
These tests examine whether models depend excessively on specific surface indicators.

2. Campaign Holdouts
Campaign-level evaluation using TF-IDF representations and K-Means clustering of smishing templates.

Two configurations are provided:

Broad Campaign Holdout
Distant Campaign Holdout
These splits assess performance on campaign distributions different from those observed during training.

3. Counterfactual Evaluation Protocol
A structured counterfactual framework evaluates model dependence on:

URLs
Phone numbers
Message templates
Remaining contextual content
The protocol produces four aggregate interpretive metrics:

CRR — Context Retention Rate
TDS — Template Dependence Score
PS — Prediction Stability
CCR — Context Contribution Ratio
4. Adversarial Robustness Analysis
Robustness is evaluated using controlled text perturbations and the:

RDR (Robustness Degradation Ratio)
metric proposed in recent smishing robustness literature.

5. Lightweight Deployment
The proposed model uses:

XLM-RoBERTa-base
LoRA (Low-Rank Adaptation)
requiring only:

3.25M trainable parameters
13 MB adapter size
4 GB VRAM for training
Dataset
Experiments are conducted using the publicly available:

Bengali SMS Smishing Dataset

Total messages: 7,005
Smish: 2,809
Normal: 2,488
Promotional: 1,708
Language varieties include:

Bengali
English
Banglish
Code-Mixed SMS
Dataset source:

from datasets import load_dataset

dataset = load_dataset(
    "shariul-islam/bengali-sms-smishing-dataset"
)
Evaluation Splits
In-Distribution (ID)
Standard stratified train/test split.

Out-of-Distribution (OOD)
Training:

Bengali
English
Testing:

Banglish
Code-Mixed
This evaluates cross-script and cross-language generalization.

URL Holdout
Training data excludes URLs.

Testing contains URL-bearing messages.

Phone Holdout
Training data excludes phone numbers.

Testing contains phone-number-bearing messages.

Broad Campaign Holdout
Campaign clusters are separated using TF-IDF + K-Means.

Distant Campaign Holdout
Training and testing clusters are selected to maximize separation.

Cross-Dataset Evaluation
Models trained on the Bengali SMS Smishing Dataset are evaluated on the BangalaBarta corpus to assess transferability across datasets.

Model Zoo
Model	Trainable Parameters
TF-IDF + Logistic Regression	~0
BanglaBERT (Frozen) + LR	0
MuRIL + LoRA	0.89M
XLM-R + LoRA	3.25M
Main Results
Macro F1 Comparison
Model	ID	OOD	URL	Phone	Broad	Distant
TF-IDF + LR	0.968	0.947	0.594	0.533	0.970	0.960
BanglaBERT (Frozen)	—	0.840	—	—	—	—
MuRIL + LoRA	—	0.762	—	—	—	—
XLM-R + LoRA	0.986	0.974	0.971	0.980	0.986	0.978
Counterfactual Analysis
Counterfactual Conditions
Variant	Description
V1	Original message
V2	URL removed
V3	Phone removed
V4	URL + Phone removed
V6	Template only
V7	Template-only duplicate condition
V8	Context-only condition
Aggregate Metrics
Metric	Value
CRR	0.933
TDS	0.017
PS	0.972
CCR	0.950
Adversarial Robustness
Robustness is evaluated using:

Character repetition
Character deletion
Heavy typographical noise
Case flipping
Mixed perturbations
Performance degradation is quantified using:

RDR = (F1_clean − F1_perturbed) / F1_clean
Efficiency
Metric	Value
Adapter size	13 MB
Trainable parameters	3.25M
Training time	~10 minutes
Batch-32 latency	3.22 ms/SMS
Single-message latency	20.37 ms
Hardware:

NVIDIA RTX 2050 (4 GB VRAM)
Installation
git clone https://github.com/farhan-uddin/bengali-smishing-detection.git

cd bengali-smishing-detection

pip install -r requirements.txt
Quick Start
1. Data Preparation
python src/data_prep.py
Generated files:

data/processed/
├── cleaned.csv
├── train_id.csv
├── test_id.csv
├── train_ood.csv
├── test_ood.csv
├── train_campaign_broad.csv
├── test_campaign_broad.csv
├── train_campaign_distant.csv
├── test_campaign_distant.csv
2. Train XLM-R + LoRA
python src/train_lora.py \
    --config configs/lora_v2.yaml
Default configuration:

Base model: xlm-roberta-base
LoRA rank: 16
Alpha: 32
Dropout: 0.1
Epochs: 5
Learning rate: 3e-4
Batch size: 8
Gradient accumulation: 2
FP16 enabled
3. Evaluate
python src/evaluate.py \
    --splits id ood url phone broad distant
4. Counterfactual Evaluation
python src/counterfactual.py
5. Adversarial Robustness
python src/adversarial.py
Reproducibility
Environment:

Python 3.10+
PyTorch 2.0+
Transformers 4.35+
PEFT 0.6+
Hardware:

NVIDIA RTX 2050 (4 GB VRAM)
CUDA 12.x
Random seed:

42
Cross-validation experiments use seeds:

42, 43, 44, 45, 46
Repository Structure
bengali-smishing-detection/
├── README.md
├── requirements.txt
├── LICENSE
├── notebooks/
├── src/
├── configs/
├── results/
└── data/
Citation
@misc{jibon2026beyond,
  title={Beyond Memorization: A Generalization Evaluation Framework for Lightweight Bengali SMS Phishing Detection},
  author={Jibon, MD Farhan Uddin},
  year={2026}
}
Acknowledgments
Bengali SMS Smishing Dataset — Shariul Islam
XLM-RoBERTa
Hugging Face Transformers
PEFT / LoRA
BangalaBarta Dataset
Contact
MD Farhan Uddin Jibon Department of Computer Science and Engineering Daffodil International University, Bangladesh

Email: farhanuddinjibon@gmail.com