# FinRAG-Equinor: A Human-Validated Benchmark for Long-Form Financial Document Question Answering

[![Paper](https://img.shields.io/badge/Paper-ACL%202026-blue)](https://arxiv.org/abs/XXXX.XXXXX)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://img.shields.io/badge/DOI-10.XXXX%2Fzenodo.XXXXXXX-orange)](https://doi.org/10.XXXX/zenodo.XXXXXXX)

## 📋 Overview

**FinRAG-Equinor** is a question-answering benchmark for evaluating retrieval systems on long-form enterprise documents. The dataset comprises:

- **17,994** semantically segmented text chunks extracted from 15 years of oil & gas annual reports (2010–2024)
- **230** expert-validated question-answer pairs
- **Substantial inter-annotator agreement**: Cohen's κ = 0.79

Unlike existing financial QA benchmarks that focus on short passages or isolated tables, FinRAG-Equinor addresses **multi-paragraph reasoning** over narrative-heavy regulatory filings, requiring systems to locate and synthesize information across hierarchical document structures.

### Key Features

✅ **Long-form documents**: 200–350 page annual reports  
✅ **Rigorous validation**: 5-stage human-in-the-loop curation  
✅ **Chunking-agnostic evaluation**: Keyword-based grounding with threshold sensitivity (50%, 60%, 70%)  
✅ **Diverse question types**: Numerical extraction (24.8%), multi-hop reasoning (13.0%), causal inference (8.3%)  
✅ **Challenging baseline**: E5-large-v2 achieves MRR@10 of 0.580 (significant room for improvement)

---

## 📊 Dataset Statistics

| **Metric** | **Value** |
|------------|-----------|
| Annual reports (years) | 15 (2010–2024) |
| Total pages | ~4,125 |
| Total words | ~2,250,000 |
| Text chunks (semantic) | 17,994 |
| QA pairs | 230 |
| Multi-hop questions | 30 (13.0%) |
| Questions with year constraints | 187 (81.3%) |
| Cohen's κ (IAA) | 0.79 (Substantial) |

### Question Type Distribution

| Type | Count | Percentage |
|------|-------|------------|
| Numerical extraction | 57 | 24.8% |
| Multi-hop reasoning | 30 | 13.0% |
| Conceptual definition | 20 | 8.7% |
| Causal reasoning | 19 | 8.3% |
| Temporal comparison | 18 | 7.8% |
| Other | 86 | 37.4% |

### Difficulty Distribution

| Level | Count | Percentage |
|-------|-------|------------|
| Easy (single fact) | 60 | 26.1% |
| Medium (context required) | 122 | 53.0% |
| Hard (multi-hop, cross-section) | 48 | 20.9% |

---

## 📁 Repository Structure

```
FinRAG-Equinor/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0 license
├── data/
│   ├── qa_pairs.jsonl                 # 230 question-answer pairs
│   ├── corpus_metadata.json           # Metadata for 17,994 chunks
│   └── chunk_statistics.json          # Statistics per chunking strategy
├── evaluation/
│   ├── evaluate_retrieval.py          # Main evaluation script
│   ├── keyword_grounding.py           # Keyword-based answer grounding
│   ├── threshold_validation.py        # 50%/60%/70% threshold analysis
│   └── metrics.py                     # MRR, Hit@K, Precision, Recall
├── baselines/
│   ├── dense_retrieval.py             # MPNet, BGE, E5 baseline
│   ├── reproduce_results.sh           # Script to reproduce baseline results
│   └── requirements.txt               # Python dependencies
├── docs/
│   ├── annotation_guidelines.md       # Complete annotation protocol
│   ├── data_format.md                 # Data format specification
│   └── chunking_strategies.md         # 7 chunking strategies used
└── scripts/
    ├── download_reports.sh            # Instructions to download source PDFs
    └── create_chunks.py               # Script to regenerate chunks from PDFs
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/[YOUR-USERNAME]/FinRAG-Equinor.git
cd FinRAG-Equinor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r baselines/requirements.txt
```

### Download Source Documents

Annual reports are publicly available SEC Form 20-F filings:

```bash
# Download from Equinor's investor relations website
# Years: 2010–2024
# Link: https://www.equinor.com/investors/annual-report

# Alternatively, use our download script
bash scripts/download_reports.sh
```

**Note**: Due to copyright restrictions, we do not distribute the original PDFs. Users must download them from the official source.

### Reproduce Baseline Results

```bash
cd baselines

# Run all baselines (MPNet, BGE, E5)
bash reproduce_results.sh

# Or run individual models
python dense_retrieval.py --model e5-large-v2 --chunking semantic-130
```

**Expected output** (E5-large-v2 with Semantic-130 chunking):
```
MRR@10: 0.5803
Hit@1:  50.4%
Hit@5:  65.2%
Hit@10: 71.3%
```

---

## 📖 Data Format

### QA Pairs (`data/qa_pairs.jsonl`)

Each line is a JSON object with the following fields:

```json
{
  "id": "gold_en_2017_para_000013",
  "question": "According to the 2017 document, what potential benefit does the company name change have?",
  "answer": "The name has potential to strengthen the company's attractiveness with investors and talent.",
  "year": 2017,
  "query_type": "other",
  "difficulty": "medium",
  "gold_paragraph_ids": ["en_2017_para_000013"],
  "requires_multiple_paragraphs": false,
  "answer_span": {
    "found": true,
    "char_start": 0,
    "char_end": 185,
    "paragraph_id": "en_2017_para_000013"
  }
}
```

**Field Descriptions**:
- `id`: Unique identifier for the QA pair
- `question`: The question text
- `answer`: Gold-standard answer extracted from the document
- `year`: Report year (2010–2024)
- `query_type`: `numerical_exact`, `other`, `reason_why`, etc.
- `difficulty`: `easy`, `medium`, `hard`
- `gold_paragraph_ids`: List of relevant paragraph IDs
- `requires_multiple_paragraphs`: Boolean indicating multi-hop reasoning
- `answer_span`: Character-level span location in source paragraph

### Corpus Metadata (`data/corpus_metadata.json`)

Metadata for all 17,994 chunks:

```json
{
  "chunks": [
    {
      "chunk_id": "en_2017_para_000013",
      "year": 2017,
      "text": "Full paragraph text...",
      "word_count": 130,
      "section": "Strategic Overview",
      "page_number": 15
    }
  ]
}
```

**Note**: Due to file size (~150MB), the full corpus text is available via:
- **Zenodo**: [https://doi.org/10.XXXX/zenodo.XXXXXXX](https://doi.org/10.XXXX/zenodo.XXXXXXX)
- **Hugging Face**: [https://huggingface.co/datasets/[USERNAME]/FinRAG-Equinor](https://huggingface.co/datasets/[USERNAME]/FinRAG-Equinor)

---

## 🔍 Evaluation Methodology

### Chunking-Agnostic Grounding

For each question $q$ with gold answer $a$, a retrieved chunk $c$ is deemed relevant if:

$$
\text{Overlap}(c, a) = \frac{|\text{Keywords}(c) \cap \text{Keywords}(a)|}{|\text{Keywords}(a)|} \geq \tau
$$

Where $\tau$ is the overlap threshold (default: 0.60).

### Running Evaluation

```bash
cd evaluation

# Evaluate with default threshold (60%)
python evaluate_retrieval.py \
  --predictions results/e5_predictions.jsonl \
  --gold_data ../data/qa_pairs.jsonl \
  --threshold 0.60

# Sensitivity analysis (50%, 60%, 70%)
python threshold_validation.py \
  --predictions results/e5_predictions.jsonl \
  --gold_data ../data/qa_pairs.jsonl
```

**Output**:
```
Threshold: 0.50 | MRR: 0.5921 | Hit@10: 73.5%
Threshold: 0.60 | MRR: 0.5803 | Hit@10: 71.3%  ✓ (Optimal)
Threshold: 0.70 | MRR: 0.5654 | Hit@10: 68.7%
```

### Metrics

- **MRR@k**: Mean Reciprocal Rank (first relevant chunk in top-k)
- **Hit@k**: Recall at k (% queries with ≥1 relevant chunk in top-k)
- **Precision@k / Recall@k**: Standard IR metrics

---

## 📈 Baseline Results

| **Model** | **Chunking** | **MRR@10** | **Hit@1** | **Hit@5** | **Hit@10** |
|-----------|--------------|------------|-----------|-----------|------------|
| MPNet | Semantic-130 | 0.313 | 23.0% | 38.3% | 43.9% |
| MPNet | Fixed-256 | 0.287 | 20.4% | 35.2% | 41.3% |
| BGE-large | Semantic-130 | 0.328 | 23.0% | 40.9% | 47.4% |
| BGE-large | Fixed-256 | 0.301 | 21.3% | 37.4% | 43.5% |
| **E5-large-v2** | **Semantic-130** | **0.580** | **50.4%** | **65.2%** | **71.3%** ✓ |
| E5-large-v2 | Fixed-256 | 0.488 | 40.0% | 54.3% | 67.4% |

**Key Observations**:
- ✅ **E5-large-v2** achieves best performance (instruction-tuned embeddings)
- ✅ **Semantic chunking** consistently outperforms fixed-length (+8–19% MRR)
- ⚠️ **Substantial headroom**: Even best system correctly ranks relevant chunks first for only 50.4% of queries

---

## 📚 Citation

If you use FinRAG-Equinor in your research, please cite:

```bibtex
@inproceedings{yang2026finrag,
  title={FinRAG-Equinor: A Human-Validated Benchmark for Long-Form Financial Document Question Answering},
  author={Yang, Xiaojing},
  booktitle={Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL)},
  year={2026},
  url={https://arxiv.org/abs/XXXX.XXXXX}
}
```

---

## 🤝 Contributing

We welcome contributions! Please open an issue or pull request if you:

- Find errors in annotations
- Have suggestions for improving evaluation protocols
- Want to add new baseline systems
- Propose extensions (multilingual QA, conversational setting, etc.)

---

## 📄 License

This dataset is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to:
- ✅ Share — copy and redistribute the material
- ✅ Adapt — remix, transform, and build upon the material for any purpose

Under the following terms:
- 📝 **Attribution** — You must give appropriate credit and indicate if changes were made

See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgments

- **Data Source**: Equinor ASA annual reports (2010–2024), publicly available at [https://www.equinor.com/investors](https://www.equinor.com/investors)
- **Annotators**: We thank the two annotators for their careful validation work (compensated at $25/hour)
- **Funding**: This work was supported by Uppsala University, Department of Linguistics and Philology

---

## 📧 Contact

- **Author**: Xiaojing Yang
- **Email**: xiaojing.yang.4987@student.uu.se
- **Institution**: Uppsala University, Sweden
- **GitHub Issues**: [https://github.com/[YOUR-USERNAME]/FinRAG-Equinor/issues](https://github.com/[YOUR-USERNAME]/FinRAG-Equinor/issues)

---

## 🔗 Links

- 📄 **Paper**: [https://arxiv.org/abs/XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)  
- 💾 **Zenodo Archive**: [https://doi.org/10.XXXX/zenodo.XXXXXXX](https://doi.org/10.XXXX/zenodo.XXXXXXX)  
- 🤗 **Hugging Face**: [https://huggingface.co/datasets/[USERNAME]/FinRAG-Equinor](https://huggingface.co/datasets/[USERNAME]/FinRAG-Equinor)  
- 📊 **Leaderboard**: [https://finrag-equinor.github.io/leaderboard](https://finrag-equinor.github.io/leaderboard) (coming soon)

---

**Last Updated**: March 8, 2026  
**Version**: 1.0.0
